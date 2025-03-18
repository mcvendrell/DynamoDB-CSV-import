# Before use, install dependencies
# pip install awscli
# pip install boto3
# Additionally, AWS should be configured
# aws configure

import boto3
import csv
import json

# INTRUCTIONS
# Open the CSV file in Excel and go to "Data" -> "From Text/CSV"
# This will change original dynamodb export columns delimiter from , to ;
# Save the file with a new name and close Excel. This is necessary only if you have List or Map fields in your CSV
#      because the inner fields are separated by "," and this will cause issues with columns, so columns now are separated by ";"
# If you don't change the delimiter, you will have to change the delimiter at the end in the code from ; to ,
# Now, configure params below and run the script

# True = logs in console
debug = False

# Configure params
table_name = 'YOU_TABLE_HERE'
csv_file_path = 'C:/Temp/usersexcel.csv'

# Access to dynamodb
dynamodb_client = boto3.client('dynamodb', region_name='eu-west-1')

def parse_value(value):
    """Converts values to lists, maps, or leaves them as string/number."""
    if value == "":
        return None

    try:
        parsed = json.loads(value)
        return parsed
    except json.JSONDecodeError:
        return value

def convert_item(row):
    """Transform a CSV row in a DynamoDB format."""
    item = {}

    for key, value in row.items():
        parsed_value = parse_value(value)

        if debug:
            print(f"Key -> {key} -- {parsed_value}")

        if parsed_value is None:
            continue

        # Handle types
        if key in ["skills"] and isinstance(parsed_value, list):
            item[key] = {"L": parsed_value}  # List of strings
        elif key == "communications" and isinstance(parsed_value, dict):
            item[key] = {"M": parsed_value}  # Map
        elif key in ["totalVotes"] and isinstance(parsed_value, (int, float, str)):
            item[key] = {"N": str(parsed_value)}  # Numbers
        else:
            item[key] = {"S": str(parsed_value)}  # Default as string

    return item

# Read CSV file and process each row
with open(csv_file_path, mode='r', encoding='ISO-8859-1') as file:
    reader = csv.DictReader(file, delimiter=';')
    count = 0

    for row in reader:
        count += 1

        print(f"Processing row {count}...")
        if debug:
            print("-----------------------------------------------------------------------------------------------------")
            print("row in raw ->", row)

        item = convert_item(row)

        if debug:
            print("Parsed ->", item)
            # print(json.dumps(item, indent=2))

        dynamodb_client.put_item(TableName=table_name, Item=item)

print(f"✅ Data from {csv_file_path} has been successfully pushed to DynamoDB table {table_name}.")

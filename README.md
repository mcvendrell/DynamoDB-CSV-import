# DynamoDB-CSV-import
Import CSV file to DynamoDB table

Read full article in Medium: https://mcvendrell.medium.com/how-to-import-an-exported-csv-file-into-a-dynamodb-table-02cf7cf08637

## Summarize

Sometimes you need to export your table and import in another table. It's an easy operation in SQL, but with DynamoDB the process is different.

So I invest some hours creating and testing this script in Python to easely export and import the common used data I usually manage (String, Number, List and Map values).

They key here is to note that, when you use (and I do) the "Download Data as CSV" option available in the AWS Management Console, all goes fine unless you have List(L) or Map(M) values.

This is an example of my original CSV data file generated by AWS:
```
  "region","id","communications","name","role","skills"
  "ES","a","","Admin","admin",""
  "ES","b","{""vote"":{""S"":""Y""},""ads"":{""S"":""Y""}}","Pablo Mármol","worker","[{""S"":""barista""}]"
  "ES","c","{""vote"":{""S"":""Y""},""ads"":{""S"":""Y""}}","Pedro Picapiedra","worker","[{""S"":""barista""},{""S"":""bartender""}]"
```
All quoted and separated by `,` The problem here is that inner L and M values also are separated by `,` so a basic scripting operation to split fields by comma will not work.

## Reconvert with Excel
The easiest way to solve this problem is to use Excel to import CSV file, go to "Data" -> "From Text/CSV" and use comma as separator fields. Then you will end with something like this:

```
  region;id;communications;name;role;skills
  ES;a;;Admin;admin;
  ES;b;"{""vote"":{""S"":""Y""},""ads"":{""S"":""Y""}}";Pablo Mármol;worker;"[{""S"":""barista""}]"
  ES;c;"{""vote"":{""S"":""Y""},""ads"":{""S"":""Y""}}";Pedro Picapiedra;worker;"[{""S"":""barista""},{""S"":""bartender""}]"
```
And now, we are ready to work with scripting in Python.

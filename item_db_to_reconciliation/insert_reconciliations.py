#!/usr/bin/env python.
'''
    File name: job_equip_hex_converter.py
    Date created: November 22, 2017
    Python version: 3.6.1
    Purpose: Inserts new rows into the item_db

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import openpyxl  # excel plugin

out_path = "C:/repos/eRODev/rAthena Files/db/import/ero_item_db"

# extracts data from the spreadsheet
sheet_path = "C:/repos/essencero_restoration/item_db_to_reconciliation/reconciliation.xlsx"

excel = openpyxl.load_workbook(filename=sheet_path, data_only=True)

# to get sheetnames:
# excel.get_sheet_names()
target_sheet = "export"

ex_sheet = excel.get_sheet_by_name(target_sheet)

column = ex_sheet["AD"]
new_entry = {}
for cell in column:
    row = cell.value
    try:
        item_id = row.split(",")[0]
        new_entry[item_id] = row
        print("New entry: " + item_id + row[5:15])
    except IndexError:
        pass

old_filename = "item_db.txt"
old_path = out_path + "/" + old_filename
print("Opening: " + old_path)
old_f = open(file=old_path, mode='r')

new_filename = "item_db_new.txt"
new_path = out_path + "/" + new_filename
print("Opening: " + new_path)
new_f = open(file=new_path, mode="w+")

for line in old_f:
    line_split = line.split(",")
    if(len(line_split) >= 22):
        item_id = line_split[0]
        if(item_id[:2] != "//" and item_id in new_entry):
            entry = new_entry.pop(item_id)
            # If not commented out and id matches the new entry insert
            entry_length = len(entry.split(","))
            if(entry_length>=22):
                print("Inserting... " + item_id + entry[5:15])
                new_f.write(entry + "\n")
            else:
                print("Bad number of columns for " + item_id + ". Columns: " + entry_length)
        else:
            # If the line is not referenced in the file, write it.
            new_f.write(line)
    else:
        # If the line is not referenced in the file, write it.
        new_f.write(line)


left_overs = []
for item in new_entry:
    left_overs.append(item)

print("Could not find the following items: ")
print(",".join(left_overs))
# prints all 

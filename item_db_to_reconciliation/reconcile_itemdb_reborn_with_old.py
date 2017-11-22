#!/usr/bin/env python.
'''
    File name: reconcile_itemdb_reborn_with_old.py
    Date created: November 17, 2017
    Python version: 3.6.1
    Purpose: to recreate the item_db.txt table from essenceRO.

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
# TSV file old old eRO, webscraped
oldero_item_db_path = "D:/repos/essencero_restoration/web_scrape_web_archive/item_db_web_archive.tsv"

# essenceRO reborn item_db
reborn_item_db_path = "D:/repos/eRODev/rAthena Files/db/import/ero_item_db/item_db.txt"

# populates old database from old item_db
# old_db = {}
# with open(file=oldero_item_db_path, mode="r") as old_f:
#     old_f.readline()  # skips header
#     for line in old_f:
#         item_key = line.split("\t")[2].lower()
#         old_db[item_key] = line

o_filename = "out_reborn_itemdb_keys.tsv"

o_file = open(file=o_filename, mode="w")
header = "item key\titem_id\titem_name\n"
o_file.write(header)

# populates old database from old item_db
# writes all the keys and id of each item to a tsv
new_db = {}
with open(file=reborn_item_db_path, mode="r") as new_f:
    for line in new_f:
        if(
            len(line.split(",")) == 22 and  # if valid db entry
            line[:2] != "//"              # if commented out, skip
        ):
            line_split = line.split(",")
            item_id = line_split[0]
            item_key = line_split[1]
            item_name = line_split[2]
            entry = item_key + "\t" + item_id + "\t" + item_name + "\n"
            print(entry)
            o_file.write(entry)

# close file writers
o_file.close()
new_f.close()

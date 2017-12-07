#!/usr/bin/env python.
'''
    File name: build_items.py
    Date created: December 6, 2017
    Python version: 3.6.1
    Purpose:
        Converts the item_db.txt to a tsv file.
    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from os.path import isdir   # checks to see if a folder exists
import re  # regular expression


# script goes here
def main():
    if isdir("C:/repos"):
        repo_dir = "C:/repos"
    elif isdir("D:/repos"):
        repo_dir = "D:/repos"  # change this to your own

    # ero_db = repo_dir + "/eRODev/rAthena Files/db/import/ero_item_db/item_db.txt"
    iro_db = repo_dir + "/eRODev/rAthena Files/db/import/iro_item_db/item_db.txt"
    in_dir = iro_db
    out_dir = repo_dir + "/essencero_restoration/scripts/outputs/"
    out_filename = "item_db.tsv"

    item_db_to_tsv(in_dir=in_dir, out_dir=out_dir + out_filename)


# takes in a file path for an item_db and converts it to tsv
def item_db_to_tsv(in_dir, out_dir):
    out_f = open(file=out_dir, mode="w+")
    header = "ID\tAegisName\tName\tType\tBuy\tSell\tWeight\tATK\tDEF\tRange\tSlots\tJob\tClass\tGender\tLoc\twLV\t" \
             "eLV[:maxLevel]\tRefineable\tView\t{ Script }\t{ OnEquip_Script }\t{ OnUnequip_Script }\n"
    out_f.write(header)

    item_line_pattern = "^\d{3,5},.{0,}$\n"
    line_has_item = re.compile(item_line_pattern)

    with open(file=in_dir, mode="r") as in_f:
        for line in in_f:
            if line_has_item.match(line):
                # if an item line
                script_start_index = line.find("{")
                new_entry = line[:script_start_index].replace(",", "\t")

                script_split = line[script_start_index:].split(",{")
                new_entry += script_split[0]
                new_entry += "\t" + script_split[0]
                new_entry += "\t" + script_split[0]
                out_f.write(new_entry + "\n")
    out_f.close()


main()

#!/usr/bin/env python.
'''
    File name: build_items.py
    Date created: December 14, 2017
    Python version: 3.6.1
    Purpose:
        Converts the iteminfo lua to a tsv.
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

    # encoding = "latin1"
    # encoding = "iso8859_15"
    # encoding = "iso8859_9"
    encoding = "850"
    ########################################################################
    # 1. Parse in iteminfo.lua, formulate an item dictionary               #
    ########################################################################
    iteminfo_dir = repo_dir + "/eRODev/eRO Client Data/system/itemInfosryx.lub"
    iteminfo_lua = parse_item_info_lua(
        file_dir=iteminfo_dir,
        item_dict={},  # designating a new dictionary
        encoding=encoding)
    ########################################################################
    # 2. Write file out to TSV                                             #
    ########################################################################
    out_dir = repo_dir + "/essencero_restoration/scripts/outputs/"
    out_filename = "itemInfosryx.tsv"
    item_db_to_tsv(in_dir=in_dir, out_dir=out_dir + out_filename, db=iteminfo_lua["iteminfo_db"], encoding=encoding)


# takes in a file path for an item_db and converts it to tsv
def item_db_to_tsv(in_dir, out_dir, db, encoding):
    out_f = open(file=out_dir, mode="w+", encoding=encoding)
    header = "itemId\tunidentifiedDisplayName\tunidentifiedResourceName\tunidentifiedDescriptionName\t" \
             "identifiedDisplayName\tidentifiedResourceName\tidentifiedDescriptionName\tslotCount\tClassNum\n"
    out_f.write(header)

    for item_id in db:
        print(item_id)
        out_list = []
        out_list.append(str(item_id))
        out_list.append(str(db[item_id]["unidentifiedDisplayName"]))
        out_list.append(str(db[item_id]["unidentifiedResourceName"]))
        out_list.append(str(db[item_id]["unidentifiedDescriptionName"]))
        out_list.append(str(db[item_id]["identifiedDisplayName"]))
        out_list.append(str(db[item_id]["identifiedResourceName"]))
        out_list.append(str(db[item_id]["identifiedDescriptionName"]))
        out_list.append(str(db[item_id]["slotCount"]))
        out_list.append(str(db[item_id]["ClassNum"]))
        out_line = "\t".join(out_list) + "\n"
        out_f.write(out_line)
    out_f.close()


# Parses an iteminfo lua and returns a 3 element dictionary whoses keys are
# beg, mid, and end.
# beg is the begining of the file
# mid is the data structure in the middle of the file as a dictionary
# end is the remaining code in the file after the data structure
def parse_item_info_lua(file_dir, item_dict, encoding):
    print_opening_dir(file_dir=file_dir)
    ############
    # Patterns #
    ############
    # Begin item match
    new_item_line_pattern = "^\s{4,}\[\d{3,5}]\s{1,}?=\s{1,}?{$\n"
    is_new_item_line = re.compile(new_item_line_pattern)

    # 3~5 digit item code
    item_code_pattern = "\d{3,5}"
    extract_item_code = re.compile(item_code_pattern)

    # line that contains key value pairs
    key_value_line_pattern = '^\s{4,}\w{1,}\s{1,}?=\s{1,}?((".{0,}"|\d{1,})|{.{0,}}),?$\n'
    is_key_value_line = re.compile(key_value_line_pattern)

    # line that starts a multi line embedded object in the lua object
    multi_line_embed_key_pattern = '^\s{4,}\w{1,}\s{1,}?=\s{1,}?{$\n'
    is_multi_line_embed_key = re.compile(multi_line_embed_key_pattern)

    # line that has the values of a multi line embedded object
    multi_line_embed_value_pattern = '^\s{4,}(-- )?(\s{1,})?(\w{1,})?(\s{1,})?".{0,}",?$\n'
    is_multi_line_embed_value = re.compile(multi_line_embed_value_pattern)

    # marks the end of the data structure of the file by finding the main function
    end_of_data_pattern = "^function\s{1,}main\(.{0,}\)$\n|^main\s{0,}=\s{0,}function\(.{0,}\)$\n"
    is_end_of_data = re.compile(end_of_data_pattern)

    # return objects
    lua_beg = ""
    lua_end = "\n"

    # loop state objects
    current_item_id = -1
    stage_of_file = "beg"
    current_embed_key = ""

    with open(file=file_dir, mode="r", encoding=encoding) as lua:
        counter = 0
        for line in lua:
            if is_new_item_line.match(line):
                # if item code is found,
                # extract item code
                current_item_id = re.search(pattern=extract_item_code, string=line).group(0)
                if current_item_id not in item_dict:
                    item_dict[current_item_id] = {}
                    # make a new dictionary reference
                stage_of_file = "iteminfo_db"
            elif is_key_value_line.match(line):
                # if this is a key_value_pair line
                # add that key and value to the current item
                key_value_list = line.split("=")

                # key
                key = key_value_list[0].strip().replace("\n", "")

                # value
                value = key_value_list[1].strip().replace("\n", "")
                if value[-1:] == ",":  # removes trialing comma
                    # if there is a trailing comma, remove it
                    value = value[:-1]

                # adds key and value to the current item dict
                item_dict[current_item_id][key] = value

                # if key == 'identifiedResourceName' and current_item_id == '4131':
                #     print(line)
            elif is_multi_line_embed_key.match(line):
                # if it's the start of a multi line embed, create an embedded dictionary with a list
                # as it's value
                key = line.split("=")[0].strip()
                item_dict[current_item_id][key] = []
                current_embed_key = key
            elif is_multi_line_embed_value.match(line):
                # if it's the values of a multi line embed, append it to the descriptions list
                value = line.strip()
                if value[-1:] == ",":
                    value = value[:-1]
                item_dict[current_item_id][current_embed_key].append(value)
            elif stage_of_file == "beg":
                # if it's still part of the file before the item data structure,
                #   record everything to be rewritten later
                lua_beg += line
            elif is_end_of_data.match(line):
                # if it's past part of the item data structure in the file,
                #   record everything to be rewritten later
                stage_of_file = "end"
                lua_end += line
            elif stage_of_file == "end":
                # if it's past part of the item data structure in the file,
                #   record everything to be rewritten later
                lua_end += line
            else:
                # These are the lines skipped, print to be sure we didn't leave
                #     anything  behind.
                ignored_data = line.strip()
                if ignored_data != "":
                    if ignored_data[0] != "}":
                        print("Skipping line: " + str(counter) + ": " + line)
            counter += 1

    print("Parsed " + str(counter) + " lines from Lua.")
    item_lua_dict = {
        "beg": lua_beg,
        "iteminfo_db": item_dict,
        "end": lua_end
    }
    return item_lua_dict


# Tells the user in the console what file is currently being opened.
def print_opening_dir(file_dir):
    file_dir_split = file_dir.split("/")
    filename = file_dir_split[-1]
    file_path = file_dir_split[:-1]
    print("Opening: " + filename + " | From: " + "/".join(file_path))

main()

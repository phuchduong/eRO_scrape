#!/usr/bin/env python.
'''
    File name: insert_new_items_from_itemdb_into_iteminfo.py
    Date created: December 2, 2017
    Python version: 3.6.1
    Purpose:
        Inserts item_db entries that do not exist in the iteminfo.lua
    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import re  # regular expression
from os.path import isdir   # checks to see if a folder exists


def main():
    # for a list of valid codecs:
    #     essencero_restoration\Lua Codecs.xlsx
    # 437 is english codec
    encoding = "437"

    ###############
    # file system #
    ###############

    # your repo directory should look like this
    #
    # /repo root (essencero_restoration)
    #   \web_scrape_tamsinwhitfield
    #       /old_essence_item_db.txt
    #   \web_scrape_web_archive
    #       /item_db_web_archive.tsv
    if isdir("C:/repos"):
        repo_dir = "C:/repos"
    elif isdir("D:/repos"):
        repo_dir = "D:/repos"  # change this to your own

    #################################################################
    # 1. Parse in iteminfo.lua, formulate an item dictionary        #
    #################################################################
    iteminfo_dir = repo_dir + "/eRODev/eRO Client Data/system/itemInfosryx.lub"
    iteminfo_lua = parse_item_info_lua(
        file_dir=iteminfo_dir,
        item_dict={},
        encoding=encoding)
    #################################################################
    # 2. Parse in item_db, formulate an item dictionary             #
    #################################################################
    itemdb_dir = repo_dir + "/eRODev/rAthena Files/db/import/ero_item_db/item_db.txt"
    item_db = parse_item_db(file_dir=itemdb_dir, item_db={})
    #################################################################
    # 3. Insert entries that do not exist iteminfo.lua from item_db #
    #################################################################
    #################################################################
    # 4. Write out the item dictionary to a new iteminfo.lua        #
    #################################################################
    new_lua_dir = repo_dir + "/eRODev/eRO Client Data/system/new_itemInfosryx.lub"
    write_lua_items_to_lua(file_dir=new_lua_dir, lua_parts=iteminfo_lua, encoding=encoding)


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
                value = key_value_list[1].strip().replace("\n", "").replace("}", "").replace("{", "")
                if value[-1:] == ",":  # removes trialing comma
                    # if there is a trailing comma, remove it
                    value = value[:-1]

                # adds key and value to the current item dict
                item_dict[current_item_id][key] = value
            elif is_multi_line_embed_key.match(line):
                # if it's the start of a multi line embed, create an embedded dictionary with a list
                # as it's value
                key = line.split("=")[0].strip
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
    max_length = 30
    if len(file_dir) > max_length:
        filename = "..." + file_dir[-max_length:]
    else:
        filename = file_dir
    print("Opening: " + filename)


# Tells the user how many lines were writte to a file
def print_writing_status(counter, file_dir):
    filename = file_dir.split("/")[-1]
    print("Found... " + str(counter) + " items in " + filename + "\n")

# Writes an iteminfo lua and from a 3 element dictionary parameter [1]<lua_parts> whoses keys are
# beg, mid, and end.
# beg is the begining of the file
# mid is the data structure in the middle of the file as a dictionary
# end is the remaining code in the file after the data structure
# [0]<file_dir> is the full path of the file to be written
# [2]<is_korean> can be True or False, true will specify encoding of ms949 for korean encoding
#     while false will yeild utf-8 encoding
def write_lua_items_to_lua(file_dir, lua_parts, encoding):
    print_opening_dir(file_dir=file_dir)

    # file parts
    lua_beg = lua_parts["beg"]
    lua_dict = lua_parts["iteminfo_db"]
    lua_end = lua_parts["end"]

    # writting specs
    spaces_per_tab = 4
    tab = " " * spaces_per_tab

    f = open(file=file_dir, mode="w+", encoding=encoding)
    f.write(lua_beg)  # first line

    lua_dict_keys = sorted([int(x) for x in lua_dict])
    for item_id in lua_dict_keys:
        item_id = str(item_id)
        f.write(tab + "[" + item_id + "] = {\n")
        for item_key in sorted(lua_dict[item_id]):
            if isinstance(lua_dict[item_id][item_key], list):

                multi_line_embed_str = tab * 2 + item_key + " = {\n"

                for item in lua_dict[item_id][item_key]:
                    multi_line_embed_str += tab * 3 + item + ",\n"
                multi_line_embed_str += tab * 2 + "},\n"
                f.write(multi_line_embed_str)
            else:
                f.write(tab * 2 + str(item_key) + " = " + str(lua_dict[item_id][item_key]) + ",\n")
        f.write(tab + "},\n")
    f.write("}\n")
    f.write(lua_end)
    print("Writing " + str(len(lua_dict)) + " items to... " + file_dir)
    f.close()


# Takes in a dictionary and creates a list of headers for a csv file
# based upon all keys inside of the dictionary.
# Params:
#   dict: takes in a dictioanry to populate the headers with its keys
#   prefix: what the items headers should be prefixed with, helps mitigate colisions when
#       merging two dictionaries together
#   pk: primary key name of the parent key of the file to be incorporated into the list of header names
# Return: a list of header names
def scan_headers(dictionary, name_of_pk):
    headers = [name_of_pk]
    for item_id in dictionary:  # loop over all items
        for attribute in dictionary[item_id]:  # loop over all attributes of items
            if attribute not in headers:
                headers.append(attribute)
    return headers

# derives unidentifiedDisplayName from the item_db
def get_unidentifiedDisplayName(item_entry):
    # if it's not a weapon or an armor, keep the name the same
    #   when unidentified since it kind of doesn't matter
    unidentifiedDisplayName = item_entry["display_name"]
    return unidentifiedDisplayName

# derives unidentifiedResourceName from the item_db
def get_unidentifiedResourceName(item_entry):
    
    return unidentifiedResourceName


# derives unidentifiedDescriptionName from the item_db
def get_unidentifiedDescriptionName(item_entry):
    
    return unidentifiedDescriptionName


# derives identifiedDisplayName from the item_db
def get_identifiedDisplayName(item_entry):
    
    return identifiedDisplayName


# derives identifiedResourceName from the item_db
def get_identifiedResourceName(item_entry):
    
    return identifiedResourceName


# derives identifiedDescriptionName from the item_db
def get_identifiedDescriptionName(item_entry):
    
    return identifiedDescriptionName


# derives slotCount from the item_db
def get_slotCount(item_entry):
    
    return slotCount


# derives ClassNum from the item_db
def get_ClassNum(item_entry):
    
    return ClassNum


main()

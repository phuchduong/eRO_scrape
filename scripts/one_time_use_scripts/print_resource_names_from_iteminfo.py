#!/usr/bin/env python.
'''
    File name: generate_dyes_for_valk_helms.py
    Date created: December 4, 2017
    Python version: 3.6.1
    Purpose:
        Prints an item id, and its resource name in cp850 encoding
    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import re  # regular expression
from os.path import isdir   # checks to see if a folder exists

def main():

    ###############
    # file system #
    ###############

    if isdir("C:/repos"):
        repo_dir = "C:/repos"
    elif isdir("D:/repos"):
        repo_dir = "D:/repos"  # change this to your own

    encoding = "850"

    iteminfo_dir = repo_dir + "/eRODev/eRO Client Data/system/itemInfosryx.lub"
    print_resource_names_from_lua(file_dir=iteminfo_dir, encoding=encoding)


# Prints the item id, and its resource name
def print_resource_names_from_lua(file_dir, encoding):
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
    resource_name_line_pattern = '^\s{4,}identifiedResourceName\s{1,}?=\s{1,}?((".{0,}"|\d{1,})|{.{0,}}),?$\n'
    is_resource_name_line = re.compile(resource_name_line_pattern)

    # line that contains the display name of the item
    display_name_line_pattern = '^\s{4,}identifiedDisplayName\s{1,}?=\s{1,}?((".{0,}"|\d{1,})|{.{0,}}),?$\n'
    is_display_name_line = re.compile(display_name_line_pattern)

    item_dict = {}
    current_item_id = None
    with open(file=file_dir, mode="r", encoding=encoding) as lua:
        counter = 0
        for line in lua:
            if is_new_item_line.match(line):
                # if item code is found,
                # extract item code
                current_item_id = re.search(pattern=extract_item_code, string=line).group(0)
                if current_item_id not in item_dict and int(current_item_id) < 1616:
                    # make a new dictionary reference
                    item_dict[current_item_id] = {}
            elif is_resource_name_line.match(line) or is_display_name_line.match(line):
                if int(current_item_id) < 1616:
                    # if this line contains item display or resource name
                    # add that key and value to the current item
                    key_value_list = line.split("=")

                    # key
                    key = key_value_list[0].strip().replace("\n", "")

                    value = key_value_list[1].strip().replace("\n", "").replace("\"", "")
                    if value[-1:] == ",":  # removes trialing comma
                        # if there is a trailing comma, remove it
                        value = value[:-1]

                    # adds key and value to the current item dict
                    item_dict[current_item_id][key] = value
            counter += 1

    print("Parsed " + str(counter) + " lines from Lua.")

    for item_id in item_dict:
        output = str(item_id)
        output += "," + item_dict[item_id]["identifiedDisplayName"]
        output += "," + item_dict[item_id]["identifiedResourceName"]
        print(output)


# Tells the user in the console what file is currently being opened.
def print_opening_dir(file_dir):
    file_dir_split = file_dir.split("/")
    filename = file_dir_split[-1]
    file_path = file_dir_split[:-1]
    print("Opening: " + filename + " | From: " + "/".join(file_path))


main()

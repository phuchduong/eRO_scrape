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

    accname_dir = repo_dir + "/eRODev/eRO Client Data/data/luafiles514/lua files/datainfo/accname.lub"
    print_resource_names_from_lua(file_dir=accname_dir, encoding=encoding)


# Prints the item id, and its resource name
def print_resource_names_from_lua(file_dir, encoding):
    print_opening_dir(file_dir=file_dir)
    ############
    # Patterns #
    ############
    # Begin item match
    new_item_line_pattern = '^\s{1,}\[ACCESSORY_IDs.ACCESSORY_.{1,}\]\s{1,}=\s{1,}".{1,}",$\n'
    is_new_item_line = re.compile(new_item_line_pattern)

    with open(file=file_dir, mode="r", encoding=encoding) as lua:
        counter = 0
        for line in lua:
            if is_new_item_line.match(line):
                # if item code is found,
                # extract item code
                line_split = line.split("=")
                item_alias = line_split[0].split(".ACCESSORY_")[1].replace("]", "").strip()
                item_sprite = line_split[1].replace(",", "").replace("_", "").replace("\"", "").strip()
                print(item_alias + "," + item_sprite)
            counter += 1

    print("Parsed " + str(counter) + " lines from Lua.")


# Tells the user in the console what file is currently being opened.
def print_opening_dir(file_dir):
    file_dir_split = file_dir.split("/")
    filename = file_dir_split[-1]
    file_path = file_dir_split[:-1]
    print("Opening: " + filename + " | From: " + "/".join(file_path))


main()

#!/usr/bin/env python.
'''
    File name: print_tem_names.py
    Date created: January 31, 2017
    Python version: 3.6.1
    Version: 1.0.0
    Purpose:
        Prints the item names from an item_db and an item_info.
    Author: Phuc H Duong
    Original Repo: https://github.com/phuchduong/essencero_restoration
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from os import path, makedirs
import re  # regular expression


# script goes here
def main():
    debug_mode = True
    # Repo folder
    if path.isdir("C:/repos"):
        repo_dir = "C:/repos"
    elif path.isdir("D:/repos"):
        repo_dir = "D:/repos"
    else:
        repo_dir = ""  # change this to your own directory

    # Repos
    server_repo = "/essencera/"
    client_repo = "/eRODev/"

    # Input data files
    # item_db = repo_dir + server_repo + "/db/pre-re/item_db.txt"
    item_db = repo_dir + server_repo + "/db/import-tmpl/item_db.txt"
    item_info = repo_dir + client_repo + "/eRO Client Data/System/itemInfosryx.lub"

    # Builds an output folder if it doesn't exist within the same directory
    # as the executed script.
    out_folder_path = make_output_folder()

    # Output files
    out_filename = "item_names.tsv"

    item_db_names = parse_item_names_from_item_db(
        db_path=item_db,
        debug=debug_mode
    )
    item_info_names = parse_item_names_from_item_info(
        info_path=item_info,
        debug=debug_mode
    )
    print_item_names(
        item_db_names=item_db_names,
        item_info_names=item_info_names,
        out_file_path=out_folder_path + out_filename,
        debug=debug_mode,
    )


# Loads the local file system, else create a new one.
def make_output_folder():
    # Requires import os
    # Get the current file path of the script.
    script_dir = path.dirname(path.realpath(__file__))
    file_system_path = script_dir + "/outputs/"
    system_folder_exists = path.isdir(file_system_path)

    # Creates a system folder if it does not exist.
    if system_folder_exists:
        print("Output folder found...")
    else:
        print("Initializing output folder...")
        # creates a folder called "build_item_info_files" in the script directory
        makedirs(file_system_path)
        print("Created folder: " + file_system_path)

    return(file_system_path)


# Traveres an item_db.txt and gets all item_ids and item names.
def parse_item_names_from_item_db(db_path, debug):
    item_regex = "^\d{3,5},"
    item_db = {}
    is_item = re.compile(item_regex)
    with open(file=db_path, mode="r") as f:
        for line in f:
            if is_item.match(line):
                line_split = line.split(",")
                item_id = int(line_split[0])
                aegis_name = line_split[1]
                rathena_name = line_split[2]
                item_db[item_id] = {
                    "aegis_name": aegis_name,
                    "rathena_name": rathena_name
                }
                if debug:
                    print(str(item_id) + "\t" + aegis_name + "\t" + rathena_name)
    return item_db


# Traveres an item_db.txt and gets all item_ids and item names.
def parse_item_names_from_item_info(info_path, debug):
    item_id_regex = "\[\d{3,5}\]"
    item_display_regex = "^\s{1,}identifiedDisplayName"
    is_item_id = re.compile(item_id_regex)
    is_item_display = re.compile(item_display_regex)
    item_info = {}
    current_id = None
    with open(file=info_path, mode="r", encoding="850") as f:
        for line in f:
            if is_item_id.search(line):
                current_id = int(line.split("[")[1].split("]")[0])
                item_info[current_id] = {}
            if is_item_display.search(line):
                line_split = line.split("=")
                display_name = line_split[1].strip()
                display_name = display_name.split("\"")[1].strip()
                item_info[current_id]["display_name"] = display_name
                if debug:
                    print(str(current_id) + "\t" + item_info[current_id]["display_name"])
    return item_info


# Prints out a TSV of item names using an item_db and an item_info.
# Uses the item_Db to filter the item_info since the into_info is verbose.
def print_item_names(item_db_names, item_info_names, out_file_path, debug):
    f = open(file=out_file_path, mode="w")
    header = "item_id\tdisplay_name\taegis_name\trathena_name\n"
    f.write(header)
    for item_id in item_db_names:
        line = [str(item_id)]
        line.append(item_db_names[item_id]["aegis_name"])
        line.append(item_db_names[item_id]["rathena_name"])
        try:
            line.append(item_info_names[item_id]["display_name"])
        except KeyError:
            print("Missing from item_info: " + str(item_id) + " " + item_db_names[item_id]["rathena_name"])
            pass

        if len(line) == 4:
            line = "\t".join(line)
            line += "\n"
            f.write(line)

    f.close()


main()

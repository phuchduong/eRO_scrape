#!/usr/bin/env python.
'''
    File name: reconcile_iteminfo_with_itemdb.py.py
    Date created: February 2, 2017
    Python version: 3.6.1
    Version: 0.2.0
    Purpose:
        Prints a new item_info from an existing item_info,
        give the details of an item_db.txt.
    Author: Phuc H Duong
    Original Repo: https://github.com/phuchduong/essencero_restoration
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from os import path, makedirs  # Windows file system
import re  # regular expression
import subprocess as sp  # to open files in a text editor as a subprocess


# script goes here
def main():
    debug_mode = False
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


    # Builds an output folder if it doesn't exist within the same directory
    # as the executed script.
    out_folder_path = make_output_folder()

    ero_item_db_path = repo_dir + server_repo + "/db/import-tmpl/item_db.txt"
    ero_item_db = parse_item_names_from_item_db(
        db_path=ero_item_db_path,
        debug=debug_mode
    )

    iro_item_db_path = repo_dir + server_repo + "/db/pre-re/item_db.txt"
    iro_item_db = parse_item_names_from_item_db(
        db_path=iro_item_db_path,
        debug=debug_mode
    )

    # Merge two dictionaries together
    item_db = {**ero_item_db, **iro_item_db}
    print("ero_item_db:\t" + str(len(ero_item_db)) + "\titems found...")
    print("iro_item_db:\t" + str(len(iro_item_db)) + "\titems found...")
    print("combined_db:\t" + str(len(item_db)) + "\titems found...")

    # item infos
    item_info_input_path = repo_dir + client_repo + "/eRO Client Data/System/itemInfosryx.lub"
    item_info_output_path = out_folder_path + "itemInfosryx.lub"
    rename_and_write_item_info(
        item_db=item_db,
        item_info_input_path=item_info_input_path,
        item_info_output_path=item_info_output_path,
        debug=debug_mode,
    )

    # # Opens the new iteminfo.lua and item_db.txt in sublime text
    # program_dir = "C:\Program Files\Sublime Text 3\sublime_text.exe"
    # print("Done... Opening both item_infos in Sublime...")
    # sp.Popen([program_dir, item_info])
    # sp.Popen([program_dir, out_path])


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
    print_opening_dir(file_dir=db_path)
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

    print_opening_dir(file_dir=info_path)
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


# Writes out a new item_db.txt and renames the items from a list of items to rename.
def rename_and_write_item_info(item_db, item_info_input_path, item_info_output_path, debug):
    f_out = open(file=item_info_output_path, mode="w", encoding="850")

    # item id
    item_id_regex = "\[\d{3,5}\]"
    is_item_id = re.compile(item_id_regex)

    # Slot count
    slot_count_regex = "^\s{1,}slotCount\s{1,2}=\s{1,2}\d,"
    is_slot_count = re.compile(slot_count_regex)

    current_id = None
    with open(file=item_info_input_path, mode="r", encoding="850") as f_in:
        for line in f_in:
            # Finds keys that match an existing item_db entry
            if is_item_id.search(line):
                item_id = int(line.split("[")[1].split("]")[0])
                if current_id in item_db:
                    current_id = item_id
                else:
                    current_id = None

            # Only parse line if current_id is an active item_id
            # that exists in the item_db
            if current_id is not None:
                if is_slot_count.match(line):
                    # slot count
                    line_split = line.split("=")
                    line_split[1] = " \"" + item_db["slo"] + "\",\n"
                    line = "=".join(line_split)
                    if debug:
                        print("Renaming " + str(current_id) + ":\t\t" + line)
            f_out.write(line)
    f_out.close()


# Tells the user in the console what file is currently being opened.
def print_opening_dir(file_dir):
    file_dir_split = file_dir.split("/")
    filename = file_dir_split[-1]
    file_path = file_dir_split[:-1]
    print("Opening: " + filename + " | From: " + "/".join(file_path))


# Tells the user how many lines were writte to a file
def print_writing_status(counter, file_dir):
    filename = file_dir.split("/")[-1]
    print("Found... " + str(counter) + " items in " + filename + "\n")


main()

#!/usr/bin/env python.
'''
    File name: reconcile_iteminfo_names_with_itemdb.py
    Date created: February 7, 2017
    Python version: 3.6.1
    Version: 1.0.0
    Purpose:
        Takes the item display name from an item_db and renames all the items
        in an item_db
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

    # Builds an output folder if it doesn't exist within the same directory
    # as the executed script.
    out_folder_path = make_output_folder()

    # parse item info
    item_info_input_path = repo_dir + client_repo + "/eRO Client Data/System/itemInfosryx.lub"
    item_info_db = parse_item_names_from_item_info(
        item_info_input_path=item_info_input_path,
        debug=debug_mode,
    )

    # ero_item_db_path_in = repo_dir + server_repo + "/db/import-tmpl/item_db.txt"
    # ero_item_db_path_out = out_folder_path + "/item_db.txt"
    # ero_log_path = out_folder_path + "/item_db_rename.txt"
    # write_out_item_db(
    #     item_info_db=item_info_db,
    #     db_path_in=ero_item_db_path_in,
    #     db_path_out=ero_item_db_path_out,
    #     log_path=ero_log_path,
    #     debug=debug_mode
    # )

    iro_item_db_path_in = repo_dir + server_repo + "/db/pre-re/item_db.txt"
    iro_item_db_path_out = out_folder_path + "/item_db.txt"
    iro_log_path = out_folder_path + "/item_db_rename.txt"
    write_out_item_db(
        item_info_db=item_info_db,
        db_path_in=iro_item_db_path_in,
        db_path_out=iro_item_db_path_out,
        log_path=iro_log_path,
        debug=debug_mode
    )

    # Opens the new iteminfo.lua and item_db.txt in sublime text
    program_dir = "C:\Program Files\Sublime Text 3\sublime_text.exe"
    print("Done... Opening both item_infos in Sublime...")
    sp.Popen([program_dir, iro_item_db_path_in])
    sp.Popen([program_dir, iro_item_db_path_out])
    sp.Popen([program_dir, iro_log_path])


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
def write_out_item_db(item_info_db, db_path_in, db_path_out, log_path, debug):
    f_out = open(file=db_path_out, mode="w")
    f_log = open(file=log_path, mode="w")
    item_regex = "^\d{3,5},"
    is_item = re.compile(item_regex)
    with open(file=db_path_in, mode="r") as f_in:
        print_opening_dir(file_dir=db_path_in)
        for line in f_in:
            if is_item.match(line):

                # Parse item line

                line_split = line.split(",")
                # 0  ID
                item_id = int(line_split[0])
                if item_id in item_info_db:
                    display_name = item_info_db[item_id]
                    display_name_aegis = display_name.replace(" ", "_")
                    # 1  AegisName
                    aegis_name = line_split[1]
                    # 2  Name
                    rathena_name = line_split[2]
                    # 3  Type
                    # 4  Buy
                    # 5  Sell
                    # 6  Weight
                    # 7  ATK[:MATK]
                    # 8  DEF
                    # 9  Range
                    # 10 Slots
                    # 11 Job
                    # 12 Class
                    # 13 Gender
                    # 14 Loc
                    # 15 wLV
                    # 16 eLV[:maxLevel]
                    # 17 Refineable
                    # 18 View
                    # 19 { Script }
                    # 20 { OnEquip_Script }
                    # 21 { OnUnequip_Script }
                    if(display_name != rathena_name or aegis_name != display_name_aegis):
                        line_split[1] = display_name_aegis
                        line_split[2] = display_name
                        new_line = ",".join(line_split)
                        try:
                            f_out.write(new_line)

                            if(display_name != rathena_name):
                                log_line = str(item_id) + " renaming @item_info display name from " + rathena_name + " to " + display_name + ".\n"
                                f_log.write(log_line)
                            if(aegis_name != display_name_aegis):
                                log_line = str(item_id) + " renaming @item_info lookup name from " + aegis_name + " to " + display_name_aegis + ".\n"
                                f_log.write(log_line)
                        except UnicodeEncodeError:
                            f_out.write(line)
                    else:
                        f_out.write(line)
                else:
                    f_out.write(line)
            else:
                f_out.write(line)
    f_out.close()
    f_log.close()


# Parse an item_info and returns a dictionary.
def parse_item_names_from_item_info(item_info_input_path, debug):
    # item id
    item_id_regex = "\[\d{3,5}\]"
    is_item_id = re.compile(item_id_regex)

    # slot count
    is_display_name_regex = "^\t{2}identifiedDisplayName\s{1,2}=\s{1,2}\".{0,}\"\,\n"
    is_display_name = re.compile(is_display_name_regex)

    item_info_db = {}

    current_id = None
    with open(file=item_info_input_path, mode="r", encoding="850") as f_in:
        print_opening_dir(file_dir=item_info_input_path)
        for line in f_in:
            if is_item_id.search(line):
                item_id = int(line.split("[")[1].split("]")[0])
                current_id = item_id
                item_info_db[item_id] = ""
            if is_display_name.match(line):
                # Updating slot count
                line_split = line.split("=")
                display_name = line_split[1].strip()[1:-2]  # removes quotes and comma
                item_info_db[current_id] = display_name.strip()

    f_in.close()
    print_writing_status(counter=len(item_info_db), file_dir=item_info_input_path)
    return item_info_db


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

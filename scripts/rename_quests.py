#!/usr/bin/env python.
'''
    File name: rename_quests.py
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
    practice_repo = "/essencero_restoration/scripts/outputs/practice/essencera/"
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

    script_conf_path = repo_dir + server_repo + "/npc/scripts_custom.conf"
    filenames = get_quest_filenames(
        script_conf=script_conf_path,
        debug=debug_mode,
    )

    change_log_output_path = out_folder_path + "quest_files_renamed.txt"
    quest_folder = practice_repo + "/npc/custom"
    rename_quest_files(
        script_conf=script_conf_path,
        quest_folder=quest_folder,
        quest_filenames=filenames,
        log_file=change_log_output_path,
        debug=debug_mode,
    )

    # Opens the new iteminfo.lua and item_db.txt in sublime text
    program_dir = "C:\Program Files\Sublime Text 3\sublime_text.exe"
    print("Done... Opening both item_infos in Sublime...")
    sp.Popen([program_dir, change_log_output_path])


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


# scans a quest conf for quest and renames quest files based upon the final item.
def get_quest_filenames(script_conf, debug):
    start = "// Old Red Box Script Begin Scan\n"
    stop = "// Old Red Box Script End Scan\n"
    filenames = []
    scan = False
    with open(file=script_conf, mode="r") as f_in:
        for line in f_in:
            if line == start:
                scan = True
            if line == stop:
                scan = False
            if scan is True:
                if line.startswith("npc:"):
                    filename = line.split("/")[-1]
                    filenames.append(filename)
    return filenames

# scans a quest conf for quest and renames quest files based upon the final item.
def rename_quest_files(script_conf, quest_folder, log_file, debug):
    start = "// Old Red Box Script Begin Scan\n"
    stop = "// Old Red Box Script End Scan\n"
    filenames = []
    scan = False
    with open(file=script_conf, mode="r") as f_in:
        for line in f_in:
            if line == start:
                scan = True
            if line == stop:
                scan = False
            if scan is True:
                if line.startswith("npc:"):
                    filename = line.split("/")[-1]
                    filenames.append(filename)
    return filenames

# Traveres an item_db.txt and gets all item_ids and item names.
def parse_item_names_from_item_db(db_path, debug):
    item_regex = "^\d{3,5},"
    item_db = {}
    is_item = re.compile(item_regex)
    print_opening_dir(file_dir=db_path)
    with open(file=db_path, mode="r") as f:
        for line in f:
            if is_item.match(line):
                # Parse item line

                line_split = line.split(",")
                # 0  ID
                item_id = int(line_split[0])
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
                slot_count = line_split[10]
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
                item_db[item_id] = {
                    "aegis_name": aegis_name,
                    "slot_count": slot_count,
                    "rathena_name": rathena_name,
                }
                if debug:
                    print(str(item_id) + "\t" + aegis_name + "\t" + rathena_name)
    return item_db

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

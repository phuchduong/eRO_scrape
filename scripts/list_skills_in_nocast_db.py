#!/usr/bin/env python.
'''
    File name: list_skills_in_nocast_db.py
    Date created: February 7, 2017
    Python version: 3.6.1
    Version: 1.0.0
    Purpose:
        Takes on a skill_db to derive skill name and skill id. Then uses
        that information to ellaborate skill_ids inside of a skill_nocast_db.txt.
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
    skill_db_in_path = repo_dir + server_repo + "/db/pre-re/skill_db.txt"
    skill_db = parse_skill_db(
        item_info_input_path=skill_db_in_path,
        debug=debug_mode,
    )

    no_castdb_in = repo_dir + server_repo + "/db/pre-re/skill_nocast_db.txt"
    no_castdb_out = out_folder_path + "/skill_nocast_db.txt"
    write_out_skill_nocast_db(
        skill_db=skill_db,
        db_path_in=no_castdb_in,
        db_path_out=no_castdb_out,
        debug=debug_mode
    )

    # Opens the new iteminfo.lua and item_db.txt in sublime text
    program_dir = "C:\Program Files\Sublime Text 3\sublime_text.exe"
    print("Done... Opening both item_infos in Sublime...")
    sp.Popen([program_dir, no_castdb_in])
    sp.Popen([program_dir, no_castdb_out])


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


# Traveres an skill_nocast_db.txt and ellaborates on the skill name as commentary
def write_out_skill_nocast_db(skill_db, db_path_in, db_path_out, debug):
    f_out = open(file=db_path_out, mode="w")
    skill_nocast_regex = "^(////)*(//// )*\d{1,5},\d{1,4}"
    is_skill_nocast_line = re.compile(skill_nocast_regex)
    with open(file=db_path_in, mode="r") as f_in:
        print_opening_dir(file_dir=db_path_in)
        for line in f_in:
            if is_skill_nocast_line.match(line):
                print(line)
                # Parse item line
                line = line.split("\t")[0].strip()
                skill_id = int(line.split(",")[0])

                line += "\t// " + skill_db[skill_id] + "\n"
            f_out.write(line)


# Takes in skill_db, parses it for skill name and id.
def parse_skill_db(item_info_input_path, debug):
    skill_db = {}
    with open(file=item_info_input_path, mode="r") as f_in:
        skill_regex = "^\d{1,5}\,"
        is_skill_line = re.compile(skill_regex)
        print_opening_dir(file_dir=item_info_input_path)
        for line in f_in:
            if is_skill_line.match(line) and line.count(",") == 17:
                line_split = line.split(",")
                # 0   id
                # 1   range
                # 2   hit
                # 3   inf
                # 4   element
                # 5   nk
                # 6   splash
                # 7   max
                # 8   list_num
                # 9   castcancel
                # 10  cast_defence_rate
                # 11  inf2
                # 12  maxcount
                # 13  skill_type
                # 14  blow_count
                # 15  inf3
                # 16  name
                # 17  description
                skill_id = int(line_split[0])
                skill_name = line_split[16]
                skill_desc = line_split[17].split("//")[0]
                skill_db[skill_id] = skill_name.strip() + "\t" + skill_desc.strip()
    print_writing_status(counter=len(skill_db), file_dir=item_info_input_path)
    return skill_db


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

#!/usr/bin/env python.
'''
    File name: build_iteminfo.py
    Date created: January 13, 2018
    Python version: 3.6.1
    Purpose:
        Generates a new:
            1. iteminfo.lua
            2. item_db.txt (s)
    Author: Phuc H Duong
    Website: phuchduong.io
    Github: https://github.com/phuchduong
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import os


# Edits an iteminfo by using an item_db.
def main():

    get_file_system()


# Loads the local file system, else create a new one.
def get_file_system():
    # Requires import os
    # Get the current file path of the script.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_system_path = script_dir + "\\build_iteminfo_files"
    system_folder_exists = os.path.isdir(file_system_path)

    # Creates a system folder if it does not exist.
    if system_folder_exists:
        print("Loading system folder contents...")
    else:
        print("Initializing system folder...")
        # creates a folder called "build_item_info_files" in the script directory
        os.makedirs(file_system_path)
        print("Created folder: " + file_system_path)

    # Loads the local files.
    conf_file_dir = file_system_path + "\\config.json"
    conf_file_exists = os.path.exists(conf_file_dir)
    if conf_file_exists:
        print("Loading config file...")
    else:
        print("Generating config file...")


main()

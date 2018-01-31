#!/usr/bin/env python.
'''
    File name: print_tem_names.py
    Date created: January 31, 2017
    Python version: 3.6.1
    Version: 0.0.0
    Purpose:
        Prints the item names from an item_db and an item_info.
    Author: Phuc H Duong
    Original Repo: https://github.com/phuchduong/essencero_restoration
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from os.path import isdir   # checks to see if a folder exists
import re  # regular expression


# script goes here
def main():
    # Repo folder
    if isdir("C:/repos"):
        repo_dir = "C:/repos"
    elif isdir("D:/repos"):
        repo_dir = "D:/repos"
    else:
        repo_dir = ""  # change this to your own directory

    # Repos
    server_repo = "/essencera/"
    client_repo = "/eRODev/"

    # Input data files
    item_db = repo_dir + server_repo + "/db/pre-re/item_db.txt"
    item_info = repo + client_repo + "/eRO Client Data/System/itemInfosryx.lub"

    # Builds an output folder if it doesn't exist within the same directory
    # as the executed script.
    out_folder_path = make_output_folder()

    # Output files
    out_filename = "item_names.tsv"


# Loads the local file system, else create a new one.
def make_output_folder():
    # Requires import os
    # Get the current file path of the script.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_system_path = script_dir + "/outputs/"
    system_folder_exists = os.path.isdir(file_system_path)

    # Creates a system folder if it does not exist.
    if system_folder_exists:
        print("Output folder found...")
    else:
        print("Initializing output folder...")
        # creates a folder called "build_item_info_files" in the script directory
        os.makedirs(file_system_path)
        print("Created folder: " + file_system_path)

    return(file_system_path)


main()

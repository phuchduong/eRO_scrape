#!/usr/bin/env python.
'''
    File name: generate_dyes_for_valk_helms.py
    Date created: December 4, 2017
    Python version: 3.6.1
    Purpose:
        Prints a specific line in a text file.
    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from os.path import isdir   # checks to see if a folder exists


def main():

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
    item_id = 63267
    print_line_from_file(file_dir=iteminfo_dir, line_num=item_id, encoding="850")
    print_line_from_file(file_dir=iteminfo_dir, line_num=item_id + 1, encoding="850")
    print_line_from_file(file_dir=iteminfo_dir, line_num=item_id + 13, encoding="850")


# prints the specific line of a file
def print_line_from_file(file_dir, line_num, encoding):
    with open(file=file_dir, mode="r", encoding=encoding) as f:
        counter = 0
        for line in f:
            counter += 1
            if counter == line_num:
                print("Line Number " + str(counter) + ":" + line)


main()

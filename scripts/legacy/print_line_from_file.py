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


def main(codec):

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
    item_id = 36167
    print_line_from_file(file_dir=iteminfo_dir, line_num=item_id, encoding=codec)
    print_line_from_file(file_dir=iteminfo_dir, line_num=item_id + 1, encoding=codec)
    print_line_from_file(file_dir=iteminfo_dir, line_num=item_id + 13, encoding=codec)


# prints the specific line of a file
def print_line_from_file(file_dir, line_num, encoding):
    with open(file=file_dir, mode="r", encoding=encoding) as f:
        counter = 0
        for line in f:
            counter += 1
            if counter == line_num:
                print("Line Number " + str(counter) + ":" + line)


codecs = [
    "cp850",
    "cp1252",
    "latin_1",
    "iso8859_3",
    "iso8859_15",
    "cp437",
    "cp1256",
    "cp1257",
    "iso8859_2",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_13",
    "iso8859_14",
    "cp1250",
    "cp1251",
    "cp866",
    "koi8_r",
    "koi8_u",
    "cp1253",
    "cp1255",
    "cp1254",
    "cp1258",
]
works = []
for codec in codecs:
    try:
        print("=====================================")
        print("Trying Codec:" + codec)
        print("=====================================")
        main(codec=codec)
        works.append(codec)
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print("--------------------------------")
        print("Error in codec: " + codec + ". Error: " + str(e))
        print("--------------------------------")
        pass
print("--------------------------------")
print("Script Finished-----------------")
print("These codecs work:")
print(",".join(works))

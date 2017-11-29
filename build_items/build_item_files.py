#!/usr/bin/env python.
'''
    File name: build_item_files.py
    Date created: November 29, 2017
    Python version: 3.6.1
    Purpose:
        Rebuild the eRO item database by...
        - Merge the two webscraped TSV files together obtained from:
            - tamsinwhitfield
            - web archive (the way back machine)
        - Join with and insert into the item_db.txt
        - Join with and insert into iteminfo
        - Validate sprite files

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''

###############
# file system #
###############

# your repo directory should look like this
#
# /repo root (essencero_restoration)
#   /web_scrape_tamsinwhitfield
#       /old_essence_item_db.txt
#   /web_scrape_web_archive
#       /item_db_web_archive.tsv
repo_dir = "D:/repos/essencero_restoration"  # change this to your own

# data webscraped from tamsinwhitfield
tw_dir = "/web_scrape_tamsinwhitfield/old_essence_item_db.txt"  # tab deliminated

# data webscraped from web archive (the way back machine)
wa_dir = "/web_scrape_web_archive/item_db_web_archive.tsv"


##################
# old eRO fields #
##################

# List of item ids of items that are being left behind and not integrated into the new server.
# Treatment: These item should be skipped during the merge.
old_ero_ignore_list = [
    20631,  # Drooping Aria
    20522,  # Drooping Aria Stark
    20524,  # Drooping Biomaster
    20194,  # Drooping Cebalrai
    20521,  # Drooping Doctor Wyrd
    20568,  # Drooping Eike
    20525,  # Drooping Eileithyia
    20633,  # Drooping Faustus
    20154,  # Drooping Gazel
    20557,  # Drooping Mokona
    20755,  # Drooping Mulder
    20128,  # Drooping Neko
    20508,  # Drooping Nora Stark
    20634,  # Drooping Okale
    20754,  # Drooping Paradox924X
    20165,  # Drooping Pikachu
    20635,  # Drooping Praetor
    20558,  # Drooping Saproling
    20506,  # Drooping Skwipe
    20576,  # Drooping Super Scope
    20513,  # Drooping Takara
    20507,  # Drooping Tony Stark
    20514,  # Drooping Vhaidra
    20552,  # Drooping Windii
    20517,  # Drooping Xackery
    20799,  # Drooping Yami
    20502,  # Drooping Yosh
    20581,  # Drooping Zhao
]
old_ero_itemid_list = []
old_ero_item_dict = {}

# Read in tamsinwhitfield as a dictionary by item_id as the key, remaining line as values
tw_dict = {}
with open(file=repo_dir + tw_dir, mode="r") as tw:
    tw_header = tw.readline()  # header
    for line in tw:            # body
        item_id = line.split("\t")[0]
        item_body = line[len(item_id) + 1:]  # grabs everything after the item_id
        tw_dict[item_id] = item_body

# Read in web archive as a dictionary by item_id as the key, remaining line as values
wa_dict = {}
print(repo_dir + wa_dir)
with open(file=repo_dir + wa_dir, mode="r") as wa:
    wa_header = wa.readline()
    for line in wa:            # body
        item_id = line.split("\t")[0]
        item_body = line[len(item_id) + 1:]  # grabs everything after the item_id
        wa_dict[item_id] = item_body

# Combine tamsinwhitfield and web archive lists, filtering ignored items

# build a master key list of item ids in both lists, and remove the ignore list
both_exists = set(tw_dict.keys()).intersection(wa_dict.keys())  # finds items that exist in both lists
both_exists = [int(x) for x in both_exists]  # converts all elements to integer from string
both_exists = [x for x in both_exists not in old_ero_ignore_list]  # filters items in ignore list
both_exists = sorted(both_exists)  # sorts keys
for item in both_exists:
    print(item)
tw_exclusive = []
wa_exclusive = []

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
old_aero_ignore_list = [
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

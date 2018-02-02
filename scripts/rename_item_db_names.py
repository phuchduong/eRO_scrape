#!/usr/bin/env python.
'''
    File name: rename_item_db_names.py
    Date created: February 2, 2017
    Python version: 3.6.1
    Version: 1.0.0
    Purpose:
        Rename the item names from an item_db
        and standardizes their forms together.
    Author: Phuc H Duong
    Original Repo: https://github.com/phuchduong/essencero_restoration
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from os import path, makedirs
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

    # Input data files
    item_db_in_dir = repo_dir + server_repo + "/db/import-tmpl/item_db.txt"

    # Builds an output folder if it doesn't exist within the same directory
    # as the executed script.
    out_folder_path = make_output_folder()

    # Gets the list of items to rename
    rename_list = get_rename_list()

    # Output files
    db_path_out = out_folder_path + "item_db.txt"
    rename_and_write_item_db(
        rename_list=rename_list,
        db_path_in=item_db_in_dir,
        db_path_out=db_path_out,
        debug=debug_mode,
    )

    # Opens the new iteminfo.lua and item_db.txt in sublime text
    program_dir = "C:\Program Files\Sublime Text 3\sublime_text.exe"
    sp.Popen([program_dir, item_db_in_dir])
    sp.Popen([program_dir, db_path_out])


# List of items to rename.
def get_rename_list():
    return {
        45042: "Bat Mask",
        45048: "Black Beret",
        45049: "Blue Beret",
        45050: "Brown Beret",
        45051: "Pink Beret",
        45052: "Purple Beret",
        45053: "Red Beret",
        45054: "White Beret",
        45055: "Yellow Beret",
        45056: "Butterfly Net",
        45059: "Black Winter Hat",
        45060: "Black Wind Milestone",
        45065: "Blue Neck Tie",
        45066: "Black Tailed Ribbon",
        45068: "Blue Robe",
        45069: "Blue Wind Milestone",
        45070: "Blue Bandana Black",
        45071: "Blue Bandana Brown",
        45072: "Blue Bandana Green",
        45073: "Blue Bandana Pink",
        45074: "Blue Bandana Purple",
        45075: "Blue Bandana Red",
        45076: "Blue Bandana White",
        45077: "Blue Bandana Yellow",
        45084: "Blue Tailed Ribbon",
        45088: "Brazilian Flag Hat",
        45089: "Brown Winter Hat",
        45090: "Brown Wind Milestone",
        45092: "Brown Helm of Darkness",
        45093: "Brown Neck Tie",
        45094: "Brown Tailed Ribbon",
        45099: "Blue Bubble Gum",
        45100: "Green Bubble Gum",
        45101: "Pink Bubble Gum",
        45125: "Drooping Choco",
        45138: "Creepy Pumpkin",
        45141: "Cupcake Hat",
        45145: "Deity Mask",
        45147: "Deviling Backpack",
        45158: "Dragoon Wings",
        45179: "Dunce Hat",
        45183: "Empty Eye Socket",
        45184: "Enchanced Shackles",
        45185: "Exodus Wing",
        45186: "Lilika's Butterfly Wings",
        45187: "Fairy Egg",
        45190: "Black Feather Beret",
        45191: "Brown Feather Beret",
        45192: "Green Feather Beret",
        45193: "Pink Feather Beret",
        45194: "Purple Feather Beret",
        45195: "White Feather Beret",
        45196: "Yellow Feather Beret",
        45197: "Feather Mask",
        45198: "Female Smith Pack",
        45199: "Female Super Novice Pack",
        45200: "Ghost of Fallen Bishop",
        45202: "Final Sacrifice Hat",
        45207: "Flower Earrings",
        45210: "Flying Angeling",
        45211: "Freya Crescent's Hat",
        45213: "Frog Hood",
        45215: "Fur Mantle",
        45216: "Black Gangster Scarf",
        45217: "Blue Gangster Scarf",
        45218: "Brown Gangster Scarf",
        45219: "Green Gangster Scarf",
        45220: "Pink Gangster Scarf",
        45221: "Purple Gangster Scarf",
        45222: "White Gangster Scarf",
        45223: "Yellow Gangster Scarf",
        45224: "Gem Bracelet",
        45225: "Gem Necklace",
        45227: "Giga Pudding",
        45241: "Gold Cup",
        45243: "Gold Poring Necklace",
        45244: "Green Winter Hat",
        45245: "Green Wind Milestone",
        45246: "Green Butterfly Wings",
        45248: "Green Nature Wings",
        45249: "Green Neck Tie",
        45252: "Green Tailed Ribbon",
        45255: "Gryphon Item",
        45256: "Gryphon Hat",
        45259: "Gypsy Tiara",
        45261: "Halloween Box",
        45262: "Hane Ribbon",
        45266: "Heart Phones",
        45269: "Heart Wings",
        45273: "Arch Angeling Hat",
        45278: "Holy Wing",
        45280: "Hunny",
        45281: "Huntercap Blue",
        45283: "Drooping Hylozoist",
        45284: "Icecream Cone",
        45286: "Im Gay",
        45287: "Incubus Doll",
        45303: "Black Kawaii Ribbon",
        45304: "Blue Kawaii Ribbon",
        45305: "Brown Kawaii Ribbon",
        45306: "Green Kawaii Ribbon",
        45307: "Pink Kawaii Ribbon",
        45308: "Purple Kawaii Ribbon",
        45309: "White Kawaii Ribbon",
        45310: "Yellow Kawaii Ribbon",
        45312: "Kid's Letter",
        45314: "Drooping Kikki",
        45316: "Lala's Hat",
        45322: "Light Blue Wind Milestone",
        45326: "Sailor Scout's Moon Locket",
        45328: "Love eRO",
        45331: "Black Magic Eyes",
        45332: "Blue Magic Eyes",
        45333: "Brown Magic Eyes",
        45334: "Green Magic Eyes",
        45335: "Pink Magic Eyes",
        45336: "Red Magic Eyes",
        45337: "White Magic Eyes",
        45338: "Yellow Magic Eyes",
        45340: "Majoras Mask",
        45341: "Male Smith Pack",
        45342: "Male Super Novice Pack",
        45346: "Metaling Party Hat",
        45348: "Mini Holy Wings",
        45350: "Mushroom Kingdom Crown",
        45354: "Neko Cookie",
        45361: "Stack of Pancakes",
        45366: "Peco Peco Wing",
        45368: "Phoenix Wings",
        45372: "Drooping Pikachu",
        45374: "Pink Butterfly Wings",
        45375: "Pink Hat",
        45376: "Pink Helm of Darkness",
        45377: "Pink Neck Tie",
        45381: "Poring Envelope",
        45383: "Poring Party Hat",
        45385: "Poring Rucksack",
        45386: "Drooping Praetor",
        45389: "Purple Wind Milestone",
        45390: "Purple Butterfly Wings",
        45391: "Purple Hat",
        45392: "Purple Helm of Darkness",
        45393: "Purple Neck Tie",
        45395: "Purple Tailed Ribbon",
        45396: "Shadow Arrow Quiver",
        45397: "Crystal Arrow Quiver",
        45398: "Earth Arrow Quiver",
        45399: "Wind Arrow Quiver",
        45400: "Immaterial Arrow Quiver",
        45401: "Holy Arrow Quiver",
        45402: "Poison Arrow Quiver",
        45403: "Fire Arrow Quiver",
        45404: "Rare Candy",
        45405: "Randgris Helmet",
        45408: "Red Winter Hat",
        45409: "Black Redbonnet",
        45410: "Blue Redbonnet",
        45411: "Brown Redbonnet",
        45412: "Green Redbonnet",
        45413: "Pink Redbonnet",
        45414: "Purple Redbonnet",
        45415: "White Redbonnet",
        45416: "Yellow Redbonnet",
        45419: "Red Helm of Darkness",
        45420: "Red Neck Tie",
        45422: "Little Red Riding Hood",
        45426: "Ribbon Wizard Hat",
        45430: "Blue Romantic Flower",
        45431: "Purple Romantic Flower",
        45432: "Red Romantic Flower",
        45437: "Sapphire Earrings",
        45440: "Sarasand Kingdom Crown ",
        45443: "Shedinja Halo",
        45444: "Shedinja Mask",
        45445: "Shedinja Wings",
        45446: "Shinobi Helm",
        45447: "Fang of Skoll",
        45453: "Snowflake Ring",
        45458: "Squatting Drops",
        45459: "Squatting Marin",
        45460: "Squatting Poporing",
        45461: "Plumber's Stash",
        45472: "Teddy Bear Ears",
        45473: "Tengu Mask",
        45482: "Twin Swords",
        45483: "U Mad",
        45485: "United Cap",
        45487: "Valentines Ribbon Hat",
        45489: "White Butterfly Wings",
        45494: "Vote Post",
        45498: "White Winter Hat",
        45499: "White Wind Milestone",
        45501: "White Hat",
        45502: "White Helm of Darkness",
        45503: "White Neck Tie",
        45504: "White Tailed Ribbon",
        45506: "Why So Serious",
        45507: "Peco Peco Ears",
        45508: "Wizard Beard",
        45509: "Wooper Hat",
        45513: "Yellow Winter Hat",
        45514: "Yellow Wind Milestone",
        45515: "Yellow Butterfly Wings",
        45516: "Yellow Helm of Darkness",
        45517: "Yellow Neck Tie",
        45518: "Yellow Quiz Hat",
        45519: "Yellow Tailed Ribbon",
        45564: "2b Mask",
        46015: "Level 1 Donor Token",
        46016: "Level 2 Donor Token",
        46017: "Mystery Headgear Envelope",
        46310: "Individual Guild Package",
        46311: "Guild Package 2a",
        46312: "Guild Package 2b",
        46313: "Guild Package 1a",
        51302: "Snowbunny Pokeball",
        51303: "Atroce Pokeball",
        51304: "Doppelganger Pokeball",
        51305: "Drake Pokeball",
        51306: "Eddga Pokeball",
        51307: "Gloom Under Night Pokeball",
        51308: "Golden Thief Bug Pokeball",
        51309: "Ifrit Pokeball",
        51310: "Mistress Pokeball",
        51311: "Moonlight Flower Pokeball",
        51312: "Osiris Pokeball",
        51313: "Pharaoh Pokeball",
        51314: "Stormy Knight Pokeball",
        51315: "Tao Gunka Pokeball",
        51316: "Turtle General Pokeball",
        51317: "Valkyrie Randgris Pokeball",
        51318: "Am Mut Pokeball",
        51319: "Cat O Nine Tails Pokeball",
        51320: "Cecil Damon Pokeball",
        51321: "Deviace Pokeball",
        51322: "Eremes Guile Pokeball",
        51323: "Giant Hornet Pokeball",
        51324: "Howard Alt-Eisen Pokeball",
        51325: "Jakk Pokeball",
        51326: "Kathryne Keyron Pokeball",
        51327: "Margaretha Solin Pokeball",
        51328: "Mavka Pokeball",
        51329: "Seyren Windsor Pokeball",
        51330: "Skeleton General Pokeball",
        51331: "Teddy Bear Pokeball",
        51332: "Tengu Pokeball",
        51333: "Zombie Master Pokeball",
        51334: "Antonio Pokeball",
        51335: "Christmas Jakk Pokeball",
        51336: "Garden Keeper Pokeball",
        51337: "Garden Watcher Pokeball",
        51338: "Earth Crystal Pokeball",
        51339: "Fire Crystal Pokeball",
        51340: "Golden Savage Pokeball",
        51341: "Water Crystal Pokeball",
        51342: "Wind Crystal Pokeball",
    }


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


# Writes out a new item_db.txt and renames the items from a list of items to rename.
def rename_and_write_item_db(rename_list, db_path_in, db_path_out, debug):
    f_out = open(file=db_path_out, mode="w")

    item_regex = "^\d{3,5},"
    is_item_id = re.compile(item_regex)
    with open(file=db_path_in, mode="r") as f_in:
        for line in f_in:
            if is_item_id.search(line):
                line_split = line.split(",")
                item_id = int(line_split[0])
                if item_id in rename_list:
                    # rename the item
                    item_name = rename_list[item_id]
                    aegis_name = item_name.replace("  ", " ").replace(" ", "_")
                    line_split[2] = item_name
                    line_split[1] = aegis_name
                    renamed_line = ",".join(line_split)
                    f_out.write(renamed_line)
                else:
                    f_out.write(line)
            else:
                f_out.write(line)
    f_out.close()


main()

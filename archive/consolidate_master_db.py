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
import re  # regular expression
from os.path import isdir   # checks to see if a folder exists


def main():
    # for a list of valid codecs:
    #     essencero_restoration\Lua Codecs.xlsx
    # 437 is english codec
    encoding = "437"

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

    # data webscraped from tamsinwhitfield
    tw_dir = repo_dir + "/essencero_restoration/web_scrape_tamsinwhitfield/old_essence_item_db.txt"  # tab deliminated

    # data webscraped from web archive (the way back machine)
    wa_dir = repo_dir + "/essencero_restoration/web_scrape_web_archive/item_db_web_archive.tsv"

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

    master_db = {}

    ######################
    # tamsinwhitfield db #
    ######################
    # Read in tamsinwhitfield as a dictionary by item_id as the key, remaining line as values
    # Ignores any item in the ignore list.
    # with open(file=tw_dir, mode="r") as tw:
    #     print_opening_dir(file_dir=tw_dir)
    #     tw_header = tw.readline()  # header
    #     tw_dict = parse_item_scrape_tsv(file_reader=tw, ignore_list=old_ero_ignore_list)
    #     print_writing_status(counter=len(tw_dict), file_dir=tw_dir)

    ##################
    # web archive db #
    ##################
    # Read in webarchive as a dictionary by item_id as the key, remaining line as values
    # Ignores any item in the ignore list.
    # with open(file=wa_dir, mode="r") as wa:
    #     print_opening_dir(file_dir=wa_dir)
    #     wa_header = wa.readline()  # header
    #     wa_dict = parse_item_scrape_tsv(file_reader=wa, ignore_list=old_ero_ignore_list)
    #     print_writing_status(counter=len(tw_dict), file_dir=wa_dir)

    #########################
    # reborn item_db custom #
    #########################
    reborn_item_db_dir = repo_dir + "/eRODev/rAthena Files/db/import/ero_item_db/item_db.txt"
    master_db = parse_item_db(file_dir=reborn_item_db_dir, item_db=master_db)

    ########################
    # reborn item_info lua #
    ########################
    # parses ero iteminfo lua file into a python dictionary
    existing_reborn_lua_dir = repo_dir + "/eRODev/eRO Client Data/system/itemInfosryx.lub"
    existing_reborn_lua = parse_item_info_lua(
        file_dir=existing_reborn_lua_dir,
        item_dict=master_db,
        encoding=encoding)
    master_db = existing_reborn_lua["mid"]

    #############################
    # pre-renewal item_info lua #
    #############################
    # # parses pre-renewal iteminfo lua file into a python dictionary
    # old_item_info_lua_prerenewal = repo_dir + "/eRODev/eRO Client Data/data/luafiles514/lua files/datainfo/pre_re_itemInfo.lua"
    # prerenewal_lua = parse_item_info_lua(file_dir=old_item_info_lua_prerenewal, encoding=encoding)
    # # sees if the new lua has anythign that the old lua lacks
    # for item_id in prerenewal_lua["mid"]:
    #     if item_id not in existing_reborn_lua["mid"]:
    #         print("base lua missing item id: " + str(item_id))

    ###########
    # outputs #
    ###########
    write_dict_to_tsv(
        file_dir=repo_dir + "/eRODev/work in progress/master_db.tsv",
        item_dict=master_db,
        encoding=encoding)

    # writes the item lua to a tsv
    write_dict_to_tsv(
        file_dir=repo_dir + "/eRODev/eRO Client Data/System/new_itemInfosryx.tsv",
        item_dict=existing_reborn_lua["mid"],
        encoding=encoding)

    # Writes new lua to file
    new_lua_dir = repo_dir + "/eRODev/eRO Client Data/system/new_itemInfosryx.lub"
    write_lua_items_to_lua(file_dir=new_lua_dir, lua_parts=existing_reborn_lua, encoding=encoding)


# Parses a TSV and returns a dictionary.
# Grabs the first item in the TSV on each line as the key, converts
#   key to integer.
# The remaining line becomes the value of the key.
# Ex. "a/tb/tc/td/te/t\n" input would return
# {
#   "a": "b/tc/td/te/t\n"
# }
# Takes in a list of keys to ignore and skip
def parse_item_scrape_tsv(file_reader, ignore_list):
    tsv_dict = {}
    for line in file_reader:  # body
        try:
            item_id = int(line.split("\t")[0])
        except ValueError:
            item_id = int(line.split("    ")[0])
        if item_id not in ignore_list:
            # skip items in the ignore list
            item_body = line[len(str(item_id)) + 1:]  # grabs everything after the item_id
            tsv_dict[item_id] = item_body
    return tsv_dict


# Parses an iteminfo lua and returns a 3 element dictionary whoses keys are
# beg, mid, and end.
# beg is the begining of the file
# mid is the data structure in the middle of the file as a dictionary
# end is the remaining code in the file after the data structure
def parse_item_info_lua(file_dir, item_dict, encoding):
    print_opening_dir(file_dir=file_dir)
    ############
    # Patterns #
    ############
    # Begin item match
    new_item_line_pattern = "^\s{4,}\[\d{3,5}]\s{1,}?=\s{1,}?{$\n"
    is_new_item_line = re.compile(new_item_line_pattern)

    # 3~5 digit item code
    item_code_pattern = "\d{3,5}"
    extract_item_code = re.compile(item_code_pattern)

    # line that contains key value pairs
    key_value_line_pattern = '^\s{4,}\w{1,}\s{1,}?=\s{1,}?((".{0,}"|\d{1,})|{.{0,}}),?$\n'
    is_key_value_line = re.compile(key_value_line_pattern)

    # line that starts a multi line embedded object in the lua object
    multi_line_embed_key_pattern = '^\s{4,}\w{1,}\s{1,}?=\s{1,}?{$\n'
    is_multi_line_embed_key = re.compile(multi_line_embed_key_pattern)

    # line that has the values of a multi line embedded object
    multi_line_embed_value_pattern = '^\s{4,}(-- )?(\s{1,})?(\w{1,})?(\s{1,})?".{0,}",?$\n'
    is_multi_line_embed_value = re.compile(multi_line_embed_value_pattern)

    # marks the end of the data structure of the file by finding the main function
    end_of_data_pattern = "^function\s{1,}main\(.{0,}\)$\n|^main\s{0,}=\s{0,}function\(.{0,}\)$\n"
    is_end_of_data = re.compile(end_of_data_pattern)

    # return objects
    lua_beg = ""
    lua_end = "\n"

    # loop state objects
    current_item_id = -1
    stage_of_file = "beg"

    with open(file=file_dir, mode="r", encoding=encoding) as lua:
        counter = 0
        for line in lua:
            if is_new_item_line.match(line):
                # if item code is found,
                # extract item code
                current_item_id = re.search(pattern=extract_item_code, string=line).group(0)
                if current_item_id not in item_dict:
                    item_dict[current_item_id] = {}
                    # make a new dictionary reference
                stage_of_file = "mid"
            elif is_key_value_line.match(line):
                # if this is a key_value_pair line
                # add that key and value to the current item
                key_value_list = line.split("=")

                # key
                key = key_value_list[0].strip().replace("\n", "")

                # value
                value = key_value_list[1].strip().replace("\n", "").replace("}", "").replace("{", "")
                if value[-1:] == ",":  # removes trialing comma
                    # if there is a trailing comma, remove it
                    value = value[:-1]
                
                # adds key and value to the current item dict
                if key == "identifiedDescriptionName":
                    item_dict[current_item_id]["description"] = value
                elif key == "identifiedResourceName":
                    item_dict[current_item_id]["sprite"] = value
                elif key == "identifiedDisplayName":
                    item_dict[current_item_id]["display_name"] = value
            elif is_multi_line_embed_key.match(line):
                # if it's the start of a multi line embed, create an embedded dictionary with a list
                # as it's value
                item_dict[current_item_id]["description"] = []
            elif is_multi_line_embed_value.match(line):
                # if it's the values of a multi line embed, append it to the descriptions list
                value = line.strip()
                if value[-1:] == ",":
                    value = value[:-1]
                item_dict[current_item_id]["description"].append(value)
            elif stage_of_file == "beg":
                # if it's still part of the file before the item data structure,
                #   record everything to be rewritten later
                lua_beg += line
            elif is_end_of_data.match(line):
                # if it's past part of the item data structure in the file,
                #   record everything to be rewritten later
                stage_of_file = "end"
                lua_end += line
            elif stage_of_file == "end":
                # if it's past part of the item data structure in the file,
                #   record everything to be rewritten later
                lua_end += line
            else:
                # These are the lines skipped, print to be sure we didn't leave
                #     anything  behind.
                ignored_data = line.strip()
                if ignored_data != "":
                    if ignored_data[0] != "}":
                        print("Skipping line: " + str(counter) + ": " + line)
            counter += 1

    print("Parsed " + str(counter) + " lines from Lua.")
    item_lua_dict = {
        "beg": lua_beg,
        "mid": item_dict,
        "end": lua_end
    }
    return item_lua_dict


# Tells the user in the console what file is currently being opened.
def print_opening_dir(file_dir):
    max_length = 30
    if len(file_dir) > max_length:
        filename = "..." + file_dir[-max_length:]
    else:
        filename = file_dir
    print("Opening: " + filename)


# Tells the user how many lines were writte to a file
def print_writing_status(counter, file_dir):
    filename = file_dir.split("/")[-1]
    print("Found... " + str(counter) + " items in " + filename + "\n")


# Takes in an existing item dictionary then adds to it by reading in an item_db
# Parameters:
#   file_dir = full path to the item_db.txt file
#   item_db = dictionary of existing items
# Return: the same item_db that was augmented with the item_db entries
def parse_item_db(file_dir, item_db):
    print_opening_dir(file_dir=file_dir)
    with open(file=file_dir, mode="r") as reborn_item_db_f:
        item_db_entry_pattern = '^\d{3,5},.{0,}$\n'  # looks for an item_id followed by 19 commas
        is_item_db_line = re.compile(item_db_entry_pattern)
        counter = 0
        for line in reborn_item_db_f:
            if is_item_db_line.match(line):
                item_n_scripts = line.split(",{")
                attribute_line = item_n_scripts[0]
                attributes = attribute_line.split(",")

                item_id = attributes[0]
                if item_id not in item_db:
                    item_db[item_id] = {}
                item_db[item_id]["display_name"] = attributes[2].strip()
                item_db[item_id]["item_type"] = attributes[3].strip()
                item_db[item_id]["buy_price"] = attributes[4].strip()
                item_db[item_id]["weight"] = attributes[6].strip()
                item_db[item_id]["weapon_atk"] = attributes[7].strip()
                item_db[item_id]["defense"] = attributes[8].strip()
                item_db[item_id]["weapon_range"] = attributes[9].strip()
                item_db[item_id]["slots"] = attributes[10].strip()
                item_db[item_id]["job"] = attributes[11].strip()
                item_db[item_id]["upper"] = attributes[12].strip()
                item_db[item_id]["gender"] = attributes[13].strip()
                item_db[item_id]["loc"] = attributes[14].strip()
                item_db[item_id]["weapon_lvl"] = attributes[15].strip()
                item_db[item_id]["required_lvl"] = attributes[16].strip()
                item_db[item_id]["refineable_lvl"] = attributes[17].strip()
                item_db[item_id]["view_id"] = attributes[18].strip()
                item_db[item_id]["script"] = item_n_scripts[1].replace("}", "").strip()
                item_db[item_id]["script_on_equip"] = item_n_scripts[2].replace("}", "").strip()
                item_db[item_id]["script_on_unequip"] = item_n_scripts[3].replace("}", "").strip()
                counter += 1
    print_writing_status(counter=counter,file_dir=file_dir)
    return item_db


# Summary: takes in an item dictionary, outputs to csv
# Params:
#       -file_dir: full path to file to be written out
#       -item_dict: the dictionary to be converted to csv
#       -encoding: the encoding to be used to write the file
def write_dict_to_tsv(file_dir, item_dict, encoding):
    print_opening_dir(file_dir=file_dir)
    headers = scan_headers(dictionary=item_dict, name_of_pk="item_id")
    f = open(file=file_dir, mode="w", encoding=encoding)
    f.write("\t".join(headers) + "\n")   # writes headers
    counter = 1
    for item_id in item_dict:    # loops over each item
        line = str(item_id)
        for header in headers:  # loops over each attribute inside each item
            if header in item_dict[item_id]:
                line += str(item_dict[item_id][header])
            line += "\t"
        f.write(line + "\n")
        counter += 1
    f.close()
    print("Wrote " + str(counter) + " items to: " + file_dir)


# Writes an iteminfo lua and from a 3 element dictionary parameter [1]<lua_parts> whoses keys are
# beg, mid, and end.
# beg is the begining of the file
# mid is the data structure in the middle of the file as a dictionary
# end is the remaining code in the file after the data structure
# [0]<file_dir> is the full path of the file to be written
# [2]<is_korean> can be True or False, true will specify encoding of ms949 for korean encoding
#     while false will yeild utf-8 encoding
def write_lua_items_to_lua(file_dir, lua_parts, encoding):
    print_opening_dir(file_dir=file_dir)

    # file parts
    lua_beg = lua_parts["beg"]
    lua_dict = lua_parts["mid"]
    lua_end = lua_parts["end"]

    # writting specs
    spaces_per_tab = 4
    tab = " " * spaces_per_tab

    f = open(file=file_dir, mode="w+", encoding=encoding)
    f.write(lua_beg)  # first line

    lua_dict_keys = sorted([int(x) for x in lua_dict])
    for item_id in lua_dict_keys:
        item_id = str(item_id)
        f.write(tab + "[" + item_id + "] = {\n")
        for item_key in sorted(lua_dict[item_id]):
            if isinstance(lua_dict[item_id][item_key], list):

                multi_line_embed_str = tab * 2 + item_key + " = {\n"

                for item in lua_dict[item_id][item_key]:
                    multi_line_embed_str += tab * 3 + item + ",\n"
                multi_line_embed_str += tab * 2 + "},\n"
                f.write(multi_line_embed_str)
            else:
                f.write(tab * 2 + str(item_key) + " = " + str(lua_dict[item_id][item_key]) + ",\n")
        f.write(tab + "},\n")
    f.write("}\n")
    f.write(lua_end)
    print("Writing " + str(len(lua_dict)) + " items to... " + file_dir)
    f.close()


# Takes in a dictionary and creates a list of headers for a csv file
# based upon all keys inside of the dictionary.
# Params:
#   dict: takes in a dictioanry to populate the headers with its keys
#   prefix: what the items headers should be prefixed with, helps mitigate colisions when
#       merging two dictionaries together
#   pk: primary key name of the parent key of the file to be incorporated into the list of header names
# Return: a list of header names
def scan_headers(dictionary, name_of_pk):
    headers = [name_of_pk]
    for item_id in dictionary:  # loop over all items
        for attribute in dictionary[item_id]:  # loop over all attributes of items
            if attribute not in headers:
                headers.append(attribute)
    return headers


main()

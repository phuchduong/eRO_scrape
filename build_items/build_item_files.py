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


def main():
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

    # new iteminfo
    new_iteminfo_dir = "D:/repos/eRODev/eRO Client Data/data/luafiles514/lua files/datainfo/pre_re_itemInfo.lua"

    # old iteminfo
    old_iteminfo_dir = "D:/repos/eRODev/eRO Client Data/System/itemInfosryx.lub"

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

    ######################
    # tamsinwhitfield db #
    ######################
    # Read in tamsinwhitfield as a dictionary by item_id as the key, remaining line as values
    # Ignores any item in the ignore list.
    with open(file=repo_dir + tw_dir, mode="r") as tw:
        print("Opening... " + repo_dir + tw_dir)
        tw_header = tw.readline()  # header
        tw_dict = parse_item_scrape_tsv(file_reader=tw, ignore_list=old_ero_ignore_list)
        print("Found... " + str(len(tw_dict)) + " items...")

    ##################
    # web archive db #
    ##################
    # Read in webarchive as a dictionary by item_id as the key, remaining line as values
    # Ignores any item in the ignore list.
    with open(file=repo_dir + wa_dir, mode="r") as wa:
        print("Opening... " + repo_dir + wa_dir)
        wa_header = wa.readline()  # header
        wa_dict = parse_item_scrape_tsv(file_reader=wa, ignore_list=old_ero_ignore_list)
        print("Found... " + str(len(wa_dict)) + " items...")

    ##################################################
    # Combine both old item db dictionaries together #
    ##################################################

    # Combines both item keys togther into a set that is sorted
    item_ids_all = list(wa_dict.keys()) + list(tw_dict.keys())  # Adds both item lists together
    item_ids_all = set(item_ids_all)  # removes duplicate item_ids
    item_ids_all = sorted(item_ids_all)  # sorts the keys

    for item_id in item_ids_all:
        # parse tw items
        if item_id in tw_dict:
            tw_item = tw_dict[item_id]
        else:
            # Item does not exist in tw_item_db
            pass

        # parse wa items
        if item_id in wa_dict:
            wa_item = wa_dict[item_id]
        else:
            # Item does not exist in wa_item_db
            pass

    ############
    # Patterns #
    ############
    # Begin item match
    new_item_line_pattern = "^\s{4,}\[\d{3,5}\]\s{1,}?=\s{1,}?{$\n"
    is_new_item_line = re.compile(new_item_line_pattern)

    # 3~5 digit item code
    item_code_pattern = "\d{3,5}"
    extract_item_code = re.compile(item_code_pattern)

    key_value_line_pattern = '^\s{4,}\w{1,}\s{1,}?=\s{1,}?((".{0,}"|\d{1,})|{.{0,}}),?$\n'
    is_key_value_line = re.compile(key_value_line_pattern)

    multi_line_embed_key_pattern = '^\s{4,}\w{1,}\s{1,}?=\s{1,}?{$\n'
    is_multi_line_embed_key = re.compile(multi_line_embed_key_pattern)

    multi_line_embed_value_pattern ='^\s{4,}".{0,}",?$\n'
    is_multi_line_embed_value = re.compile(multi_line_embed_value_pattern)

    end_of_data_pattern = "^function \w{0,}\(\)$\n"
    is_end_of_data = re.compile(end_of_data_pattern)

    nid_beg = ""
    nid_dict = {}
    nid_end = "\n"
    current_item_id = -1
    current_embed_key = ""
    stage_of_file = "beg"
    # read in new iteminfo
    with open(file=old_iteminfo_dir, mode="r", encoding="ms949") as nid:
        print("Opening... " + new_iteminfo_dir)
        counter = 0
        for line in nid:
            if is_new_item_line.match(line):
                # if item code is found,
                # extract item code
                current_item_id = re.search(pattern=extract_item_code, string=line).group(0)
                if current_item_id not in nid_dict:
                    nid_dict[current_item_id] = {}
                    # make a new dictionary reference
                stage_of_file = "mid"
            elif is_key_value_line.match(line):
                # if this is a key_value_pair line
                # add that key and value to the current item
                key_value_list = line.split("=")

                # key
                key = key_value_list[0].strip().replace("\n", "")

                # value
                value = key_value_list[1].strip().replace("\n", "")  # removes trialing comma
                if value[-1:] == ",":
                    # if there is a trailing comma, remove it
                    value = value[:-1]

                # adds key and value to the current item dict
                nid_dict[current_item_id][key] = value
            elif is_multi_line_embed_key.match(line):
                # if it's the start of a multi line embed, create an embedded dictionary with a list
                # as it's value
                current_embed_key = line.split("=")[0].strip()
                nid_dict[current_item_id][current_embed_key] = []
            elif is_multi_line_embed_value.match(line):
                value = line.strip()
                if value[-1:] == ",":
                    value = value[:-1]
                nid_dict[current_item_id][current_embed_key].append(value)
            elif stage_of_file == "beg":
                nid_beg += line
            elif is_end_of_data.match(line):
                stage_of_file = "end"
                nid_end += line
            elif stage_of_file == "end":
                nid_end += line
            counter += 1
        print("Lines found: " + str(counter))

    iteminfo_dir = "D:/repos/eRODev/eRO Client Data/System/new_itemInfosryx.lub"
    spaces_per_tab = 4
    tab = " " * spaces_per_tab

    f = open(file=iteminfo_dir, mode="w+", encoding="ms949")
    f.write("\n" + nid_beg)  # first line

    for item_id in nid_dict:
        f.write(tab + "[" + str(item_id) + "] = {\n")
        for item_key in nid_dict[item_id]:
            if isinstance(nid_dict[item_id][item_key], list):

                multi_line_embed_str = tab * 2 + item_key + " = {\n"

                for item in nid_dict[item_id][item_key]:
                    multi_line_embed_str += tab * 3 + item + ",\n"
                multi_line_embed_str += tab * 2 + "},\n"
                f.write(multi_line_embed_str)
            else:
                f.write(tab * 2 + str(item_key) + " = " + str(nid_dict[item_id][item_key]) + ",\n")
        f.write(tab + "},\n")
    f.write(nid_end)
    f.close()

    # for x in nid_dict[key]:
    #     print(print("\t" * 2 + x + " = " + nid_dict[key][x]) + ",\n")
    # read in old iteminfo
    # Using Windows-949 encoding (korean)
    with open(file=old_iteminfo_dir, mode="r", encoding="ms949") as oid:
        print("Opening... " + old_iteminfo_dir)
        counter = 0
        for line in oid:
            counter += 1
        print("Lines found: " + str(counter))

# Parses a TSV and returns a dictionary.
# Grabs the first item in the TSV on each line as the key, converts
#   key to integer.
# The remaining line becomes the value of the key.
# Ex. "a/tb/tc/td/te/t/n" input would return
# {
#   "a": "b/tc/td/te/t/n"
# }
# Takes in a list of keys to ignore and skip
def parse_item_scrape_tsv(file_reader, ignore_list):
    tsv_dict = {}
    for line in file_reader:  # body
        item_id = int(line.split("\t")[0])
        if item_id not in ignore_list:
            # skip items in the ignore list
            item_body = line[len(str(item_id)) + 1:]  # grabs everything after the item_id
            tsv_dict[item_id] = item_body
    return tsv_dict


main()



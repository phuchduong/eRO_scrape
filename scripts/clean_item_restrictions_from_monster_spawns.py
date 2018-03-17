#!/usr/bin/env python.
'''
    File name: clean_item_restrictions_from_monster_spawns.py
    Date created: March 17, 2018
    Python version: 3.6.1
    Version: 1.0.0
    Purpose:
        Goal: Fix, the item_trade.txt
            • Get a list of monsters that naturally spawn.
            • Link those monsters that spawn, with their drops.
            • Get a list of items that are dropped by monsters that naturally spawn
            • Scan through, the item_trade.txt
            • Find items, that are dropped by monsters that spawn naturally,
            • Then: remove those items.
    Author: Phuc H Duong
    Original Repo: https://github.com/phuchduong/essencero_restoration
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import re
from datetime import datetime


def main():
    ##########################################################################
    # 1 Get a list of monsters that naturally spawn.
    ##########################################################################
    spawn_path_root = "D:/repos/essencera/npc/pre-re/mobs/"

    spawn_db = {}
    spawn_files = get_monster_spawn_table()
    for filename in spawn_files:
        spawn_file_filepath = spawn_path_root + filename
        spawn_db = get_monster_spawns_from_file(
            file_path=spawn_file_filepath, spawn_db=spawn_db)
    ##########################################################################
    # 2 Link those monsters that spawn, with their drops.
    # 3 Get a list of items that are dropped by monsters that naturally spawn
    ##########################################################################
    item_drop_list = []

    item_drop_list = get_list_of_item_drops(spawn_db)

    ##########################################################################
    # 4 can through, the item_trade.txt
    # 5 Find items, that are dropped by monsters that spawn naturally,
    # 6 Then: remove those items.
    ##########################################################################
    old_item_trade_path = 'D:/repos/essencera/db/pre-re/item_trade.txt'
    new_item_trade_path = 'D:/repos/essencero_restoration/scripts/output/item_trade.txt'
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    restricted_item_regex = '^\d{3,5},\d{1,3},\d{1,3}'
    is_restricted_item = re.compile(restricted_item_regex)
    with open(file=old_item_trade_path, mode="r") as old_f:
        for line in old_f:
            if is_restricted_item.match(line):
                line_split = line.split(",")
                item_id = int(line_split[0])
                if item_id in item_drop_list:
                    print(line)

def get_monster_spawns_from_file(file_path, spawn_db):
    # monster search function
    monster_regex = "^\w{1,},\d,\d"
    is_monster = re.compile(monster_regex)

    # opened the file
    with open(file=file_path, mode="r") as in_f:
        # grab each monster line

        for line in in_f:
            # looping through the file
            if is_monster.match(line):
                line_split = line.split("\t")
                line_split = line_split[3].split(",")

                try:
                    mob_id = int(line_split[0])
                    spawn_count = int(line_split[1])
                    if mob_id in spawn_db:
                        spawn_db[mob_id] += spawn_count
                    else:
                        spawn_db[mob_id] = spawn_count
                except ValueError:
                    pass
    return spawn_db


def get_monster_spawn_table():
    monster_spawn_tables = [
        "fields/amatsu.txt",
        "fields/ayothaya.txt",
        "fields/comodo.txt",
        "fields/dicastes.txt",
        "fields/einbroch.txt",
        "fields/geffen.txt",
        "fields/gonryun.txt",
        "fields/hugel.txt",
        "fields/lighthalzen.txt",
        "fields/louyang.txt",
        "fields/lutie.txt",
        "fields/manuk.txt",
        "fields/mjolnir.txt",
        "fields/morocc.txt",
        "fields/moscovia.txt",
        "fields/niflheim.txt",
        "fields/payon.txt",
        "fields/prontera.txt",
        "fields/rachel.txt",
        "fields/splendide.txt",
        "fields/umbala.txt",
        "fields/veins.txt",
        "fields/yuno.txt",
        "dungeons/abbey.txt",
        "dungeons/abyss.txt",
        "dungeons/alde_dun.txt",
        "dungeons/ama_dun.txt",
        "dungeons/anthell.txt",
        "dungeons/ayo_dun.txt",
        "dungeons/beach_dun.txt",
        "dungeons/c_tower.txt",
        "dungeons/ein_dun.txt",
        "dungeons/gefenia.txt",
        "dungeons/gef_dun.txt",
        "dungeons/glastheim.txt",
        "dungeons/gld_dun.txt",
        "dungeons/gld_dunSE.txt",
        "dungeons/gon_dun.txt",
        "dungeons/ice_dun.txt",
        "dungeons/in_sphinx.txt",
        "dungeons/iz_dun.txt",
        "dungeons/juperos.txt",
        "dungeons/kh_dun.txt",
        "dungeons/lhz_dun.txt",
        "dungeons/lou_dun.txt",
        "dungeons/mag_dun.txt",
        "dungeons/mjo_dun.txt",
        "dungeons/moc_pryd.txt",
        "dungeons/mosk_dun.txt",
        "dungeons/nyd_dun.txt",
        "dungeons/odin.txt",
        "dungeons/orcsdun.txt",
        "dungeons/pay_dun.txt",
        "dungeons/prt_maze.txt",
        "dungeons/prt_sew.txt",
        "dungeons/ra_san.txt",
        "dungeons/tha_t.txt",
        "dungeons/thor_v.txt",
        "dungeons/treasure.txt",
        "dungeons/tur_dun.txt",
        "dungeons/um_dun.txt",
        "dungeons/xmas_dun.txt",
        "dungeons/yggdrasil.txt",
    ]
    return monster_spawn_tables


def get_list_of_item_drops(spawn_db):
    db_path1 = "D:/repos/essencera/db/pre-re/mob_db.txt"
    db_path2 = "D:/repos/essencera/db/import-tmpl/mob_db.txt"
    # print(spawn_db)
    monster_regex = '\d{4,}'
    starts_with_id = re.compile(monster_regex)
    item_list = []
    drop_index = [37, 39, 41, 43, 45, 47, 49, 51, 53]
    with open(file=db_path1, mode="r") as in_f:
        for line in in_f:
            if starts_with_id.match(line):
                line_split = line.split(",")
                mob_id = int(line_split[0])
                if mob_id in spawn_db:
                    for i in drop_index:
                        try:
                            item_id = int(line_split[i])
                            if item_id not in item_list:
                                item_list.append(item_id)
                        except ValueError:
                            pass
    with open(file=db_path2, mode="r") as in_f:
        for line in in_f:
            if starts_with_id.match(line):
                line_split = line.split(",")
                mob_id = int(line_split[0])
                if mob_id in spawn_db:
                    for i in drop_index:
                        try:
                            item_id = int(line_split[i])
                            if item_id not in item_list:
                                item_list.append(item_id)
                        except ValueError:
                            pass
    item_list = sorted(item_list)
    # print(item_list)
    return item_list

main()


#!/usr/bin/env python.
'''
    File name: clean_item_restrictions_from_monster_spawns.py
    Date created: March 17, 2018
    Python version: 3.6.1
    Version: 0.2.0
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

    for mob_db in spawn_db:
        print(str(mob_db) + "\t|\tCount: " + str(spawn_db[mob_db]))
    ##########################################################################
    # 2 Link those monsters that spawn, with their drops.
    ##########################################################################
    item_drop_list = []

    item_drop_list = get_list_of_item_drops(item_drop_list)
    ##########################################################################
    # 3 Get a list of items that are dropped by monsters that naturally spawn
    ##########################################################################

    ##########################################################################
    # 4 can through, the item_trade.txt
    ##########################################################################

    ##########################################################################
    # 5 Find items, that are dropped by monsters that spawn naturally,
    ##########################################################################

    ##########################################################################
    # 6 Then: remove those items.
    ##########################################################################


def get_monster_spawns_from_file(file_path, spawn_db):
    # opened the file
    with open(file=file_path, mode="r") as in_f:
        # grab each monster line

        # monster search function
        monster_regex = "^\w{1,},\d,\d"
        is_monster = re.compile(monster_regex)
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


main()


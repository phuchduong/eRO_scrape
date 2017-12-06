#!/usr/bin/env python.
'''
    File name: job_equip_hex_converter.py
    Date created: November 22, 2017
    Python version: 3.6.1
    Purpose: converts class combinations into hex strings

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''

filename = "convert_to_hex_equipable_classes.tsv"

bit_dict = {
    "Novice": 1,
    "Swordman": 2,
    "Mage": 4,
    "Magician": 4,
    "Archer": 8,
    "Acolyte": 16,
    "Merchant": 32,
    "Thief": 64,
    "Knight": 128,
    "Priest": 256,
    "Wizard": 512,
    "Blacksmith": 1024,
    "Hunter": 2048,
    "Assassin": 4096,
    "Unused": 8192,
    "Crusader": 16384,
    "Monk": 32768,
    "Sage": 65536,
    "Rogue": 131072,
    "Alchemist": 262144,
    "Bard/Dancer": 524288,
    "Unused": 1048576,
    "Taekwon": 2097152,
    "Star Gladiator": 4194304,
    "Soul Linker": 8388608,
    "Gunslinger": 16777216,
    "Ninja": 33554432,
    "Gangsi": 67108864,
    "Death Knight": 134217728,
    "Dark Collector": 268435456,
    "Kagerou/Oboro": 536870912,
    "Rebellion": 1073741824,
    "Summoner": 2147483648,
    "All Jobs": 4294967295,
    "All Jobs Except Novice": 4294967294
}

with open(file=filename, mode="r+") as f:
    for line in f:
        line = line.replace("\n", "")
        jobs = line.split(" / ")
        if(len(jobs) == 1):
            hex_code = bit_dict[line]  # look up class bit
            hex_code = format(hex_code, "x")
        else:
            # adds up all classes bits and converts to hex
            # example: Novice + Swordman + Magician + Archer = 0x0000000F
            sum_dec = 0
            for job in jobs:
                sum_dec += bit_dict[job]
            hex_code = format(sum_dec, "x")
        # adds pre zeros to make 8 bit
        remaining = 8 - len(str(hex_code))
        hex_string = "0x" + "0" * remaining + str(hex_code)
        f.write(line + "\t" + hex_string + "\n")

f.close()

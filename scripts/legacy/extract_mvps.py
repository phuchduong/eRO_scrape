#!/usr/bin/env python.
'''
    File name: extract_mvps.py
    Date created: January 24, 2017
    Python version: 3.6.1
    Purpose: Extract all monsters out of a mob_db.
    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import re  # regular expression

def main():
	out_path = "C:\\repos\\essencero_restoration\\scripts\\outputs\\mvps.txt"
	db_path = "C:\\repos\\essencera\\db\\pre-re\\mob_db.txt"
	line_regex = "\d{4,}"
	mvp_id_list = [
		"1038", # Osiris
		"1039", # Baphomet
		"1046", # Doppelganger
		"1059", # Mistress
		"1086", # Golden Thief Bug
		"1087", # Orc Hero
		"1112", # Drake
		"1115", # Eddga
		"1147", # Maya
		"1150", # Moonlight Flower
		"1157", # Pharaoh
		"1159", # Phreeoni
		"1190", # Orc Lord
		"1251", # Knight of Windstorm
		"1252", # Garm
		"1272", # Dark Lord
		"1312", # Turtle General
		"1373", # Lord of Death
		"1389", # Dracula
		"1418", # Evil Snake Lord
		"1492", # Incantation Samurai
		"1511", # Amon Ra
		"1583", # Tao Gunka
		"1623", # RSX 0806
		"1630", # Bacsojin
		"1646", # Lord Knight Seyren
		"1647", # Assassin Cross Eremes
		"1648", # Whitesmith Harword
		"1649", # High Priest Magaleta
		"1650", # Sniper Shecil
		"1651", # High Wizard Katrinn
		"1658", # Ygnizem
		"1685", # Vesper
		"1688", # Lady Tanee
		"1708", # Thanatos
		"1719", # Detale
		"1734", # Kiel D-01
		"1751", # Valkyrie Randgris
		"1768", # Gloom Under Night
		"1779", # Ktullanux
		"1785", # Atroce
		"1832", # Ifrit
		"1871", # Fallen Bishop
		"1874", # Beelzebub
		"1885", # Gopinich
		"1917", # Wounded Morroc
		"1956", # Naght Sieger
		"1957", # Entweihen Crothen
		"2022", # Nidhoggr's Shadow
		"2317", # Bangungot
		"2319", # Buwaya
		"2320", # Bakonawa
		"2475", # Root of Corruption
		"2476", # Amdarias
		"2529", # Faceworm Queen
	]
	extract_by_ids(id_list=mvp_id_list, match_regex=line_regex, db_path=db_path, out_file_path=out_path)


def extract_by_ids(id_list, match_regex, db_path, out_file_path):
	starts_with_id = re.compile(match_regex)
	mvp_list = []
	non_mvp_list = []
	with open(file=db_path, mode="r") as in_f:
		for line in in_f:
			uncommented_line = line.replace("//","") # removes comments
			if starts_with_id.match(uncommented_line):
				line_split = uncommented_line.split(",")
				if line_split[0] in id_list:
					# if mvp
					mvp_list.append(line)
				else:
					# if not mvp
					non_mvp_list.append(line)
			else:
				# if not a mob
				non_mvp_list.append(line)
	out_f = open(file=out_file_path, mode="w")
	for line in non_mvp_list:
		out_f.write(line)

	out_f.write("\n\n// MVPs\n")
	for line in mvp_list:
		out_f.write(line)
	out_f.write("\n\n")
	out_f.close()

main()


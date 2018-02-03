#!/usr/bin/env python.
'''
    File name: extract_item_names.py
    Date created: January 29, 2017
    Python version: 3.6.1
    Purpose: Extract all item names from the iteminfo and the item_db.
    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
import re  # regular expression

def main():
	out_path = "C:\\repos\\essencero_restoration\\scripts\\outputs\\mvps.txt"
	local_server_files_path = "C:\\repos\\essencera"
	iro_db_path = "C:\\repos\\essencera\\db\\pre-re\\item_db.txt"
	ero_db_path = "C:\\repos\\essencera\\db\\pre-re\\item_db.txt"

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


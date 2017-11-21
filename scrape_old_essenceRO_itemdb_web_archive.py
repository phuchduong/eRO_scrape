#!/usr/bin/env python.
'''
    File name: scrape_old_essenceRO_itemdb_web_archive.py
    Date created: November 17, 2017
    Python version: 3.6.1
    Purpose: to recreate the item_db.txt table from essenceRO.

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from selenium import webdriver  # imports web browser controller
from os.path import isfile

filename = "item_db_web_archive.tsv"

existing_ids = []  # keeps track of what ids have already been parsed
if isfile(filename):
    # if file exists
    print("Found existing scrape db... Scanning...")
    # read through entire file, and finds all ids
    # open in read mode
    with open(file=filename, mode="r") as f:
        next(f)  # skips header
        # scan through the file for all item ids
        for line in f:
            sub = line.find("\t")
            item_id = line[:sub]
            print("Found Item ID: " + item_id)
            existing_ids.append(item_id)
    f.close
    f = open(file=filename, mode="a")  # opens in append mode
else:
    # if file does not exist create a new one in write mode
    print("Creating a new file...")
    f = open(file=filename, mode="w")
    header = "Item ID,For Sale,Identifier,Credit Price,Name,Type,NPC Buy," \
             "Weight,NPC Sell,Attack,Range,Defense,Slots,Refineable,Equip Level," \
             "Weapon Level,Equip,Locations,Equip Upper,Equippable Jobs,Equip Gender," \
             "Item Use Script,Equip Script,Unequip Script,Image Path,Icon Path\n"
    f.write(header)
    print("Added header...")

root_url = "https://web.archive.org/web/20150524022657/http://essence-ro.com/item/view/"

# start at id 20000 if non exists, otherwise
# start at the last id pare
if len(existing_ids) > 0:
    beg = int(existing_ids[-1]) + 1
else:
    beg = 20000

# turn on the web client, must be downloaded from:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# note: firefox also has one too
chrome_driver_path = "D:/repos/scrape_eRO/chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_driver_path)

# loops between item id #20000 and #32022
for i in range(beg, 32022):
    item_id = i

    target_url = root_url + "?id=" + str(item_id)

    # tells browser to navigate to page
    browser.get(target_url)

    # find all tables
    query = browser.find_elements_by_tag_name("tbody")

    # get last table
    try:
        tbody = query[5]
        # find headers and values
        tds = tbody.find_elements_by_tag_name("td")
        ths = tbody.find_elements_by_tag_name("th")

        item_entry = {}
        for i in range(0, len(ths)):
            header = ths[i].text
            j = i
            if(j > 0):
                j = i + 1
            value = tds[j].text
            print(header + ": " + value)
            item_entry[header] = value
        # Grabs image path
        image_path = tds[1].find_element_by_tag_name("img").get_attribute("src")
        item_entry["Image Path"] = image_path
        print("Image Path: " + image_path)
        # Grabs icon path
        icon_path = browser.find_element_by_tag_name("h3").find_element_by_tag_name("img").get_attribute("src")
        item_entry["Icon Path"] = icon_path
        print("Icon Path: " + icon_path)
        entry_list = [
            item_entry["Item ID"],
            item_entry["For Sale"],
            item_entry["Identifier"],
            item_entry["Credit Price"],
            item_entry["Name"],
            item_entry["Type"],
            item_entry["NPC Buy"],
            item_entry["Weight"],
            item_entry["NPC Sell"],
            item_entry["Attack"],
            item_entry["Range"],
            item_entry["Defense"],
            item_entry["Slots"],
            item_entry["Refineable"],
            item_entry["Equip Level"],
            item_entry["Weapon Level"],
            item_entry["Equip Locations"],
            item_entry["Equip Upper"],
            item_entry["Equippable Jobs"],
            item_entry["Equip Gender"],
            item_entry["Item Use Script"],
            item_entry["Equip Script"],
            item_entry["Unequip Script"],
            item_entry["Image Path"],
            item_entry["Icon Path"]
        ]
        line = "\t".join(entry_list)
        line += "\n"
        print("Writing item file...")
        f.write(line)
    except IndexError:
        print("Skipping Item Id: " + str(item_id))
        line = str(item_id) + "".join(["\t" * 24]) + "\n"
        f.write(line)

f.close()

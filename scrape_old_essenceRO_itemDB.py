#!/usr/bin/env python.
'''
    File name: scrape_old_essenceRO_itemDB.py
    Date created: November 17, 2017
    Python version: 3.6.1
    Purpose: to recreate the item_db.txt table from essenceRO.

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''
from string import ascii_lowercase  # the alphabet a-z
from selenium import webdriver      # autonomous webpage client
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime
from time import sleep


# scrapes a single page from http://www.tamsinwhitfield.co.uk/cp/item_db.php
# returns a list of items and their information as dictionary entries
def scrape_page(items_list, driver):

    parsed_items = items_list

    # isolates the div housing the item tables
    query_divs = driver.find_elements_by_id("ajax")

    # grabs a list of WebElements holding the item-id and display name
    titles = query_divs[0].find_elements_by_css_selector('h3.table-head')

    # grabs a list of WebElements holding the item details
    i_tables = query_divs[0].find_elements_by_tag_name("tbody")

    # parse item_id and display_name
    for i in range(0, len(titles)):
        # loops through each title, skipping the first one.
        id_name = titles[i].text
        print("Found... " + id_name)

        # separates item_id from item display name
        sep = id_name.find(" ")  # finds the first space separation
        item_id = id_name[:sep]
        display_name = id_name[(sep + 1):]

        item_entry = {
            "item_id": item_id,
            "display_name": display_name
        }

        # parses item details like descriptions and item types
        col_headers = i_tables[i].find_elements_by_tag_name("th")
        col_values = i_tables[i].find_elements_by_tag_name("td")
        for j in range(1, len(col_headers)):
            col_name = col_headers[j].text
            value = col_values[j].text

            # scripts were sanitized, putting curly brace back in
            if(col_name == "Item Script"):
                value = "{ " + value + " }"

            item_entry[col_name] = value

        parsed_items.append(item_entry)

    return parsed_items


# scrapes all the pages, then scans for a next button and scrapes the next page
# until it can no longer find a next button.
def scrape_all_pages(items_list, driver):
    items_list = scrape_page(items_list=items_list, driver=driver)
    print("Page done...")
    try:
        # If there is a next button in the pagnation, click it
        next_button = driver.find_element_by_xpath("//a[text()='Next']")
        print("Found another page... Going to next page...")
        next_button.click()
        # recursion: scrape page
        print("Waiting for page to load...")
        sleep(2)
        try:
            items_list = scrape_all_pages(items_list, driver)
        except StaleElementReferenceException as e:
            items_list = scrape_all_pages(items_list, driver)
    except NoSuchElementException as e:
        pass
    return(items_list)


# verbose url
# http://www.tamsinwhitfield.co.uk/cp/item_db.php?limit=30&sort=0&order=ASC&id=0&item=&type=6&iclass=-1&slot_sign=-1&slots=-1&desc=&script=&letter=Z&search_x=0&search_y=0&start=0
# shorten url
# http://www.tamsinwhitfield.co.uk/cp/item_db.php?limit=99&type=6&letter=A&start=0
base_url = "http://www.tamsinwhitfield.co.uk/cp/item_db.php"

# url param: type, item type
# -1 = (Any)
# 0 = Healing Item
# 2 = Usable Item
# 3 = Misc
# 4 = Weapon
# 5 = Armor
# 6 = Card
# 7 = Pet Egg
# 8 = Pet Equipment
# 10 = Ammunition
# 11 = Usable Item (delayed)
# 12 = Special
p_type = "-1"


# turn on the web client, must be downloaded from:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# note: firefox also has one too
chrome_driver_path = "chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_driver_path)

# holds all the items found and parsed
parsed_items = []

# url param: letter
for c in ascii_lowercase:
    ''' scrapes all items a-z pages '''
    p_letter = c
    target_url = base_url + "?letter=" + p_letter + "&type=" + p_type + "&limit=25&start=0"

    # tells the bot browser to the url
    browser.get(target_url)

    parsed_items = scrape_all_pages(items_list=parsed_items, driver=browser)

# closes the browser
browser.quit()

# Gets current time now as a string
scrape_time = datetime.now().strftime("%Y%m%d%H%M%S")

# prints the items found and its details
all_headers = []

# creates a list of all possible headers by going through
# and recording all items and all their dictionary keys
for item in parsed_items:
    for key in item:
        if key not in all_headers:
            all_headers.append(key)

filename = "items_" + scrape_time + ".tsv"
f = open(filename, "w")

# writes the header file
header = "\t".join(all_headers) + "\n"
f.write(header)

# writes each item into a row in the tsv
for item in parsed_items:
    entry = ""
    for header in all_headers:
        try:
            value = item[header]
            entry += value
        except KeyError:
            pass
        entry += "\t"  # adds a tab
    # trims the last tab
    last_tab = entry.rfind("\t")
    entry = entry[:last_tab]
    entry += "\n"
    entry = entry.replace("�", "-")
    f.write(entry)

# closes the file
f.close()

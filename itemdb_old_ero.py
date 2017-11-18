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
from bs4 import BeautifulSoup       # html data structure
# from urllib.request import urlopen
from string import ascii_lowercase  # the alphabet a-z
from selenium import webdriver      # autonomous webpage client
from selenium.common.exceptions import NoSuchElementException

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
p_type = "6"

# url param: letter
# for c in ascii_lowercase:
    # ''' scrapes all items a-z pages '''
    # print(c)

p_letter = 'z'
target_url = base_url + "?letter=" + p_letter + "&type" + p_type + "&limit=99&start=0"

# turn on the web client, must be downloaded from:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# note: firefox also has one too
chrome_driver_path = "chromedriver.exe"
driver = webdriver.Chrome(executable_path = chrome_driver_path)

# tells the bot browser to the url
driver.get(target_url)

# grabs elements holding the item-id and display name
titles = driver.find_elements_by_css_selector('h3.table-head')

parsed_items = {}

for i in range(1, len(titles)):
    # loops through each title, skipping the first one.
    id_name = titles[i].text

    print("Found..." + id_name)

    # separates item_id from item display name
    sep = id_name.find(" ")  # finds the first space
    item_id = id_name[:sep]
    display_name = id_name[(sep + 1):]

    # add to dictonary
    parsed_items[item_id] = {"display_name": display_name}

for item in parsed_items:
    print(item + "," + str(parsed_items[item]["display_name"]))

# Closes the browser
# driver.quit()
# try:
#   # If there is a next button in the pagnation, click it
#   next_button = driver.find_element_by_xpath("//a[text()='Next']")
#   next_button.click()

#   # recursion: scrape page
# except NoSuchElementException as e:
#   pass
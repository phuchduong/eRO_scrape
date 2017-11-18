#!/usr/bin/env python.
'''
    File name: itemdb_old_ero.py
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
i_type = 6

# url param: letter
# for c in ascii_lowercase:
    # ''' scrapes all items a-z pages '''
    # print(c)

letter = 'z'
target_url = base_url + "?letter=" + letter + "&type" + i_type

# u_client = urlopen(target_url)

# page_soup = BeautifulSoup(u_client.read(), "html.parser")

# u_client.close()

# turn on the web client, must be downloaded from:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# note: firefox also has one too
driver = webdriver.Chrome("D:/repos/scrape_eRO/chromedriver.exe")
driver.get(target_url)
# have the browser open the page
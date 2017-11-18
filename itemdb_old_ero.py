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

base_url = "http://www.tamsinwhitfield.co.uk/cp/item_db.php"

for c in ascii_lowercase:
    ''' scrapes all items a-z pages '''
    print(c)

letter = 'z'
target_url = base_url + "?letter=" + letter

# u_client = urlopen(target_url)

# page_soup = BeautifulSoup(u_client.read(), "html.parser")

# u_client.close()

# turn on the web client, must be downloaded from:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# note: firefox also has one too
driver = webdriver.Chrome("D:/repos/scrape_eRO/chromedriver.exe")

# have the browser open the page
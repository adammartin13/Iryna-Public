"""
This file contains the scripts for iterating through our dataset and pulling text from associated articles. HTML is sent
to WebScrapers.py as a pandas dataframe for specialized parsing prior to being updated in our dataset.

Information on pro-info sources has been omitted from the public version of this project.
"""
import os
import subprocess
import time
from selenium import webdriver  # Gets HTML, opens browser
import selenium.common.exceptions
import pandas as pd
from bs4 import BeautifulSoup as BS  # parses HTML
import dataCleanup  # contains methods for cleaning .csv data
import WebScrapers  # contains methods for scraping article text


def vpn_reconnect():
    os.system('mullvad disconnect')
    os.system('mullvad relay set location any')
    os.system('mullvad connect')
    while subprocess.check_output('mullvad status', shell=True, text=True)[:9] != 'Connected':
        pass


def new_driver():  # Creates new webdriver instance
    vpn_reconnect()
    driver = webdriver.Firefox()
    driver.delete_all_cookies()  # delete all cookies
    time.sleep(3)  # Time to prevent driver interruption
    return driver


def get_html(url):
    try:
        driver.get(url)
        time.sleep(5)
        return driver.page_source
    except selenium.common.exceptions.WebDriverException:
        os.system('mullvad disconnect')  # change to "Russia trusted" location
        os.system('mullvad relay set location hk')
        os.system('mullvad connect')
        while subprocess.check_output('mullvad status', shell=True, text=True)[:9] != 'Connected':
            pass
        driver.refresh()
        time.sleep(5)
        return driver.page_source


# If title in URL, can validate w/o opening driver
title_urls = ['rt.com', 'sputnikglobe.com']

# Article title will need translating
needs_translating = ['uz.sputniknews.ru', 'ТАСС', 'ИноСМИ', 'inosmi.ru']

crankie_panda = pd.read_csv('data.csv')   # panda is eepy after long day of reading html

for index, article in crankie_panda.iterrows():
    if article['Title'] != '0':  # Title field already populated, text is scraped
        continue
    if article['Source'] in title_urls:
        verify = input("Continue or Discard (c/d)? " + article['Link'] + '\n')
        if 'd' in verify:
            dataCleanup.flagged_article(article['Link'])
            crankie_panda = crankie_panda.drop(index)
            crankie_panda.to_csv('data.csv', index=False)
            continue
    driver = new_driver()
    print(article['Link'])
    html = get_html(article['Link'])
    fr_onion = BS(html, features="html.parser")
    title = fr_onion.find_all('title')
    title = title[0].get_text()
    interrupted_connections = ['HTTP 504']
    if title in interrupted_connections:
        # found title returns when connection is lost, above array is discovered instances of such
        print('Connection Lost')
        driver.quit()
        exit(0)
    driver.quit()
    print(title)
    if article['Source'] in needs_translating:
        title = dataCleanup.translate(title)
    verify = input("Is the following topic relevant (y/n)? " + title + '\n')
    if 'n' in verify:
        dataCleanup.flagged_article(article['Link'])
        crankie_panda = crankie_panda.drop(index)
        crankie_panda.to_csv('data.csv', index=False)
        driver.quit()
        continue
    if article['Source'] == 'sputnikglobe.com' or article['Source'] == 'uz.sputniknews.ru':
        crankie_panda.loc[index, 'Title'] = title
        crankie_panda.loc[index, 'Text'] = WebScrapers.sputnik(title, fr_onion)
        crankie_panda.to_csv('data.csv', index=False)
    if article['Source'] == 'ТАСС':
        crankie_panda.loc[index, 'Title'] = title
        crankie_panda.loc[index, 'Text'] = WebScrapers.tass(title, fr_onion)
        crankie_panda.to_csv('data.csv', index=False)
    if article['Source'] == 'rt.com':
        crankie_panda.loc[index, 'Title'] = title
        crankie_panda.loc[index, 'Text'] = WebScrapers.rt(title, fr_onion)
        crankie_panda.to_csv('data.csv', index=False)
    if article['Source'] == 'ИноСМИ':
        crankie_panda.loc[index, 'Title'] = title
        crankie_panda.loc[index, 'Text'] = WebScrapers.inosmi(title, fr_onion)
        crankie_panda.to_csv('data.csv', index=False)
    if article['Source'] == 'inosmi.ru':
        crankie_panda.loc[index, 'Title'] = title
        crankie_panda.loc[index, 'Text'] = WebScrapers.inosmi(title, fr_onion)
        crankie_panda.to_csv('data.csv', index=False)
    if article['Source'] == 'Zee24tass':
        crankie_panda.loc[index, 'Title'] = title
        crankie_panda.loc[index, 'Text'] = WebScrapers.zee(title, fr_onion)
        crankie_panda.to_csv('data.csv', index=False)

"""
This file contains scripts for web scraping specific to our domains. Each take in the html as a pandas object and return
the article text. The unique nature of these domains can result in a wide array of scraping methods.

Pro-information outlet scraping is omitted from the public version of this file.
"""
import re
from bs4 import BeautifulSoup as BS  # parses HTML


def sputnik(title, html):  # sputnikglobe.com
    data = title
    text = html.find_all('div', {'class': 'article__announce-text'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('div', {'class': 'article__text'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('div', {'class': 'article__quote-text'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('div', {'class': 'article__h2'})
    for item in text:
        data += ' ' + item.get_text()
    dirty_text = re.split(r'[,!?;:.\n\t]', data)
    clean_text = ''
    for word in dirty_text:
        clean_text += word + ' '
    while '  ' in clean_text:
        clean_text = clean_text.replace('  ', ' ')
    print(clean_text)
    return clean_text


def tass(title, html):  # tass.ru
    data = title
    text = html.find_all('h3')
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('span', {'class': 'tass_pkg_text-oEhbR'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('strong')
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('span', {'class': 'ds_ext_title-1XuEF'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('span', {'class': 'tass_pkg_title-xVUT1'})
    for item in text:
        data += ' ' + item.get_text()
    dirty_text = re.split(r'[,!?;:.\n\t]', data)
    clean_text = ''
    for word in dirty_text:
        clean_text += word + ' '
    while '  ' in clean_text:
        clean_text = clean_text.replace('  ', ' ')
    print(clean_text)
    return clean_text


def rt(title, html):
    data = title
    text = html.find_all('div', {'class': 'article__summary'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('p')
    for item in text:
        data += ' ' + item.get_text()
    dirty_text = re.split(r'[,!?;:.\n\t]', data)
    clean_text = ''
    for word in dirty_text:
        clean_text += word + ' '
    while '  ' in clean_text:
        clean_text = clean_text.replace('  ', ' ')
    print(clean_text)
    return clean_text


def inosmi(title, html):
    data = title
    text = html.find_all('h1', {'class': 'article__second-title'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('div', {'class': 'article__announce-text'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('div', {'class': 'article__text'})
    for item in text:
        data += ' ' + item.get_text()
    dirty_text = re.split(r'[,!?;:.\n\t]', data)
    clean_text = ''
    for word in dirty_text:
        clean_text += word + ' '
    while '  ' in clean_text:
        clean_text = clean_text.replace('  ', ' ')
    print(clean_text)
    return clean_text


def zee(title, html):
    data = title
    text = html.find_all('div', {'class': 'news-header__lead'})
    for item in text:
        data += ' ' + item.get_text()
    text = html.find_all('div', {'class': 'text-block'})
    for item in text:
        data += ' ' + item.get_text()
    dirty_text = re.split(r'[,!?;:.\n\t]', data)
    clean_text = ''
    for word in dirty_text:
        clean_text += word + ' '
    while '  ' in clean_text:
        clean_text = clean_text.replace('  ', ' ')
    print(clean_text)
    return clean_text


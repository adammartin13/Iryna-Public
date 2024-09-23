"""
Contains a modicum of methods used to clean up our csv data.

Information on pro-info sources have been omitted from the public version of this project.
"""
import pandas as pd
import csv
import re
from deep_translator import GoogleTranslator


# Checks for and removes duplicate rows in the csv
def remove_duplicates():
    file = "data.csv"
    fatpanda = pd.read_csv(file)
    fatpanda.drop_duplicates(subset=None, inplace=True)  # Drops duplicate UNSCRAPED rows
    print("Checking for duplicates...")
    for article in fatpanda.iterrows():
        if article[1][4] != '0':  # Title is scraped
            for comparator in fatpanda.iterrows():
                if comparator[1][4] == '0' and comparator[1][1] == article[1][1]:
                    print('Duplicate found: ' + comparator[1][1])
                    fatpanda = fatpanda.drop(fatpanda[(fatpanda.Link == comparator[1][1])
                                                      & (fatpanda.Title == '0')].index)
    fatpanda.to_csv('data.csv', index=False)
    print('Duplicates removed')


# Removes bad links based on url patterns for each domain
def remove_bad_links():
    file = "data.csv"
    hungiepanda = pd.read_csv(file)  # panda is hungie for bad links
    for article in hungiepanda.iterrows():
        if 'sputnik' in article[1][0]:
            if '/20' not in article[1][1]:
                hungiepanda = hungiepanda.drop(hungiepanda[hungiepanda['Link'] == article[1][1]].index)
        elif 'tass.ru' == article[1][0]:  # Other Tass domains appear to not be relevant
            if article[1][0] != 'tass.ru' and article[1][0] != 'Zee24tass' or article[1][0] != 'ТАСС':
                hungiepanda = hungiepanda.drop(hungiepanda[hungiepanda['Link'] == article[1][1]].index)
            elif article[1][0] == 'tass.ru' or article[1][0] == 'ТАСС':
                if '/politika/' not in article[1][1] and '/armiya-i-opk/' not in article[1][1] and 'panorama/' not in \
                        article[1][1] and '/obschestvo/' not in article[1][1] and '/proisshestviya/' not in \
                        article[1][1] and '/opinions/' not in article[1][1] and '/plus-one/' not in article[1][1] and \
                        '/interviews/' not in article[1][1]:
                    hungiepanda = hungiepanda.drop(hungiepanda[hungiepanda['Link'] == article[1][1]].index)
            elif article[1][0] == 'Zee24tass':
                if '/world/' not in article[1][1] and '/politics/' not in article[1][1] and '/defense/' not in \
                        article[1][1] and '/society/' not in article[1][1] and '/emergencies/' not in article[1][1] and \
                        '/military-operation-in-ukraine/' not in article[1][1] and '/russia/' not in article[1][1] and \
                        '/pressreview/' not in article[1][1] and '/russias-foreign-policy/' not in article[1][1]:
                    hungiepanda = hungiepanda.drop(hungiepanda[hungiepanda['Link'] == article[1][1]].index)
        elif 'rt.com' in article[1][0]:
            if ('/russia/' not in article[1][1] and '/news/' not in article[1][1] and '/actualidad/' not in
                    article[1][1] and '/russie/' not in article[1][1] and '/international/' not in article[1][1] and
                    '/inotv/' not in article[1][1] and '/opinions/'):
                hungiepanda = hungiepanda.drop(hungiepanda[hungiepanda['Link'] == article[1][1]].index)
        elif 'inosmi' in article[1][0] or 'ИноСМИ' in article[1][0]:  # ИноСМИ is the Russian domain
            if '/20' not in article[1][1]:
                hungiepanda = hungiepanda.drop(hungiepanda[hungiepanda['Link'] == article[1][1]].index)
        else:  # Anything falling into here is a new case that needs to be added in
            if 'ТАСС' != article[1][0] and 'RT на русском' != article[1][0] and 'Zee24tass' != article[1][0]:  # exceptions
                print(article[1][0] + " " + article[1][1])
    hungiepanda.to_csv('data.csv', index=False)


# Takes in text of any language as input, returns English translated text
def translate(text):
    to_translate = re.split(r'[,!?;:.\n\t]', text)
    translated = ''
    for word in to_translate:
        try:
            translated += GoogleTranslator(source='auto', target='en').translate(word) + ' '
        except TypeError:
            translated += word + ' '
    return translated


# Adds removed articles to a file where they can be auto-removed if re-added later
def flagged_article(link):
    data = [link]
    with open(r'flagged_articles.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


# Removes flagged articles
def remove_flags():
    print('Removing flagged articles...')
    detective_panda = pd.read_csv('flagged_articles.csv')  # Detective panda tracks down flags and crime
    suspicious_panda = pd.read_csv('data.csv')   # Suspicious panda is full of flags, or is it?
    for index, link in detective_panda.iterrows():
        for it, li in suspicious_panda.iterrows():
            if li['Link'] == link['Link']:
                suspicious_panda = suspicious_panda.drop(it)
                suspicious_panda.to_csv('data.csv', index=False)


# Removes articles that precede the Russia invasion of Ukraine
def check_date():
    elder_panda = pd.read_csv('data.csv')  # Panda may be a bit dated
    for index, link in elder_panda.iterrows():
        if int(link['Date'][-4:]) < 2022:
            print('Outdated: ' + link['Link'])
            elder_panda = elder_panda.drop(index)
            elder_panda.to_csv('data.csv', index=False)


"""
Uses SerpAPI to gather Google search data on top Russian media outlets. This will allow us to use indexed Google search
data as a database, wherein we can gather news articles pertaining to a list of input phrases.

Top outlets include: Sputnik, RIA Novosti, inoSMI, TASS, and Interfax.

Due to Google News search limitations we can only achieve 100 results per search. Each search combines a search term
from our common labels which was created based on our summer research along with a specified domain, updated to keep up
to date with current disinformation tactics.

Queries shown below were the last queries ran prior to updating the public version of this repo and are not indicative
of the latest queries ran internally.
"""
import csv
from serpapi import GoogleSearch  # Performs Google News searches
import dataCleanup  # contains methods for cleaning .csv data
import time

queries = {  # 1 = Disinformation, 0 = Pro-information
    'sputnikglobe.com': [1, 'Ukraine', 'Ukrainian+Nazi', 'Ukraine+War+Cost', 'nuclear', 'Kursk', 'Ukrainian+Terrorism'],
    'tass.com': [1, 'Ukraine', 'Ukraine+War+Cost', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces', 'summit+on+peace',
                 'nuclear', 'NATO', 'Kursk', 'Article+51', 'Ukrainian+Terrorism', 'Zaporizhzhia'],
    'rt.com': [1, 'Ukraine', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces', 'summit+on+peace', 'nuclear', 'NATO',
               'Kursk', 'Ukrainian+Terrorism'],
    'apnews.com': [0, 'Ukraine', 'Ukrainian+Nazi', 'Ukraine+War+Cost', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces',
                   'summit+on+peace', 'nuclear', 'Navy+Day', 'Okhmatdyt', 'NATO'],
    'reuters.com': [0, 'Ukraine', 'Ukrainian+Nazi', 'Ukraine+War+Cost', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces',
                    'summit+on+peace', 'nuclear', 'Navy+Day', 'Okhmatdyt', 'NATO'],
    'npr.org': [0, 'Ukraine', 'Ukrainian+Nazi', 'Ukraine+War+Cost', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces',
                   'summit+on+peace', 'nuclear', 'Navy+Day', 'Okhmatdyt', 'NATO'],
    'bbc.com': [0, 'Ukraine', 'Ukrainian+Nazi', 'Ukraine+War+Cost', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces',
                   'summit+on+peace', 'nuclear', 'Navy+Day', 'Okhmatdyt', 'NATO'],
    'pbs.org': [0, 'Ukraine', 'Ukrainian+Nazi', 'Ukraine+War+Cost', 'Volodymyr+Zelenskyy', 'Ukrainian+Armed+Forces',
                   'summit+on+peace', 'nuclear', 'Navy+Day', 'Okhmatdyt', 'NATO']
}


def query(term, domain, flag):  # Performs Google News searches with SerpAPI
    params = {
        "engine": "google_news",
        "q": term + " site:" + domain,
        "api_key": NoneofYourBusiness.api()  # My API key is NoneofYourBusiness
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['news_results']
    print(organic_results)

    field_names = ['Source', 'Link', 'Date', 'Disinformation', 'Title', 'Text', 'Translated', 'Tokenized']
    articles = []
    for result in organic_results:
        if 'rt.com' in result['source']['name'] and result['source']['name'] != 'rt.com':
            continue  # other variations of rt.com have html headers that differ from language to language
        article_data = {
            'Source': result['source']['name'],
            'Link': result['link'],
            'Date': result['date'][:10],
            'Disinformation': flag,
            'Title': 0,
            'Text': 0,
            'Translated': 0,
            'Tokenized': 0
        }
        print(article_data)
        articles.append(article_data)

    with open('data.csv', 'a', newline='', encoding='utf-8') as data:
        writer = csv.DictWriter(data, fieldnames=field_names)
        writer.writerows(articles)


def search_articles():
    for source in queries:  # Iterates through terms and domains
        for search in queries[source]:
            if search == 0 or search == 1:  # Ignore disinfo/proinfo flag
                pass
            else:
                try:
                    query(search, source, queries[source][0])
                except KeyError:  # returns KeyError when no results are returned for a given query
                    continue
                time.sleep(60)


search_articles()  # Gather articles with SerpAPI

dataCleanup.remove_duplicates()  # Removes duplicate items from dataset

dataCleanup.check_date()  # Removes articles that precede the Russia invasion of Ukraine

dataCleanup.remove_bad_links()  # Removes bad links based on url for each domain

dataCleanup.remove_flags()  # Removes flagged articles

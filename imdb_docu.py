'''aims to scrape and save all documentaries listed at IMDB. '''

import requests
import re
from bs4 import BeautifulSoup as bs4
import os
from urllib import urlretrieve
import pandas as pd

DF = []

def get(url):
    '''Like open(url), but cached'''
    filename = str(hash(url) + 2**32)
    if not os.path.exists(filename):
        #urlretrieve(url, filename)
        pass
    return open(filename)

def connected_to_internet(url='http://www.google.com/', timeout=5):
    'Checks if internet is available. Returns False if not.'
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print "No internet connection available."
    return False

def getdetails(film):
    '''scrapes details of each movie and saves it'''

    temp = film.find('span', attrs={'class':'value'})
    rating = temp.text if temp else 'UNRATED'
    temp = film.find('span', attrs={'class':'year_type'})
    year = temp.text if temp else ''
    temp = film.find('span', attrs={'class':'outline'})
    desc = temp.text if temp else ''
    temp = film.find('span', attrs={'class':'runtime'})
    runtime = temp.text if temp else ''
    temp = film.find('td', attrs={'class':'sort_col'})
    usbo = temp.text if temp else ''
    temp = film.find('span', attrs={'class':'genre'})
    genre = temp.text if temp else ''

    url = film.find('a')['href']
    name = film.find('a')['title']
    temp = film.find('span', attrs={'class':'titlePageSprite'})
    cert = temp['title'] if temp else ''
    temp = film.find('div', attrs={'class':'rating-list'})
    temp = re.findall(r'[\d,]+ votes', temp['title']) if temp else ''
    votes = temp[0] if temp else ''
    
    #print genre, cert, rating, year, runtime, url, name, usbo, desc, votes
    DF.append([genre, cert, rating, year, runtime, url, name, usbo, desc, votes])


def scrapepage(page):
    '''parses movies from each url'''
    page = bs4(page)
    movies = page.findAll('tr', attrs={'class':'detailed'})
    for film in movies:
        getdetails(film)
    


def imdb_recos():
    '''from each page get recommendations, number of users
    who voted, metacritic score.'''
    pass

if __name__ == '__main__':
    
    URL = 'http://www.imdb.com/search/title?sort=boxoffice_gross_us&start={:d}&title_type=documentary'
    STARTAT, LIMIT = 1, 4000
    
    for i in range(STARTAT, LIMIT):
        #print i, i*50+1
        scrapepage(get(URL.format(i*50+1)))
        
    pd.DataFrame(DF).to_csv("IMDB Docu.csv", index=False, encoding="utf-8")

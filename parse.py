from BeautifulSoup import BeautifulSoup
import urllib
import re

USER = 'alphabethos'

def fetch_stations(user):
    tokens = ['0081d3c8e037f4c32a44f01b1701dd31466957fc96e4da2e', 'db592464bbca03e7664b1093336f121ce8c7587b2172781c']
    return tokens

def fetch_tracks(stations):
    for station in stations:
        page = urllib.urlopen('http://www.pandora.com/favorites/station_tablerows_thumb_up.vm?token=' + station + '&sort_col=thumbsUpDate')
        page = BeautifulSoup(page)
        titles = []
        artists = []
        for span in page.findAll('span', attrs={'class':'track_title'}):
            for attr, value in span.attrs:
                if attr == 'tracktitle':
                    titles.append(value)
        for anchor in page.findAll('a'):
            artists.append(anchor.string)
        if len(titles) == len(artists):
            i = 0
            for title in titles:
                print '<a href=\'http://youtube.com/results?search_query=' + urllib.quote_plus(title + ' ' + artists[i]) + '\'>' + title + '</a> by', artists[i], '<br>'
                i += 1
        else:
            print 'parsing error'

def main():
    stations = fetch_stations(USER)
    fetch_tracks(stations)

if __name__ ==  "__main__":
    main()


__author__ = ("Dylan Lloyd <dylan@psu.edu>")
__license__ = "BSD"

# SETTINGS

USER = 'alphabethos'
# END OF SETTINGS

import urllib
from BeautifulSoup import BeautifulSoup

def fetch_stations(user):
    stations = []
    page = urllib.urlopen('http://www.pandora.com/favorites/profile_tablerows_station.vm?webname=' + USER)
    page = BeautifulSoup(page)
    table = page.findAll('div', attrs={'class':'station_table_row'})
    for row in table:
        if row.find('a'):
            for attr, value in row.find('a').attrs:
                if attr == 'href':
                    stations.append(value[10:])
    return stations

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

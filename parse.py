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
        search_urls = []
        for span in page.findAll('span', attrs={'class':'track_title'}):
            for attr, value in span.attrs:
                if attr == 'tracktitle':
                    titles.append(value)
        for anchor in page.findAll('a'):
            artists.append(anchor.string)
        if len(titles) == len(artists):
            i = 0
            for title in titles:
                search_url = 'http://yt.com/results?search_query=' + urllib.quote_plus(title + ' ' + artists[i])
                search_urls.append(search_url)
                print '<a href=\'' + search_url +'\'>' + title + '</a> by', artists[i], '<br>'
                i += 1
        else:
           pass  ## ERROR
    return search_urls

def fetch_videos(search_urls):
    for url in search_urls:
        page = urllib.urlopen(url)
        page = BeautifulSoup(page)
        result = page.find(attrs={'class':'yt-video-box'})
        print result
        for attr, value in result.contents[1]:
            print value

def main():
    stations = fetch_stations(USER)
    search_urls = fetch_tracks(stations)
    fetch_videos(search_urls)

if __name__ ==  "__main__":
    main()

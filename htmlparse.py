#!/usr/bin/env python
from HTMLParser import HTMLParser
import urllib

USER = 'alphabethos'

class parse(HTMLParser):

    def __init__(self, data, mode):
        HTMLParser.__init__(self)
        print mode
        self.__in_row = False
        self.station_tokens = []
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr, value in attrs:
                if attr == 'class' and value == 'station_table_row':
                    self.__in_row = True
                    continue
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and self.__in_row:
                    self.station_tokens.append(value[10:])
                    continue

    def handle_data(self, text):
        pass

    def handle_endtag(self, tag):
        self.__in_row = False
        pass


page = urllib.urlopen('http://www.pandora.com/favorites/profile_tablerows_station.vm?webname=' + USER).read()
#page = urllib.urlopen('http://www.pandora.com/favorites/station_tablerows_thumb_up.vm?token=' + station + '&sort_col=thumbsUpDate')
#page = urllib.urlopen(search_url)
p = parse(page, 'stations')
p = parse(page, 'tracks')
print p.station_tokens

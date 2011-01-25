#!/usr/bin/env python
from HTMLParser import HTMLParser
import urllib

class pandora_fetch(HTMLParser):

    def __init__(self, user):
        HTMLParser.__init__(self)
        self.user = user
        self.stations = []
        self.tracks = {}
        self.__in_row = False
        self.__in_track = False
        self.__current_track = None
        self.__mode = 'stations'
        page = urllib.urlopen('http://www.pandora.com/favorites/profile_tablerows_station.vm?webname=' + self.user).read()
        self.feed(page)
        self.__mode = 'tracks'
        for station in self.stations:
            page = urllib.urlopen('http://www.pandora.com/favorites/station_tablerows_thumb_up.vm?token=' + station + '&sort_col=thumbsUpDate').read()
            self.feed(page)

    def handle_starttag(self, tag, attrs):
        if self.__mode == 'stations':
            if tag == 'div':
                for attr, value in attrs:
                    if attr == 'class' and value == 'station_table_row':
                        self.__in_row = True
                        continue
            if self.__in_row and tag == 'a':
                for attr, value in attrs:
                    if self.__in_row and attr == 'href':
                        self.stations.append(value[10:])
                        continue
        if self.__mode == 'tracks':
            if tag == 'span':
                for attr, value in attrs:
                    if attr == 'class' and value == 'track_title':
                        self.__in_track = True
                        continue
                    if attr == 'tracktitle':
                        self.__current_track = value

    def handle_data(self, text):
        if self.__in_track:
            self.tracks[self.__current_track] = text

    def handle_endtag(self, tag):
        if tag == 'div':
            self.__in_row = False
        if tag == 'a':
            self.__in_track = False
            self.__current_track = None

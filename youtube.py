#!/usr/bin/env python

from HTMLParser import HTMLParser
import urllib
from doit import pandora_fetch

USER = 'alphabethos'
user_data = pandora_fetch(USER)


searches = []
for title, artist in user_data.tracks.iteritems():
    search = title + " " + artist
    searches.append(search)

class search_youtube(HTMLParser):

    def __init__(self, search_terms):
        HTMLParser.__init__(self)
        self.track_ids = []
        for search in search_terms:
            self.__in_result = False
            search = urllib.quote_plus(search)
            query = 'http://youtube.com/results?search_query='
            page = urllib.urlopen(query + search).read()
            self.feed(page)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            track_id = ''
            for attr, value in attrs:
                if attr == 'class' and value == 'video-main-content':
                    self.__in_result = True
                if attr == 'id':
                    track_id = value
            if self.__in_result and len(track_id[19:]) == 11:
                self.track_ids.append(track_id[19:])
                print track_id[19:]
                self.__in_result = False

    def handle_endtag(self, tag):
        pass



results = search_youtube(searches)

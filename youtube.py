#!/usr/bin/env python

from HTMLParser import HTMLParser, HTMLParseError
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
            url = 'http://youtube.com/results?search_query='
            connection = urllib.urlopen(url + search)
            encoding = connection.headers.getparam('charset')
            page = connection.read()
            page = page.decode(encoding)
            try:
                self.feed(page)
            except UnicodeDecodeError:
                print 'problem decoding', url + search
            except HTMLParseError:
                # There is no way to override HTMLParseError and
                # continue parsing, see:
                # http://bugs.python.org/issue755660
                # But the data is there!
                print 'problem parsing', url + search

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
                self.__in_result = False


results = search_youtube(searches)
print results.track_ids

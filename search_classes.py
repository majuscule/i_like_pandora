#!/usr/bin/env python

from HTMLParser import HTMLParser, HTMLParseError
import urllib

class pandora_fetch(HTMLParser):
    """ This class should be initiated with a Pandora account username. It exposes a list of tracks `self.tracks` and a dictionary of title->artist pairs `tracks`.
    """

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
        if len(self.stations) == 0:
            print 'Are you sure your pandora profile is public? Can\'t seem to find any stations listed with your account.'
            return 1
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


class search_youtube(HTMLParser):
    """ This class should be initiated with a list of search terms. It exposes a list of YouTube video ids `self.track_ids`.  """

    def __init__(self, search_terms):
        self.track_ids = []
        for search in search_terms:
            HTMLParser.__init__(self)
            page = ''
            self.__in_search_results = False
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
            except UnicodeEncodeError:
                print 'problem encoding', url + search
            except HTMLParseError:
                # There is no way to override HTMLParseError and
                # continue parsing, see:
                # http://bugs.python.org/issue755660
                # But the data is there!
                print 'problem parsing', url + search
            except found_video:
                pass

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr, value in attrs:
                if attr == 'id' and value == 'search-results':
                    self.__in_search_results = True
        if self.__in_search_results:
            for attr, value in attrs:
                if attr == 'href' and value[:-11] == '/watch?v=' and len(value[9:]) == 11:
                    self.track_ids.append(value[9:])
                    self.__in_search_results = False
                    #self.reset()
                    # Calling self.reset() causes the following error:

                    # File "/usr/lib/python2.6/HTMLParser.py", line 108, in feed self.goahead(0)
                    # File "/usr/lib/python2.6/HTMLParser.py", line 148, in goahead k = self.parse_starttag(i)
                    # File "/usr/lib/python2.6/HTMLParser.py", line 229, in parse_starttag endpos = self.check_for_whole_start_tag(i)
                    # File "/usr/lib/python2.6/HTMLParser.py", line 305, in check_for_whole_start_tag
                    # raise AssertionError("we should not get here!")

                    # I can't figure out why that's happening. I've
                    # discovered that calling HTMLParser.__init__(self)
                    # inside the search term loop in self.__init__ also
                    # resets the instance. The instance must be reset to
                    # accept a new page with self.feed(). Until a better
                    # solution is found:
                    raise found_video

class found_video(BaseException):
    """ Exception class to throw after finding a video to stop HTMLParser. """
    pass

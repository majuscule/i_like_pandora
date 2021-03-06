#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ("Dylan Lloyd <dylan@psu.edu>")
__license__ = "BSD"

default_options = {
    'notifications' : 'true',
    # NOTIFICATIONS must be a string due to issues noted here:
    # http://bugs.python.org/issue974019
    # ConfigParser.getboolean fails when falling back to the default value
    # if the value type is bool.
    'youtube-dl' : '/usr/bin/youtube-dl',
    'default_icon' : '/usr/share/icons/gnome/48x48/mimetypes/gnome-mime-application-x-shockwave-flash.png',
    'youtube-dl_options' : '--no-progress --ignore-errors --continue --max-quality=22 -o "%(stitle)s---%(id)s.%(ext)s"'
}

import ConfigParser # This module has been renamed to configparser in python  3.0
import sys
import os

CONFIG_FILE= os.path.join(os.path.expanduser('~'), '.i_like_pandora.config')
config = ConfigParser.ConfigParser(default_options)
loaded_files = config.read(CONFIG_FILE) # config.read returns an empty array if it fails.
if len(loaded_files) == 0:
    print 'Can\'t find a configuration file at', CONFIG_FILE
    sys.exit()
try:
    USER = config.get('settings', 'username')
    DIR = os.path.expanduser(config.get('settings', 'download_folder'))
    NOTIFICATIONS = config.getboolean('settings', 'notifications')
    YT_DL = config.get('settings', 'youtube-dl')
    DEFAULT_ICON = config.get('settings', 'default_icon')
    YT_OPT = default_options['youtube-dl_options']
except:
    print 'There is a formatting error in the configuration file at', CONFIG_FILE
    sys.exit()

from search_classes import pandora_fetch, search_youtube, found_video
import urllib
import urllib2
import re
import copy
import shlex, subprocess

if NOTIFICATIONS:
    import pynotify
    import hashlib
    import tempfile
    import string

def fetch_tracks(stations):
    """ Takes a list of station tokens and returns a list of Title + Artist strings.
    """
    search_strings = []
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
                search_string = title + ' ' + artists[i]
                search_strings.append(search_string)
                i += 1
        else:
            # This would mean something strange has happened: there
            # aren't the same number of titles and artist names on a
            # station page.
            pass
    return search_strings

def check_for_existing(video_list):
    """ Checks the download-folder for existing videos with same id and removes from video_list. """
    filelist = os.listdir(DIR)
    i = 0
    for video in copy.deepcopy(video_list):
        for files in filelist:
            if re.search(video,files):
                del video_list[i]
                i -= 1
        i += 1
    return video_list

def fetch_videos(video_list):
    """ Uses subprocess to trigger a download using youtube-dl of the list created earlier, and triggers notifications if enabled. """
    os.chdir(DIR)
    args = shlex.split(YT_DL + ' ' + YT_OPT)
    if NOTIFICATIONS: regex = re.compile("\[download\] Destination: (.+)")
    for video in video_list:
        if video:
            thread = subprocess.Popen(args + ["http://youtube.com/watch?v=" + video], stdout=subprocess.PIPE)
            output = thread.stdout.read()
            if NOTIFICATIONS:
                video_file = regex.findall(output)
                if len(video_file) == 0:
                    break
                thumbnail = hashlib.md5('file://' + DIR + video_file[0]).hexdigest() + '.png'
                # Two '/'s instead of three because the path is
                # absolute; I'm not sure how this'd work on windows.
                title, sep, vid_id = video_file[0].rpartition('---')
                title = string.replace(title, '_', ' ')
                thumbnail = os.path.join(os.path.expanduser('~/.thumbnails/normal'), thumbnail)
                if not os.path.isfile(thumbnail):
                    opener = urllib2.build_opener()
                    try:
                        page = opener.open('http://img.youtube.com/vi/' + video + '/1.jpg')
                        thumb = page.read()
                        # The thumbnail really should be saved to
                        # ~/.thumbnails/normal (Thumbnail Managing
                        # Standard)
                        # [http://jens.triq.net/thumbnail-spec/]
                        # As others have had problems anyway
                        # (http://mail.gnome.org/archives/gnome-list/2010-October/msg00009.html)
                        # I decided not to bother at the moment.
                        temp = tempfile.NamedTemporaryFile(suffix='.jpg')
                        temp.write(thumb)
                        temp.flush()
                        note = pynotify.Notification(title, 'video downloaded', temp.name)
                    except:
                        note = pynotify.Notification(title, 'video downloaded', DEFAULT_ICON)
                else:
                    # Generally, this will never happen, because the
                    # video is a new file.
                    note = pynotify.Notification(title, 'video downloaded', thumbnail)
                note.show()

def main():
    stations = pandora_fetch(USER)
    searches = []
    for title, artist in stations.tracks.iteritems():
       search = title + " " + artist
       searches.append(search)
    videos = search_youtube(searches);
    videos = check_for_existing(videos.track_ids)
    fetch_videos(videos)

if __name__ ==  "__main__":
    main()

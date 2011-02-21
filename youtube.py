#!/usr/bin/env python

from HTMLParser import HTMLParser, HTMLParseError
import urllib
#from doit import pandora_fetch
#
#USER = 'alphabethos'
#user_data = pandora_fetch(USER)
#
#
#searches = []
#for title, artist in user_data.tracks.iteritems():
    #search = title + " " + artist
    #searches.append(search)

searches = ['Sugarcube Yo La Tengo', "Runnin' [Philippians Rmx] The Pharcyde", 'Take Me Out Franz Ferdinand', 'Our Remains Bitter:Sweet', 'Clan Primate Heys', 'In Remembrance  Exile', 'Point Of No Return Dead Moon', "What's Golden Jurassic 5", "If It Wasn't For You (feat. De La Soul And Starchild Excalibur) Handsome Boy Modeling School", '505 Arctic Monkeys', 'Sea Legs The Shins', 'Breathe Telepopmusik', 'Back 4 U (live) Jurassic 5', 'Cretin Hop The Ramones', 'The Modern Age The Strokes', 'Naive The Kooks', 'No Buses Arctic Monkeys', 'Concrete Schoolyard Jurassic 5', 'Cause = Time Broken Social Scene', 'Conquer  ABK', 'Hip Hop Dead Prez', 'Electro Sixteen Benny Benassi', 'Nights Introlude (Radio Edit) Nightmares On Wax', "Don't Ask Me Ok Go", 'She Does Locksley', 'Storm Vibrations Guided By Voices', 'Change Mr. J. Medeiros', 'Soma The Strokes', 'Rampage EPMD', "Don't Make Me Wait Locksley", 'Love And Emotion [Instrumental] Benny Benassi', 'Teddy Picker Arctic Monkeys', 'Crazy Gnarls Barkley', "Spittin' Images Exile (Producer)", "Simply Amazin' - Steel Blazin'  Exile", 'Cao J. Rawls', 'Show Me Love  Laidback Luke', 'Back Home (The Return) Common Market', '100% Dundee The Roots', 'Cigarette Smoker Fiona (Live) Arctic Monkeys', 'Someday The Strokes', 'Here It Goes Again Ok Go', 'Fell In Love With A Girl The White Stripes', 'Mr. Brown Styles Of Beyond', 'Stacie Anne The Fratellis', 'The Uh-Huh The Pharcyde', u'Get Up (D.O.N.S. & DBN Remix) Niki Belucci', 'Anti-Matter King Geedorah', 'Wait For Me The Pigeon Detectives', 'Around The World/Harder Better Faster Stronger (Live) Daft Punk', 'Loud Pipes Ratatat', "Ain't No Rest For The Wicked Cage The Elephant", 'Local Boy The Rifles', 'The Way It Is The Strokes', 'Heart In A Cage The Strokes', 'Blu Collar Worker  Exile', 'What You Want The Roots', 'Be Still (Extended Mix) Kaskade', 'Kill The Director The Wombats', "Why Don't You Gramophonedzie", 'Only One Chris Lake', u'Come Fly Away (Soha & Adam K Remix) Benny Benassi', 'Cry For You (Radio Mix) September', 'Not Alone (Deadmau5 Instrumental) Gianluca Motta', 'Cigarette Smoker Fiona Arctic Monkeys', 'D Is For Dangerous Arctic Monkeys', 'Small Town Girl Good Shoes', 'Rapp Snitch Knishes (Mr. Fantastik) MF Doom', "93 'til Infinity Souls Of Mischief", 'Call On Me (Eric Prydz Vs Retarded Funk Remix) Eric Prydz', 'Perhaps Vampires Is A Bit Strong But.. Arctic Monkeys', 'Us And Them Pink Floyd', 'Weight Of The World Pigeon John', "Don't Look Back Telepopmusik", 'Get Over It Ok Go', 'Get What I Want Bitter:Sweet', "We're A Happy Family The Ramones", 'Fight For You Morgan Page', 'Dancing In The Rain  Exile', 'Jerk It Out Caesars', 'Automatic Stop The Strokes', 'Nas Is Like Nas', 'Sheena Is A Punk Rocker The Ramones', 'Too Long/Steam Machine (Live) Daft Punk', 'Dance To My Ministry Brand Nubian', 'Tell Me Why (Radio Edit) Supermode', 'Trying Your Luck The Strokes', 'Chelsea Dagger The Fratellis', "Sinnerman (Felix Da Housecat's Heavenly House Mix) Nina Simone", 'The Choice Is Yours (Revisited) Black Sheep', 'All That You Are The Foreign Exchange', 'Old Yellow Bricks Arctic Monkeys', 'Alive With The Glory Of Love Say Anything', 'Work the Angles Dilated Peoples', 'Two And Two Talib Kweli', 'Last Hour Elliott Smith', "All These Things That I've Done The Killers", 'Romantic Type The Pigeon Detectives', 'Turn Off The Radio Dead Prez', 'Kick In The Door The Notorious B.I.G.', 'Sonic Reducer The Dead Boys', 'One Beer MF Doom', 'Go That Deep (Skylark Vocal Remix) Nufrequency', 'Brooklyn Go Hard Jay-Z', 'I Remember  Deadmau5', 'Feel Lonely Alex Monakhov', 'All That You Are (Remixes Blend) Nicolay', 'Diferente Gotan Project', "Runnin' [Philippians Rmx Instrumental] The Pharcyde", 'The Narrow Path (Instrumental) Blu', 'Riot Van Arctic Monkeys', 'Fine And Free Guru', 'Hip 2 The Skeme The Coup', 'Cana*T Control Myself The Pigeon Detectives', 'Hell On Earth (Front Lines) Mobb Deep', 'The World Is Yours Nas', 'I Bet You Look Good On The Dancefloor Arctic Monkeys', "I'll Be Your Man The Black Keys", 'Trouble Bitter:Sweet', 'Careful Television', 'Mastermind Deltron 3030', 'Glory Box Portishead', 'Pavadita Color Tango De Roberto Alvarez', 'Are You Gonna Be My Girl? Jet', 'World, Hold On Bob Sinclar', 'Incinerate Sonic Youth', 'Radio Freq Dead Prez', 'Anarchy In The UK (Live) Sex Pistols', 'All For You RJD2', 'Go It Alone Beck', 'Psychotic Girl The Black Keys', 'Dull Life Yeah Yeah Yeahs', 'Broke Up The Time The Futureheads', 'Leave Before The Lights Come On Arctic Monkeys', 'Children (Club Radio Edit) 4 Clubbers', 'Baditude (Original Club Mix)  Obernik', 'Topographic Darkleaf', 'Miami 2 Ibiza (Instrumental) Swedish House Mafia', 'The Island Pt. II (Dusk) Pendulum', 'WAR Little Brother', 'Meet Me Halfway (At The Remix) (Will.I.Am Remix) Black Eyed Peas', 'Milonga Astor Piazzolla', 'Heads Will Roll Yeah Yeah Yeahs', "I Don't Know Badi", 'Forest Whitiker Brother Ali', 'Perfect Moments (Official Airport Jam (Radio Edit)  Yep', "Groovin' Kero One", 'Da Hype Junior Jack', 'I Used To Love H.E.R. Common', 'All Over Again Locksley', 'Close Edge Mos Def', 'The Longest Road Morgan Page', 'Migraine Headache (feat. ICP) Esham', 'Bittersweet Faith Bitter:Sweet', 'Deep Fried Frenz MF Doom', 'This House Is A Circus Arctic Monkeys', 'Red Light The Strokes', 'Rain (Cosmic Gate Remix) Armin Van Buuren', 'Dona*T Know How To Say Goodbye The Pigeon Detectives', "Roadkill (Edx's Alcapulco At Night Remix) Dubfire", 'Halftime Nas', 'Apes From Space (Dirtyloud Remix) Aaren San', 'Bigger Boys And Stolen Sweethearts Arctic Monkeys', 'The Narrow Path Blu', "Chillin' Modjo", 'Below The Heavens Pt. II  Exile', 'Police On My Back The Clash', 'The Scene Is Dead We Are Scientists', "Coastin' Zion I", 'Bulletproof (Live At Shepherds Bush Empire, London) La Roux', 'Lost In The Post The Wombats', 'Whatever Lola Wants (Gotan Project Remix) Sarah Vaughan', 'Calabria 2008 Enur', 'Kings County Ming + FS', 'Mr. Brightside The Killers', 'Last Nite The Strokes', 'No Chance Soulstice (Rap)', 'Lady Modjo', 'Be Healthy Dead Prez', 'Repeated Offender The Rifles', "You Can't Hide, You Can't Run Dilated Peoples", 'Wusgood Clutch Players', "Azzurra (It's Not The Same Version) Gui Boratto", 'Picture The Blakes', 'Skills Gang Starr', 'Ghostwriter RJD2', 'Go! Common', 'Heads Will Roll (A-Trak Dub Mix) Yeah Yeah Yeahs', 'Red House Jimi Hendrix', 'Poker Face (Jody Den Broeder Remix) Lady Gaga', 'Hate To Say I Told You So The Hives', 'The Who Hieroglyphics', 'Stormy Weather The Kooks', 'Desert Eagle Ratatat', "You Probably Couldn't See For The Lights But You Were Staring Straight At Me Arctic Monkeys", 'All Men Are Freezing Robert Pollard', 'For The Girl The Fratellis', 'See No Evil Television', 'Aerodynamic (Daft Punk Remix) Daft Punk', 'Sandstorm Darude', 'White Knight Two Surkin', 'Hang Me Up To Dry Cold War Kids', 'Burning The Whitest Boy Alive', 'Mistress Mabel The Fratellis', 'Rite Where U Stand Gang Starr', 'YGM Atmosphere', 'One Swedish House Mafia', 'Buttons (Markus Schulz Vocal Mix) Sia', "I Don't Care Black Flag", 'One More Time/Aerodynamic (Live) Daft Punk', 'You Wish Nightmares On Wax', 'Meet Me Halfway (DJ Ammo/Poet Named Life Remix) Black Eyed Peas', 'Heartbeats (Extended Mix) Grum']

print 'starting with ', len(searches), 'searches.'

class search_youtube(HTMLParser):

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


#results = search_youtube(searches)
#print results.track_ids

# Create your views here.
from django.shortcuts import render_to_response
import wmTippspiel
from wmTippspiel.appWMTippspiel.views import punkteAuswerten

import feedparser


def feed(request):
    ## Extracts the information from the feedURL = 'http://de.fifa.com/worldcup/news/rss.xml'
    #  @param self The object pointer.
    #  @param feedURL The URL of the feed as a String
    #  @return A HTML-String with the extracted feed information
    #feedURL = 'http://de.fifa.com/worldcup/news/rss.xml'  
    #feed = feedparser.parse(feedURL)
    
    feed = feedStart(request)
    #punkteListe = wmTippspiel.appWMTippspiel.views.punkteAuswerten(request)
    punkteListe = punkteAuswerten(request)
    
    return render_to_response('appWMTippspiel/index.html',
                             # {'entries': feed.entries[0:10]})
                              {'entries': feed.entries[0:10],'punkteListe': punkteListe[0:16]})
    
    
def feedStart(request):
    ## Extracts the information from the feedURL = 'http://de.fifa.com/worldcup/news/rss.xml'
    #  @param self The object pointer.
    #  @param feedURL The URL of the feed as a String
    #  @return A HTML-String with the extracted feed information
    feedURL = 'http://de.fifa.com/worldcup/news/rss.xml'  
    feed = feedparser.parse(feedURL)
    
    return feed

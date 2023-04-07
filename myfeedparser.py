# A Feed Parser written to be able to solve Problem Set 5 from MIT's OCW 6.0001 Fall 2016
# Written by: Andre Soeiro (https://github.com/afsoeiro)

# Sorry for the lack of commentaries. I just wanted to solve this issue at this time.
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

class Entry(object):
    def __init__(self, title, link, guid, description, pubdate):
        self.title = title
        self.link = link
        self.guid = guid
        self.description = description
        self.pubdate = pubdate
    
    def __str__(self):
        ret = ''
        ret += self.title + '\n'
        ret += self.link + '\n'
        ret += self.guid + '\n'
        ret += self.description + '\n'
        ret += self.pubdate
        return ret


def fetch_url(_url):
    """
    Fetches a rss url xml and retrieves all items from all channels
    _url(string): the rss url to fetch
    returns: a list of Entry objects, that contain strings with title, link, guid, description and pubdate
    """
# Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    uh = urllib.request.urlopen(_url, context=ctx)

    data = uh.read()

    root = ET.fromstring(data)
    channels = root.findall("channel")
    entries = []
    for channel in channels:
        items = channel.findall("item")
        for item in items:
            title = get_text(item.find("title"))
            link = get_text(item.find("link"))
            guid = get_text(item.find("guid"))
            description = get_text(item.find("description"))
            pubdate = get_text(item.find("pubDate"))
            entries.append(Entry(title, link, guid, description, pubdate))
    return entries

def get_text(item):
    if item != None:
        return item.text
    return ""

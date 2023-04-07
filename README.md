# MITOCW60001-PS5_workaround
## This is a workaround to get ps5 to work retrieving the news items


When I tried to solve this problem, I noticed the file ps5.py would not download the RSS feed items from google and yahoo news sites. This happened when I reached the filtering section, right before Problem 10 from PS5.


I investigated to see why it was not working. Apparently, there was some problem with the feedparser.py file. The specifications from both google and yahoo may have changed somehow.


I built this rudimentary feed parser to substitute the supplied parser and found the necessary changes to finish *[Problem Set 5](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/pages/assignments/)* from **[MIT OCW 6.00001 - Introduction To Computer Science And Programming In Python - Fall 2016](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/)**.

These are the changes that worked for me *(somehow)*:
1. Install the [datefinder](https://pypi.org/project/datefinder/) library:
```
pip intstall datefinder
```

1. Add the file `myfeedparser.py` *(source below)* to the same directory of the other source files

2. Changes in the file `ps5.py`


A. Remove 'import feedparser' from line 6 and add:
```python
import myfeedparser
import datefinder
```


B. Change the function `process(url)` to:
```python
    def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    entries = myfeedparser.fetch_url(url)
    ret = []
    # The following loop is now using information from the feedparser I developed
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.pubdate)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        except ValueError:
            matches = datefinder.find_dates(pubdate)

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret
```

That's about it. Once these changes are applied, it will load feeds from Google and Yahoo by running
```
$ python3 ps5.py
```

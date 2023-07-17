import feedparser

feed = feedparser.parse('https://feedparser.readthedocs.io/en/latest/examples/rss20.xml')

for item in feed.entries:
    print(item.title)
    print(item.link)
    print(item.description)
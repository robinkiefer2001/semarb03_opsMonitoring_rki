import feedparser

feed = feedparser.parse("https://wid.cert-bund.de/portal/wid/rss")
all_entries = feed.entries



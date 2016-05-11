import requests
import untangle
import os.path
import json


def list_shows_rss(url):
    xml = requests.get(url)
    root = untangle.parse(xml.text)
    items = root.rss.channel.item
    for item in items:
        guid = item.guid.cdata
        url = item.enclosure['url']
        title = item.title.cdata
        yield {'guid': guid, 'url': url, 'title': title}


def save_file(filename, items):
    with open(filename, 'w') as f:
        json.dump(items, f, sort_keys=True, indent=2)


def read_file(filename):
    if not os.path.exists(filename):
        return {}
    else:
        with open(filename) as f:
            return json.load(f)


class RssMgr(object):

    def __init__(self, list_shows, save_file, read_file):
        self.list_shows = list_shows
        self.save_file = save_file
        self.read_file = read_file
        self.items = self.read_file()

    def fetch_latest(self):
        items = {}
        for item in self.list_shows():
            items[item['guid']] = item

        return items

    def find_new(self, items):
        new_items = {}
        curr_items = set(self.items.keys())
        latest_items = set(items.keys())

        for new_item in latest_items.difference(curr_items):
            new_items[new_item] = items[new_item]

        return new_items

    def update(self):
        latest_items = self.fetch_latest()
        new_items = self.find_new(latest_items)
        self.save_file(latest_items)
        self.items = latest_items
        return new_items


def build_shows_rss_mgr(url, filename):
    return RssMgr(
        lambda: list_shows_rss(url),
        lambda items: save_file(filename, items),
        lambda: read_file(filename))

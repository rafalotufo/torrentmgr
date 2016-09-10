#!/usr/bin/env python

import requests
import argparse
import json


def create_magnet_link(search_term):
    url = 'https://yts.ag/api/v2/list_movies.json'
    r = requests.get(url, params={'query_term': search_term})
    print r.url
    results = r.json()
    movies = results['data']['movies']
    return [create_link(m) for m in movies]


def create_link(movie):
    result = {}
    torrents = movie['torrents']
    result['torrents'] = [mk_torrent(t) for t in torrents]
    result['title'] = movie['title']
    return result


def mk_torrent(t):
    return {
        'hash': t['hash'],
        'size': t['size_bytes'],
        'peers': t['seeds'],
        'seeds': t['seeds'],
        'quality': t['quality'],
        'magnet': mk_magnet(t['hash'])
    }


def mk_magnet(h):
    trackers = [
        'udp://open.demonii.com:1337/announce',
        'udp://tracker.openbittorrent.com:80',
        'udp://tracker.coppersurfer.tk:6969',
        'udp://glotorrents.pw:6969/announce',
        'udp://tracker.opentrackr.org:1337/announce',
        'udp://torrent.gresille.org:80/announce',
        'udp://p4p.arenabg.com:1337',
        'udp://tracker.leechers-paradise.org:6969'
    ]

    return 'magnet:?xt=urn:btih:%s&dn=Url+Encoded+Movie+Name&%s' % (h, '&'.join(['tr=%s' % t for t in trackers]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("search")
    args = parser.parse_args()

    for m in create_magnet_link(args.search):
        print json.dumps(m, indent=2)

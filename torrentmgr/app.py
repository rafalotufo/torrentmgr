#!/usr/bin/env python

import sys
import argparse
import rssmsg
import qbittorrentclient
import time
import os
import json

import logging
import logging.handlers


def run(feeds, feed_directory, client, username, password, update_every_s, my_logger):

    def update(rss_mgr):
        my_logger.info('updating...')
        new = rss_mgr.update()
        my_logger.info('found %s new items' % len(new))
        urls = [i['url'] for i in new.itervalues()]
        if urls:
            my_logger.info('downloading %d torrents' % len(urls))
            try:
                client.login(username, password)
                try:
                    client.add_torrent(urls)
                except:
                    my_logger.exception('Error adding torrent')
            except:
                my_logger.exception('Error logging in to bittorrent client')

    def update_all():
        rss_mgrs = list(build_rss_mgrs(feeds, feed_directory))
        for rss_mgr in rss_mgrs:
            update(rss_mgr)

    update_all()
    while True:
        time.sleep(update_every_s)
        update_all()


def get_logger():
    my_logger = logging.getLogger('TorrentMgr')
    my_logger.setLevel(logging.INFO)

    if sys.platform == "darwin":
        # Apple made 10.5 more secure by disabling network syslog:
        address = "/var/run/syslog"
    else:
        address = ('localhost', 514)

    handler = logging.handlers.SysLogHandler(address=address)
    my_logger.addHandler(handler)
    return my_logger


def get_feed_uris(feeds):
    with open(feeds) as f:
        return json.load(f)


def build_rss_mgrs(feeds, feed_directory):
    feed_uris = get_feed_uris(feeds)
    if not os.path.exists(feed_directory):
        os.mkdir(feed_directory)
    for feed_id, feed_uri in feed_uris.items():
        filename = os.path.join(feed_directory, feed_id) + '.json'
        yield rssmsg.build_shows_rss_mgr(
            feed_uri['uri'], feed_uri.get('should_contain', None), filename)


def main(feeds, feed_directory, update_every_s, web_api_url, username, password):

    my_logger = get_logger()
    client = qbittorrentclient.QbittorrentClient(web_api_url)
    run(feeds, feed_directory, client, username, password, update_every_s, my_logger)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--feeds', default="feeds.json")
    parser.add_argument('--feed-directory', default='.rssmgr')
    parser.add_argument('--web-api-url', default='http://192.168.1.199:8085')
    parser.add_argument('--username', default='rlotufo')
    parser.add_argument('--password', default='baleieza')
    parser.add_argument('-s', default=5 * 60, type=int)
    args = parser.parse_args()

    main(args.feeds, args.feed_directory, args.s, args.web_api_url, args.username, args.password)

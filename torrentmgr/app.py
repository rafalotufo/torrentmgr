#!/usr/bin/env python

import sys
import argparse
import rssmsg
import qbittorrentclient
import time

import logging
import logging.handlers


def run(rss_mgr, client, username, password, update_every_s, my_logger):

    def update():
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

    update()
    while True:
        time.sleep(update_every_s)
        update()


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


def main(url, filename, update_every_s, web_api_url, username, password):

    my_logger = get_logger()
    client = qbittorrentclient.QbittorrentClient(web_api_url)
    rss_mgr = rssmsg.build_shows_rss_mgr(url, filename)
    run(rss_mgr, client, username, password, update_every_s, my_logger)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--url',
        default='http://showrss.info/user/22730.rss?magnets=true&namespaces=true&name=clean&quality=null&re=null')
    parser.add_argument('--filename', default='.rssmgr.json')
    parser.add_argument('--web-api-url', default='http://192.168.1.199:8085')
    parser.add_argument('--username', default='rlotufo')
    parser.add_argument('--password', default='baleieza')
    parser.add_argument('-s', default=5 * 60, type=int)
    args = parser.parse_args()

    main(args.url, args.filename, args.s, args.web_api_url, args.username, args.password)

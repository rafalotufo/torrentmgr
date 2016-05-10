#!/usr/bin/env python

import argparse
import rssmsg
import qbittorrentclient
import time


def main(url, filename, update_every_s, web_api_url, username, password):

    def update():
        print 'updating...'
        new = rss_mgr.update()
        print 'found %s new items' % new
        urls = [i['url'] for i in new.itervalues()]
        if urls:
            print 'downloading %s' % ' '.join(urls)
            client.add_torrent(urls)

    def run():
        exit_app = False
        try:
            update()
            while not exit_app:
                time.sleep(update_every_s)
                update()
        except KeyboardInterrupt:
            print 'interrupt!'
            exit_app = True

    client = qbittorrentclient.QbittorrentClient(web_api_url)
    client.login(username, password)
    rss_mgr = rssmsg.buildShowsRssMgr(url, filename)
    run()

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

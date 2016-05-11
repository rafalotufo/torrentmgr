import requests


class TorrentInfo(object):
    def __init__(self, name, progress):
        self.data = {
            'name': name,
            'progress': progress
        }

    def __repr__(self):
        return json.dumps(self.data)


def to_torrent_info(info):
    return TorrentInfo(
        name=info['name'],
        progress=info['progress'])


class QbittorrentClient(object):
    def __init__(self, host):
        self.host = host
        self.s = requests.Session()

    def mkurl(self, service):
        return '%s%s' % (self.host, service)

    def login(self, username, password):
        url = self.mkurl('/login')
        r = self.s.post(url, data={'username': username, 'password': password})
        r.raise_for_status()

    def list(self):
        r = self.s.get(self.mkurl('/query/torrents'))
        if r.status_code == requests.codes.ok:
            return map(to_torrent_info, r.json())
        else:
            r.raise_for_status()

    def add_torrent(self, urls):
        return self.s.post(self.mkurl('/command/download'), {'urls': urls})

if __name__ == '__main__':
    import json
    c = QbittorrentClient('http://192.168.1.199:8085')
    c.login('rlotufo', 'baleieza')
    items = c.list()
    print items

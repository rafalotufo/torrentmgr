import requests


class QbittorrentClient(object):
    def __init__(self, host):
        self.host = host
        self.s = requests.Session()

    def mkurl(self, service):
        return '%s%s' % (self.host, service)

    def login(self, username, password):
        url = self.mkurl('/login')
        self.s.post(url, data={'username': username, 'password': password})

    def list(self):        
        return self.s.get(self.mkurl('/query/torrents'))

    def add_torrent(self, urls):
        return self.s.post(self.mkurl('/command/download'), {'urls': urls})

if __name__ == '__main__':
    c = QbittorrentClient('http://192.168.1.199:8085')
    c.login('rlotufo', 'baleieza')
    items = c.list()
    print items.json()

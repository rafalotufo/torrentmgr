import unittest
import torrentmgr.rssmsg


class RssMsgTest(unittest.TestCase):

    def test_fetch_latest(self):
        def list_shows():
            return [foo, bar]

        def save_file():
            pass

        def read_file():
            return {}

        foo = {'guid': 'foo', 'url': 'foourl', 'title': 'footitle'}
        bar = {'guid': 'bar', 'url': 'barurl', 'title': 'bartitle'}
        rss_mgr = torrentmgr.rssmsg.RssMgr(list_shows, save_file, read_file, None)

        self.assertEqual(rss_mgr.fetch_latest(), {'foo': foo, 'bar': bar})

    def test_fetch_latest_with_regex(self):
        def list_shows():
            return [foo, bar, barx]

        def save_file():
            pass

        def read_file():
            return {}

        foo = {'guid': 'foo', 'url': 'foourl', 'title': 'footitle'}
        bar = {'guid': 'bar', 'url': 'barurl', 'title': 'bartitle'}
        barx = {'guid': 'bar', 'url': 'barurl', 'title': 'barxxx'}
        rss_mgr = torrentmgr.rssmsg.RssMgr(list_shows, save_file, read_file, 'title')

        self.assertEqual(rss_mgr.fetch_latest(), {'foo': foo, 'bar': bar})

    def test_find_new(self):
        def list_shows():
            pass

        def save_file():
            pass

        def read_file():
            return {'foo': foo}

        foo = {'guid': 'foo', 'url': 'foourl', 'title': 'footitle'}
        bar = {'guid': 'bar', 'url': 'barurl', 'title': 'bartitle'}
        rss_mgr = torrentmgr.rssmsg.RssMgr(list_shows, save_file, read_file, None)

        self.assertEqual(rss_mgr.find_new({'foo': foo, 'bar': bar}), {'bar': bar})

    def test_update(self):
        def list_shows():
            return [foo, bar]

        def save_file(items):
            self.assertEqual(items, {'foo': foo, 'bar': bar})

        def read_file():
            return {'foo': foo}

        foo = {'guid': 'foo', 'url': 'foourl', 'title': 'footitle'}
        bar = {'guid': 'bar', 'url': 'barurl', 'title': 'bartitle'}
        rss_mgr = torrentmgr.rssmsg.RssMgr(list_shows, save_file, read_file, None)

        self.assertEqual(rss_mgr.update(), {'bar': bar})
        self.assertEqual(rss_mgr.items, {'foo': foo, 'bar': bar})

import api
import os
from cachelib import SimpleCache
from tornado.ioloop import IOLoop
import tornado.web
import logging
from tornado.log import enable_pretty_logging


enable_pretty_logging()
cache = SimpleCache()


class Base(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')


class AtTheMoment(Base):
    def get(self):
        res = cache.get('at_the_moment')
        if res is None:
            res = {
                'current': {
                    'sun': api.get_current_position('sun'),
                    'mercury': api.get_current_position('mercury'),
                    'venus': api.get_current_position('venus'),
                    'earth': api.get_current_position('earth'),
                    'moon': api.get_current_position('moon'),
                    'mars': api.get_current_position('mars'),
                    'jupiter': api.get_current_position('jupiter barycenter'),
                    'psp': api.get_psp_current_position()
                },
                'positions': {
                    'mercury': api.get_positions('mercury', -44, 44),
                    'venus': api.get_positions('venus', -112, 112),
                    'earth': api.get_positions('earth', -182, 183),
                    'moon': api.get_positions('moon', -15, 16),
                    'mars': api.get_positions('mars', -343, 344),
                    'psp': api.get_psp_positions(-60, 61, 24)
                }
            }
            cache.set('at_the_moment', res, timeout=60*60)
        self.write(res)


class LastDays(Base):
    def get(self):
        days = int(self.get_argument('days', 1)) - 1
        res = cache.get('last_days_%d' % days)
        if res is None:
            res = {
                'sun': api.get_positions('sun', -days, 1, 4),
                'mercury': api.get_positions('mercury', -days, 1, 4),
                'venus': api.get_positions('venus', -days, 1, 4),
                'earth': api.get_positions('earth', -days, 1, 4),
                'moon': api.get_positions('moon', -days, 1, 4),
                'mars': api.get_positions('mars', -days, 1, 4),
                'psp': api.get_psp_positions(-days, 1, 4),
            }
            cache.set('last_days_%d' % days, res, timeout=60*60)
        self.write(res)


def make_app():
    return tornado.web.Application([
        (r"/at_the_moment", AtTheMoment),
        (r"/last_days", LastDays)
    ])


def main():
    app = make_app()
    app.listen(int(os.environ.get('PORT', 8080)))
    IOLoop.current().start()


if __name__ == '__main__':
    main()

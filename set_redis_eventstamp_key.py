#!/usr/bin/env python
"""
Set eventstamp every second

Usage:
    set_redis_eventstamp_key.py --path=<redis_database_path>
"""
import os
import traceback
import credis
import time
from threading import Thread
from docopt import docopt
options = docopt(__doc__)

JOBS = [
    ('127.0.0.1', 6379),
]
recentInputEventHandled = 0

def worker():
    root = options['--path']
    for host, port in JOBS:
        try:
            conn = credis.Connection(host=host, port=port)
            global recentInputEventHandled
            lastInputEventHandled = int(conn.execute('get', 'app::lastInputEventHandled'))
            if lastInputEventHandled - recentInputEventHandled > 4000:
                recentInputEventHandled = lastInputEventHandled
                print 'found recent input event handled', recentInputEventHandled
                os.link(os.path.join(root, 'dump.rdb'), os.path.join(root, 'dump.rdb.%s' % recentInputEventHandled))
        except:
            traceback.print_exc()


def main():
    while True:
        Thread(target=worker).run()
        time.sleep(1)

if __name__ == '__main__':
    main()

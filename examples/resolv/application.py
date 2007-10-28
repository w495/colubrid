import sys, os
sys.path.insert(0, os.path.realpath('..'))
from colubrid import ResolveRegexApplication, execute


class Webpage(ResolveRegexApplication):
    urls = [
        (r'^(.*?)/?$', 'resolv.apps.app_$1.execute')
    ]

app = Webpage


if __name__ == '__main__':
    execute()

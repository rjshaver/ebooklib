import six
import subprocess

from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

# Recommend usage of
# - https://github.com/w3c/tidy-html5

def tidy_cleanup(content, **extra):
    cmd = []

    for k, v in six.iteritems(extra):
    	cmd.append('--%s' % k)

    	if v:
    		cmd.append(v)

    # must parse all other extra arguments
    try:
        p = subprocess.Popen(['tidy']+cmd, shell=False, 
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, close_fds=True)
    except OSError:
        return (3, None)

    p.stdin.write(content)
    p.stdin.close()

    # 0 - all ok
    # 1 - there were warnings
    # 2 - there were errors
    # 3 - exception

    ret_code = p.wait()

    cont = ''
    while True:
        s = p.stdout.read(1024)
        if s == '':
            break
        cont += s

    return (ret_code, cont)



class TidyPlugin(BasePlugin):
    NAME = 'Tidy HTML'
    OPTIONS = {'utf8': None,
               'tidy-mark': 'no'
              }

    def __init__(self, extra = {}):
        self.options = dict(self.OPTIONS)
        self.options.update(extra)

    def html_before_write(self, book, chapter):
        if not chapter.content:
            return None

        (_, chapter.content) = tidy_cleanup(chapter.content, **self.options)

        return chapter.content

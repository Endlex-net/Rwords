"""
Rwords:
    A command line tool to help you remember words faster.

Usage:
    rw (a | add) (<Word>... | -r <WordsPath>...)
    rw (l | learn)
    rw (r | review) [--p=<ReviewPage>] [--o=<ReviewOffset>]
    rw (d | dashboard)
    rw (-h | --help)
    rw --version

Arguments:
    Word            A word you want to learn.
    WordsPath       A file with words you want to learn.
    ReviewPage      A count of review page.
    ReviewOffset    A count of item on a page.

Command:
    a add           Add words(from files) in your memory store.
    l learn         Learn a word form memory store.
    r review        Review all words in memory store.
    d dashboard     Check out your study analysis results.

Options:
    -r              Select a file(or files) with words.
    -p              Set the current page count.
    -o              Set the items count in a page.

    -h --help       Show help.
    -v --version    Show version.
"""

from docopt import docopt
from .commands import Commands
from . import __version__


def main():
    kw = docopt(__doc__, version=__version__)
    command_route(kw)


def command_route(kw):
    """command route"""
    commands = Commands()

    if kw.get("a") or kw.get('add'):
        return commands.add(kw['<Word>'], kw['<WordsPath>'])
    elif kw.get('l') or kw.get('learn'):
        return commands.learn()
    elif kw.get('r') or kw.get('review'):
        return commands.review(kw['--p'], kw['--o'])
    elif kw.get('d') or kw.get('dashboard'):
        return commands.dashboard()


if __name__ == '__main__':
    main()

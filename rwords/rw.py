"""
Rwords:
    A command line tool to help you remember words faster.

Usage:
    rw (a | add) (<Word>... | -r <WordsPath>...)
    rw (l | learn)
    rw (r | review) [-p <ReviewPage>] [-o <ReviewOffset>]
    rw (d | dashboard)
    rw (-h | --help)
    rw --version

Arguments:
    Word            A word you want to learn.
    WordsPath       A file with words you want to learn.
    ReviewPage      A count of review page.

Command:
    a add           Add words(from files) in your memory store.
    l learn         Learn a word form memory store.
    r review        Review the words in memory store.
    d dashboard     Check out your study analysis results.

Options:
    -r              Select a file(or files) with words.
    -p              Set the current page count.
    -o              Set the items count in a page.

    -h --help       Show help.
    -v --version    Show version.
"""

from docopt import docopt
from .commands import command_route
from . import __version__


def main():
    kw = docopt(__doc__, version=__version__)
    command_route(kw)


if __name__ == '__main__':
    main()

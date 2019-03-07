# -*- coding: utf-8 -*-
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
__version__ = '0.0.0.rc.106'

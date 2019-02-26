## Rwords
	Rwords is a command line tool that helps you remember words quickly.

## quick start
It is recommended to create a virtual environment before use.
#### How to install
```
    $ mkvirtualenv Rword -p python3
    $ pip install rwords
```
#### Let's start
Let's add the ‘word’ to the rwords's memory store.

```
	$ rw a word
```
If you see ```$ 0 words have been added to memory store.```

Then, learn words

```
	$ rw l
```
You can see the word and hear it's sound.
```
    [' line ']
    Q: Q: [j] 完全不会;  [k] 有印象; [l] 认识; [e] 熟悉 (j/k/l/e)
```

input k

```
    [' line ']
    [n.] 线条; 排; 行列; 界线
    [vt.] 排队; 用线标出; 沿…排列成行; 给…安衬里
    [vi.] 形成一层; 排队; 击出平直球
    Q: [t] 答对了; [f] 答错了 (t/f)
```
Input t

You have successfully completed a review, Rwords has put the word on the review list for the day you you will forget it.

## Usage
```
Rwords:
    A command line tool to help you remember words more quickly.

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
```

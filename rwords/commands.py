from rwords.core.db import init_db
from rwords.words import word_hander


class Commands:
    """Rword Commands"""
    def __init__(self):
        init_db()
        word_hander.init_review_list()

    def add(self, words=[], file_paths=[]):
        """add words to memory store"""
        if file_paths:
            words = []
            for file_path in file_paths:
                words += self._get_words_by_file_name(file_path)

        word_hander.add_words(words)

    def _get_words_by_file_name(self, file_path):
        """Return words by file_name"""
        with open(file_path, 'r') as f:
            return [word.lstrip().replace('\n', '') for word in f.readlines()]

    def learn(self):
        """Learn(Review) a word from review list"""
        errno, errmsg, _ = word_hander.learn_word()
        if errno:
            print(errmsg)


def command_route(kw):
    commands = Commands()

    if kw.get("a") or kw.get('add'):
        return commands.add(kw['<Word>'], kw['<WordsPath>'])
    elif kw.get('l') or kw.get('learn'):
        return commands.learn()
    elif kw.get('r') or kw.get('review'):
        print("开发中")
        pass
    elif kw.get('d') or kw.get('dashboard'):
        print("开发中")
        pass


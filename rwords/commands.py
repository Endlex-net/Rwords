# -*-coding:utf8-*-
import traceback

from rwords.core.db import init_db
from rwords.words import word_hander, review_hander
from rwords.console import console_hander
from rwords.core import settings
from rwords.core.exception import *


class Commands:
    """Rword Commands"""

    def __init__(self):
        init_db()
        word_hander.init_review_list()

    def add(self, words=None, file_paths=None):
        """add words to memory store"""
        try:
            word_names = words if words else []
            if file_paths:
                word_names = self._get_words_by_file_paths(file_paths)

            errno, errmsg, data = word_hander.add_words(word_names)
            if errno:
                console_hander.warning(errmsg)
                return None

            for warrning in data['warning_list']:
                console_hander.warning(warrning)

            if data['fail_list']:
                console_hander.warning("Failed to add {}".format(data['fail_list']))

            success_count = len(word_names) - len(data['fail_list'])
            console_hander.msg("{} words have been added to memory store.".format(success_count))

        except Exception as exc:
            console_hander.error(str(exc))
            if settings.DEBUG:
                traceback.print_exc()
            # TODO write log
        return None

    def _get_words_by_file_paths(self, file_paths):
        """Return word_names by file_paths"""
        word_names = []
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                lines = f.readlines()

                def format_word(word): return word.strip().replace('\n', '')
                word_names_of_lines = [format_word(word) for word in lines]
                word_names.extend(word_names_of_lines)

        return word_names

    def learn(self):
        """Learn(Review) a word from review list"""
        try:
            word_info = word_hander.get_today_word_info()
            score = console_hander.learn_word(word_info)
            review_hander.review_a_word(word_info['id'], score)

        except LearnListEmptyException:
            console_hander.msg("Today's learn list is empty.")

        except Exception as exc:
            console_hander.error(str(exc))
            if settings.DEBUG:
                traceback.print_exc()
            # TODO write log
        return None

    def review(self, page=None, offset=None):
        """Review all words in memory store."""
        page = int(page) if page else 1
        offset = int(offset) if offset else 10
        while True:
            errno, errmsg, data = word_hander.review(page, offset)
            page = data['page']
            offset = data['offset']
            chr = console_hander.review_words_page(data['word_infos'], data['page'], data['offset'], data['word_count'])
            if chr == 'q':
                break
            elif chr == 'n':
                page += 1
            elif chr == 'p':
                page -= 1
            elif chr == 'v':
                word_id = int(console_hander.input('Please enter the word id'))
                word_info = word_hander.get_word(word_id)
                console_hander.view_word_info(word_info)

    def dashboard(self):
        print("under construction")
        # 记忆库容量，今日单词数量， 完成数量
        # 单词熟练度比例
        # 总的复习趋势
        pass

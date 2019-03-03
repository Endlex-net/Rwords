# -*-coding:utf8-*-
import datetime
import json

from rwords.store import word_store, review_list_store, sys_info_store, word_factor_store
from rwords.core.iciba_word_api import get_word_info
from rwords.core import utills
from rwords.core import settings
from rwords.core.db import session_scope
from rwords.core.exception import *
from rwords.console import console_hander
from rwords.review_arithmetic import learn_arithmetic
from rwords.models import ReviewList


class WordHander():
    """Word Hander"""

    def init_review_list(self):
        """put today' words need review in review list"""
        # TODO unit test
        if sys_info_store.get_review_list_time() != datetime.datetime.now().strftime("%Y-%m-%d"):
            with session_scope() as session:
                word_ids = word_factor_store.get_today_word_ids(session=session)
                for word_id in word_ids:
                    review_list_store.add_word_in_list(word_id, session=session)
                sys_info_store.set_review_list_time(session=session)
            console_hander.msg("已添加{}个单词到今日学习计划".format(len(word_ids)))

    def add_word(self, word_name):
        """add a word"""
        try:
            word_info = get_word_info(word_name)
            mp3_path = utills.download_mp3(word_info['mp3_url'], word_name)

            word_store.create(
                word_info['word_name'],
                word_info['ph'],
                word_info['tran_means'],
                word_info['mp3_url'],
                mp3_path,
            )
            errno = 0
            errmsg = 'success'
            data = {}
        except IcibaInvalidWordException:
            errno = 1
            errmsg = "The '{}' cannot found in Iciba.".format(word_name)
            data = {}

        except WordRepeatAddException:
            errno = 1
            errmsg = "The '{}' is already in memory store!".format(word_name)
            data = {}

        return errno, errmsg, data

    def add_words(self, word_names):
        """Add words"""
        fail_list = []
        warnings = []
        for word_name in word_names:
            errno, errmsg, data = self.add_word(word_name)
            if errno:
                fail_list.append(word_name)
                warnings.append(errmsg)

        data = {'fail_list': fail_list, 'warning_list': warnings}
        return 0, "success", data

    def get_today_word_info(self):
        """Return a word_info from review list"""
        # TODO unit test
        word_id = review_list_store.get_a_word_id()
        word_info = word_store.get_word(id=word_id)
        self._check_music_by_word_info(word_info)
        return word_info

    def get_word(self, word_id):
        word_info = word_store.get_word(id=word_id)
        self._check_music_by_word_info(word_info)
        return word_info


    def _check_music_by_word_info(self, word_info):
        """check(or try download if no file) music"""
        # TODO unit test
        import os
        mp3_info = word_info['mp3']
        mp3_path = '{}{}'.format(settings.BASE_DIR, mp3_info['path'])
        if os.path.exists(mp3_path):
            return None

        if mp3_info['url']:
            path = utills.download_mp3(mp3_info['url'], word_info['word_name'])
        else:
            _word_info = get_word_info(word_info['word_name'])
            path = utills.download_mp3(_word_info['mp3_url'], _word_info['word_name'])

        word_store.update_mp3(id=word_info['id'], path=path)
        return None

    def review(self, page, offset):
        # TODO unit test
        """Review all words in memory store."""
        page = max(page, 1)
        offset = max(offset, 1)
        word_count = word_store.get_words_count()

        max_page = word_count // offset
        if word_count % float(offset) > 0.0001:
            max_page += 1
        page = min(page, max_page)

        start = (page - 1) * offset
        end = start + offset
        word_infos = word_store.get_words(start=start, end=end)
        return 0, 'success', {'word_infos': word_infos, 'word_count': word_count, 'page': page, 'offset': offset}


class ReviewHander:
    """Review Hander"""
    def review_a_word(self, word_id, score):
        """Review a word; Change Word Factors"""
        w_type = review_list_store.get_word_type(word_id)
        repeat_count = 5 - score if score < 3 else 0
        if w_type is ReviewList.WordType.repeat:
            if not repeat_count:
                review_list_store.reduce_repeat_count(word_id)
        else:
            IF, EF, OF_matrix = self.get_factors(word_id, score)
            review_list_store.del_word_in_list(word_id)
            if repeat_count:
                # score < 3, need repeat some time to remember the word.
                review_list_store.add_word_in_list(word_id, repeat=True, repeat_count=repeat_count)
            # change EF, change OF_matrix, change next_review_day

            next_review_day = datetime.datetime.now() + datetime.timedelta(days=IF)
            word_factor_store.set_EF(word_id, EF)
            word_factor_store.set_OF_matrix(word_id, OF_matrix)
            word_factor_store.set_next_review_time(word_id, next_review_day)
        return 0, "success", {}

    def get_factors(self, word_id, score):
        w_type = review_list_store.get_word_type(word_id)
        if w_type is ReviewList.WordType.new:
            IF = 1
            EF = learn_arithmetic.get_EF_by_first_score(score)
            OF_matrix = [(0, learn_arithmetic.MIN_EF)]
        else:
            _EF = word_factor_store.get_EF(word_id)
            _OF_matrix = word_factor_store.get_OF_matrix(word_id)
            IF, EF, OF_matrix = learn_arithmetic.get_new_fraction(score, _EF, _OF_matrix)
        return IF, EF, OF_matrix


word_hander = WordHander()
review_hander = ReviewHander()

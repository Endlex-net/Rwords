# -*-coding:utf8-*-
import datetime
import json

from rwords.store import word_store, review_list_store, sys_info_store, word_factor_store
from rwords.core.iciba_word_api import get_word_info
from rwords.core.utills import download_mp3
from rwords.console import return_hander
from rwords.core.exception import *
from rwords.review_arithmetic import review_hander
from rwords.core.db import session_scope


class WordHander():
    """Word Hander"""

    def init_review_list(self):
        """put today' words need review in review list"""
        if sys_info_store.get_review_list_time() != datetime.datetime.now().strftime("%Y-%m-%d"):
            with session_scope() as session:
                word_ids = word_factor_store.get_today_word_ids(session=session)
                for word_id in word_ids:
                    review_list_store.add_word_in_list(word_id, session=session)
                sys_info_store.set_review_list_time(session=session)
            return_hander.msg("已添加{}个单词到今日学习计划")

    def add_word(self, word):
        """add a word"""
        try:
            word_info = get_word_info(word)
            mp3_path = download_mp3(word_info['mp3_url'], word)

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
            errmsg = "The '{}' cannot found in Iciba.".fromat(word)
            data = {}
            return_hander.error(errmsg)

        except WordRepeatAddException:
            errno = 1
            errmsg = "The '{}' is already in memory store!".format(word)
            data = {}
            return_hander.warning(errmsg)

        return errno, errmsg, data

    def add_words(self, word_names):
        """添加单词s"""
        fail_list = []
        for word_name in word_names:
            errno, errmsg, _ = self.add_word(word_name)
            if errno:
                fail_list.append(word_name)
        success_count = len(word_names) - len(fail_list)
        if fail_list:
            errmsg = ("Failed to add {}".format(fail_list))
            return_hander.warning(errmsg)
        return_hander.msg("{} words have been added to memory store.".format(success_count))
        return 0, "success", {}

    def learn_word(self):
        """Learn(Review) a word from review list"""
        try:
            word_id = review_list_store.get_a_word_id()
            word_info = word_store.get_word(id=word_id)

            return_hander.msg(u"[' {} ']".format(word_info['word_name']))
            self._play_music_by_word_info(word_info)
            chr = return_hander.question(u"Q: [j] 完全不会;  [k] 有印象; [l] 认识; [e] 熟悉", chars=u'jkle')
            return_hander.msg(u"[' {} ']".format(word_info['word_name']))
            for tran_mean in word_info['tran_means']:
                return_hander.msg(u'[{}] {}'.format(tran_mean['part'], '; '.join(json.loads(tran_mean['means']))))
            ret = return_hander.question(u"[t] 答对了; [f] 答错了", chars=u'tf') if chr != 'j' else ''

            key = chr + ret
            key2score = {
                'j': 0, 'kf': 0, 'lf': 1, 'ef': 2, 'kt': 3, 'lt': 4, 'et': 5,
            }
            score = key2score[key]
            review_hander.review_a_word(word_id, score)
            errno = 0
            errmsg = "success"
            data = {}

        except LearnListEmptyException:
            errno = 1
            errmsg = "Today's learn list is empty."
            data = {}

        return errno, errmsg, data

    def _play_music_by_word_info(self, word_info):
        """play(or try download if no path) music if mp3_obj have path or url"""
        mp3_info = word_info['mp3']
        if not return_hander.music(mp3_info['path']) and mp3_info['url']:
            path = download_mp3(word_info['mp3_url'], word_info['word_name'])
            word_store.update_mp3(id=word_info['id'], path=path)
            return_hander.music(path)


word_hander = WordHander()

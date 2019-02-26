import json
import datetime
import random

from rwords.core.exception import *
from rwords.core.db import Session, session_scope
from rwords.core.utills import dumps_alchemy
from rwords.models import Word, TranMean, Mp3, WordFactor, ReviewList, OptimumFactorMatrix, SysInfo


class WordStore:
    """WordStore"""
    def create(self, word_name, ph, tran_means, mp3_url, mp3_path, session=None):
        """create word in memory store"""
        with session_scope(session=session) as session:
            if session.query(Word).filter_by(word_name=word_name).first():
                raise WordRepeatAddException

            # create word_obj
            tran_mean_objs = []
            for tran_mean in tran_means:
                mean_obj = TranMean(
                    part=tran_mean['part'],
                    means=json.dumps(tran_mean['means']),
                )
                tran_mean_objs.append(mean_obj)

            mp3_obj = Mp3(
                url=mp3_url,
                path=mp3_path,
            )

            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            word_factor = WordFactor(
                EF=1.3,
                number=0,
                next_review_time=tomorrow,
            )

            word_obj = Word(
                word_name=word_name,
                ph=ph,
                tran_means=tran_mean_objs,
                mp3=mp3_obj,
                word_factor=word_factor,
            )
            session.add(word_obj)
            session.flush()
            review_list_store.add_word_in_list(word_obj.id, new=True, session=session)

            word_obj_id = word_obj.id
        return word_obj_id

    def get_word(self, id=None, word=None, session=None):
        """Return a Word obj """
        with session_scope(session=session) as session:
            kwargs = {}
            if id:
                kwargs['id'] = id
            elif word:
                kwargs['word_name'] = word
            else:
                return None

            word_obj = session.query(Word).filter_by(**kwargs).first()
            word_info = dumps_alchemy(word_obj, ['mp3', 'tran_means'])
        return word_info



    def update_mp3(self, id=None, word=None, path=None, url=None, session=None):
        """Update mp3 Info"""
        kwargs = {}
        if id:
            kwargs['id'] = id
        elif word:
            kwargs['word'] = word
        with session_scope(session=session) as session:
            word_obj = session.query(Word).filter_by(id=id).first()
            mp3_obj = word_obj.mp3
            if path:
                mp3_obj.path = path
            if url:
                mp3_obj.url = url
        return True


class ReviewListStore:
    """ReviewList store"""

    def add_word_in_list(self, word_id, new=False, repeat=False, repeat_count=1,  session=None):
        """Add new word to review list."""
        with session_scope(session=session) as session:
            if new:
                w_type = ReviewList.WordType.new
            elif repeat:
                w_type = ReviewList.WordType.repeat
            else:
                w_type = ReviewList.WordType.review
            review_list_obj = ReviewList(
                word_id=word_id,
                w_type=w_type,
                repeat_count=repeat_count,
            )
            session.add(review_list_obj)
        return True

    def reduce_repeat_count(self, word_id, session=None):
        """reduce repeat_count for word"""
        with session_scope(session=session) as session:
            item = session.query(ReviewList).filter_by(word_id=word_id).first()
            if item.repeat_count > 1:
                item.repeat_count -= 1
            else:
                session.delete(item)
        return True

    def del_word_in_list(self, word_id, session=None):
        """Remove the word from review list."""
        with session_scope(session=session) as session:
            session.query(ReviewList).filter_by(word_id=word_id).delete()

    def get_a_word_id(self):
        """Return a word_id in review list."""
        with session_scope() as session:
            learn_list = session.query(ReviewList).all()

            if not learn_list:
                raise LearnListEmptyException

            item = random.choice(learn_list)
            word_id = item.word_id
        return word_id

    def get_word_type(self, word_id):
        """Return word type by word_id"""
        with session_scope() as session:
            item = session.query(ReviewList).filter_by(word_id=word_id).first()
            return item.w_type


class WordFactorStore:
    """WordFactor Store"""

    def get_OF_matrix(self, word_id):
        """Return historical optimum factor matrix of the word"""
        with session_scope() as session:
            word_factor = session.query(WordFactor).filter_by(word_id=word_id).first()
            OF_objs = word_factor.OF_matrix
            OF_matrix = [(OF_i.number, OF_i.OF) for OF_i in OF_objs]
        return OF_matrix

    def get_EF(self, word_id):
        """Return word's EF"""
        with session_scope() as session:
            word_factor = session.query(WordFactor).filter_by(word_id=word_id).first()
            EF = word_factor.EF
        return EF

    def set_EF(self, word_id, EF, session=None):
        """Set EF for word"""
        with session_scope(session=session) as session:
            word_factor = session.query(WordFactor).filter_by(word_id=word_id).first()
            word_factor.EF = EF
        return EF

    def set_OF_matrix(self, word_id, OF_matrix, session=None):
        """set OF matrix for word"""
        with session_scope(session=session) as session:
            word_factor = session.query(WordFactor).filter_by(word_id=word_id).first()
            session.query(OptimumFactorMatrix).filter_by(word_factor_id=word_factor.id).delete()
            OF_objs = [OptimumFactorMatrix(word_factor_id=word_factor.id, number=item[0], OF=item[1]) for item in OF_matrix]
            session.add_all(OF_objs)
        return OF_matrix

    def set_next_review_time(self, word_id, next_review_time, session=None):
        """set next review time for word"""
        with session_scope(session=session) as session:
            word_factor = session.query(WordFactor).filter_by(word_id=word_id).first()
            word_factor.next_review_time = next_review_time
        return next_review_time

    def get_today_word_ids(self, session=None):
        """get the words next_review_time in today"""
        now = datetime.datetime.now()
        end = now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
        with session_scope(session=session) as session:
            word_Factor_objs = session.query(WordFactor).filter(
                WordFactor.next_review_time < end
            ).all()
            word_ids = [word_factor.word_id for word_factor in word_Factor_objs]
        return word_ids


class SysInfoStore:

    def get_review_list_time(self, session=None):
        with session_scope(session=session) as session:
            return session.query(SysInfo).filter_by(key="review_list_time").first().value

    def set_review_list_time(self, session=None):
        with session_scope(session=session) as session:
            value = datetime.datetime.now().strftime("%Y-%m-%d")
            session.query(SysInfo).filter_by(key="review_list_time").first().value = value
        return value


word_store = WordStore()
review_list_store = ReviewListStore()
word_factor_store = WordFactorStore()
sys_info_store = SysInfoStore()
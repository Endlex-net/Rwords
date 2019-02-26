# -*- coding: utf-8 -*-
from rwords.core.db import session_scope
from rwords.models import *
from rwords.store import word_store, review_list_store
from rwords.review_arithmetic import learn_arithmetic, review_hander, MIN_EF, MAX_EF
from tests import mock_info


class TestLearnArithmetic():

    def test_get_new_fraction(self):
        q = 1
        EF = 1.3
        OF_matrix = [(0, 1.3)]
        for i in range(5):
            q = q + 1 if q <=5 else 5
            IF, EF, OF_matrix = learn_arithmetic.get_new_fraction(q, EF, OF_matrix)
        assert isinstance(IF, float)
        assert isinstance(EF, float)
        assert len(OF_matrix) == 6


class TestReviewHander():

    def test_get_EF_by_first_score(self):
        assert review_hander.get_EF_by_first_score(5) == MIN_EF
        assert review_hander.get_EF_by_first_score(0) == MAX_EF

    def test_get_factors(self):
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_info.word_info['word_name']).delete()
        word_id = word_store.create(
            mock_info.word_info['word_name'],
            mock_info.word_info['ph'],
            mock_info.word_info['tran_means'],
            mock_info.word_info['mp3_url'],
            '',
        )
        IF, EF, OF_matrix = review_hander.get_factors(word_id, 0)
        assert IF == 1
        assert EF == MAX_EF
        assert OF_matrix == [(0, MIN_EF)]
        # TODO Here need 'else' test

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_review_a_word(self):
        # TODO I don't know how to test it.
        # SO, smoke testing.
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_info.word_info['word_name']).delete()
        word_id = word_store.create(
            mock_info.word_info['word_name'],
            mock_info.word_info['ph'],
            mock_info.word_info['tran_means'],
            mock_info.word_info['mp3_url'],
            '',
        )

        review_hander.review_a_word(word_id, 2)
        for i in range(3):
            review_hander.review_a_word(word_id, 5)
        with session_scope() as session:
            assert session.query(ReviewList).filter_by(word_id=word_id).first() is None
        review_list_store.add_word_in_list(word_id)
        review_hander.review_a_word(word_id, 5)

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

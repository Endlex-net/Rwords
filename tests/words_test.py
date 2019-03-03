# -*- coding: utf-8 -*-
from rwords.words import word_hander, review_hander
from rwords.core.db import session_scope
from rwords import models
from rwords.store import word_store, review_list_store
from rwords.review_arithmetic import  LearnArithmetic

from tests import mock_info


class TestWordHander:
    def test_init_review_list(self):
        pass

    def test_add_word(self):
        mock_word = mock_info.word_info['word_name']
        with session_scope() as session:
            session.query(models.Word).filter_by(word_name=mock_word).delete()

        assert word_hander.add_word(mock_word)[0] == 0

        with session_scope() as session:
            word = session.query(models.Word).filter_by(word_name=mock_word).first()
            assert word.word_name == mock_info.word_info['word_name']
            word_id = word.id

            session.query(models.Mp3).filter_by(word_id=word_id).delete()
            session.query(models.ReviewList).filter_by(word_id=word_id).delete()
            session.query(models.Word).filter_by(id=word_id).delete()

    def test_add_words(self):
        mock_words = [mock_info.word_info['word_name'], ]
        with session_scope() as session:
            session.query(models.Word).filter_by(word_name=mock_words[0]).delete()

        assert word_hander.add_words(mock_words)[0] == 0

        with session_scope() as session:
            word = session.query(models.Word).filter_by(word_name=mock_words[0]).first()
            assert word.word_name == mock_info.word_info['word_name']
            word_id = word.id

            session.query(models.Mp3).filter_by(word_id=word_id).delete()
            session.query(models.ReviewList).filter_by(word_id=word_id).delete()
            session.query(models.Word).filter_by(id=word_id).delete()

    class TestReviewHander():

        def test_review_a_word(self):
            # TODO I don't know how to test it.
            # SO, smoke testing.
            with session_scope() as session:
                session.query(models.Word).filter_by(word_name=mock_info.word_info['word_name']).delete()
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
                assert session.query(models.ReviewList).filter_by(word_id=word_id).first() is None
            review_list_store.add_word_in_list(word_id)
            review_hander.review_a_word(word_id, 5)

            with session_scope() as session:
                session.query(models.Mp3).filter_by(word_id=word_id).delete()
                session.query(models.ReviewList).filter_by(word_id=word_id).delete()
                session.query(models.Word).filter_by(id=word_id).delete()


        def test_get_factors(self):
            with session_scope() as session:
                session.query(models.Word).filter_by(word_name=mock_info.word_info['word_name']).delete()
            word_id = word_store.create(
                mock_info.word_info['word_name'],
                mock_info.word_info['ph'],
                mock_info.word_info['tran_means'],
                mock_info.word_info['mp3_url'],
                '',
            )
            IF, EF, OF_matrix = review_hander.get_factors(word_id, 0)
            assert IF == 1
            assert EF == LearnArithmetic.MIN_EF
            assert OF_matrix == [(0, LearnArithmetic.MIN_EF)]
            # TODO Here need 'else' test

            with session_scope() as session:
                session.query(models.Mp3).filter_by(word_id=word_id).delete()
                session.query(models.ReviewList).filter_by(word_id=word_id).delete()
                session.query(models.Word).filter_by(id=word_id).delete()
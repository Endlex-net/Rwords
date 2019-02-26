from rwords.words import word_hander
from rwords.core.db import session_scope
from rwords import models

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


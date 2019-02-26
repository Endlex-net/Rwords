import json
import datetime

from rwords.store import word_store, review_list_store, word_factor_store
from rwords.models import Word, Mp3, WordFactor, ReviewList, OptimumFactorMatrix
from rwords.core.db import session_scope
from tests import mock_info


class TestWordStore:
    def test_create(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
            session.commit()
            word_id = word_store.create(
                mock_word_info['word_name'],
                mock_word_info['ph'],
                mock_word_info['tran_means'],
                mock_word_info['mp3_url'],
                '',
            )
            word_obj = session.query(Word).filter_by(id=word_id).first()
            assert word_obj.word_name == mock_word_info['word_name']
            assert word_obj.ph == mock_word_info['ph']
            tran_mean = word_obj.tran_means[0]
            assert {'part': tran_mean.part, 'means': json.loads(tran_mean.means)} == mock_word_info['tran_means'][0]
            assert word_obj.mp3.url == mock_word_info['mp3_url']
            assert isinstance(word_obj.word_factor, WordFactor)
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.delete(word_obj)

    def test_get_word(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()

        word_id = word_store.create(
            mock_word_info['word_name'],
            mock_word_info['ph'],
            mock_word_info['tran_means'],
            mock_word_info['mp3_url'],
            '',
        )
        word_info = word_store.get_word(id=word_id)
        assert word_info['word_name'] == mock_word_info['word_name']

        word_info = word_store.get_word(word=mock_word_info['word_name'])
        assert word_info['ph'] == mock_word_info['ph']

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()

    def test_update_mp3(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()

        word_id = word_store.create(
            mock_word_info['word_name'],
            mock_word_info['ph'],
            mock_word_info['tran_means'],
            mock_word_info['mp3_url'],
            '',
        )

        mock_path = '/data/mp3/mock.mp3'
        mock_url = mock_word_info['mp3_url'] + 'mock'
        word_store.update_mp3(id=word_id, path=mock_path, url=mock_url)
        assert word_store.get_word(id=word_id)['mp3']['path'] == mock_path
        assert word_store.get_word(id=word_id)['mp3']['url'] == mock_url

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()


class TestReviewListStore:

    def test_add_word_in_list(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
            word_obj = Word(
                word_name=mock_word_info['word_name'],
                ph=mock_word_info['ph'],
            )
            session.add(word_obj)
            session.flush()
            word_id = word_obj.id

        review_list_store.add_word_in_list(word_id, repeat_count=5)

        with session_scope() as session:
            assert session.query(ReviewList).filter_by(word_id=word_id).first().repeat_count == 5

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_del_word_in_list(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
            word_obj = Word(
                word_name=mock_word_info['word_name'],
                ph=mock_word_info['ph'],
            )
            session.add(word_obj)
            session.flush()
            word_id = word_obj.id

        review_list_store.del_word_in_list(word_id)

        with session_scope() as session:
            assert session.query(ReviewList).filter_by(word_id=word_id).first() is None

            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_reduce_repeat_count(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
            word_obj = Word(
                word_name=mock_word_info['word_name'],
                ph=mock_word_info['ph'],
            )
            session.add(word_obj)
            session.flush()
            word_id = word_obj.id

        review_list_store.del_word_in_list(word_id)
        review_list_store.add_word_in_list(word_id, new=False, repeat_count=2)
        review_list_store.reduce_repeat_count(word_id)

        with session_scope() as session:
            assert session.query(ReviewList).filter_by(word_id=word_id).first().repeat_count == 1

        review_list_store.reduce_repeat_count(word_id)

        with session_scope() as session:
            assert session.query(ReviewList).filter_by(word_id=word_id).first() is None

            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_get_word_type(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
            word_obj = Word(
                word_name=mock_word_info['word_name'],
                ph=mock_word_info['ph'],
            )
            session.add(word_obj)
            session.flush()
            word_id = word_obj.id

        review_list_store.add_word_in_list(word_id)
        assert review_list_store.get_word_type(word_id) is ReviewList.WordType.review

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()


class TestWordFactorStore:

    def test_get_OF_matrix(self):
        mock_word_info = mock_info.word_info
        mock_OF_matrix = mock_info.OF_matrix
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
        word_id = word_store.create(
            mock_word_info['word_name'],
            mock_word_info['ph'],
            mock_word_info['tran_means'],
            mock_word_info['mp3_url'],
            '',
        )

        with session_scope() as session:
            word_factor_id = session.query(WordFactor).filter_by(word_id=word_id).first().id
            OF_objs = [OptimumFactorMatrix(word_factor_id=word_factor_id, number=item[0], OF=item[1]) for item in
                       mock_OF_matrix]
            session.add_all(OF_objs)

        assert word_factor_store.get_OF_matrix(word_id) == mock_OF_matrix

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()
            session.query(OptimumFactorMatrix).filter_by(word_factor_id=word_factor_id).delete()

    def test_get_EF(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
        word_id = word_store.create(
            mock_word_info['word_name'],
            mock_word_info['ph'],
            mock_word_info['tran_means'],
            mock_word_info['mp3_url'],
            '',
        )

        assert word_factor_store.get_EF(word_id) == 1.3

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_set_EF(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
        word_id = word_store.create(
            mock_word_info['word_name'],
            mock_word_info['ph'],
            mock_word_info['tran_means'],
            mock_word_info['mp3_url'],
            '',
        )

        word_factor_store.set_EF(word_id, 1.4)
        assert word_factor_store.get_EF(word_id) == 1.4

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_set_OF_matrix(self):
        mock_word_info = mock_info.word_info
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_word_info['word_name']).delete()
        word_id = word_store.create(
            mock_word_info['word_name'],
            mock_word_info['ph'],
            mock_word_info['tran_means'],
            mock_word_info['mp3_url'],
            '',
        )

        word_factor_store.set_OF_matrix(word_id, mock_info.OF_matrix)
        assert word_factor_store.get_OF_matrix(word_id) == mock_info.OF_matrix

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_set_next_review_time(self):
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_info.word_info['word_name']).delete()
        word_id = word_store.create(
            mock_info.word_info['word_name'],
            mock_info.word_info['ph'],
            mock_info.word_info['tran_means'],
            mock_info.word_info['mp3_url'],
            '',
        )

        word_factor_store.set_next_review_time(word_id=word_id, next_review_time=mock_info.next_review_time)

        with session_scope() as session:
            assert session.query(WordFactor).filter_by(word_id=word_id).first().next_review_time == mock_info.next_review_time

            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()

    def test_get_today_word_ids(self):
        with session_scope() as session:
            session.query(Word).filter_by(word_name=mock_info.word_info['word_name']).delete()
            word_id = word_store.create(
                mock_info.word_info['word_name'],
                mock_info.word_info['ph'],
                mock_info.word_info['tran_means'],
                mock_info.word_info['mp3_url'],
                '',
                session=session,
            )
            word_factor = session.query(WordFactor).filter_by(word_id=word_id).first()
            word_factor.next_review_time = datetime.datetime.now()

        assert word_factor_store.get_today_word_ids() == [word_id]

        with session_scope() as session:
            session.query(Mp3).filter_by(word_id=word_id).delete()
            session.query(ReviewList).filter_by(word_id=word_id).delete()
            session.query(WordFactor).filter_by(word_id=word_id).delete()
            session.query(Word).filter_by(id=word_id).delete()


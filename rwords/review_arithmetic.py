import datetime

from rwords.models import ReviewList
from rwords.store import review_list_store, word_factor_store


MAX_EF = 2.5
MIN_EF = 1.3

class LearnArithmetic():
    """
    LearnArithmetic:
        SuperMemo 5
        https://www.supermemo.com/english/ol/sm5.html
    """
    def __init__(self):
        # self.min_review_interval = settings['min_review_interval']
        self.min_review_interval = 3
        self.min_EF = 1.3
        self.fraction = 0.8

    def get_new_fraction(self, q, EF, OF_matrix):
        """Return new fration(IF, EF, OF_matrix) when learn(review) a word"""
        IF = self._get_IF(len(OF_matrix), EF, OF_matrix)
        new_EF = self._get_new_EF(EF, q)
        new_OF_matrix = self._get_new_OF_matrix(q, OF_matrix)
        return IF, new_EF, new_OF_matrix

    def _get_IF(self, n, EF, OF_matrix):
        """Return inter-repetition interval"""
        if n < 1:
            return self._get_OF(n, EF)
        else:
            return self._get_OF(n, EF) * self._get_IF(*OF_matrix[n-1], OF_matrix)

    def _get_OF(self, n, EF):
        """Return optimum factor"""
        if n < 1:
            return self.min_review_interval
        return EF

    def _get_new_EF(self, EF, q):
        """Return new EF when learn(review) a word"""
        new_EF = EF + (0.1 - (5-q) * (0.08 + (5 - q) * 0.02))
        new_EF = self.min_EF if new_EF < self.min_EF else new_EF
        return new_EF

    def _get_new_OF_matrix(self, q, OF_matrix):
        """Return new OF_matrix when learn(review) a word"""
        n = len(OF_matrix)
        print(n)
        OF = OF_matrix[n-1][1]
        OF1 = OF * (0.72 + q * 0.07)
        OF2 = (1 - self.fraction) * OF + self.fraction * OF1
        OF_matrix.append((n, OF2))
        return OF_matrix


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
            EF = self.get_EF_by_first_score(score)
            OF_matrix = [(0, MIN_EF)]
        else:
            _EF = word_factor_store.get_EF(word_id)
            _OF_matrix = word_factor_store.get_OF_matrix(word_id)
            IF, EF, OF_matrix = learn_arithmetic.get_new_fraction(score, _EF, _OF_matrix)
        return IF, EF, OF_matrix

    def get_EF_by_first_score(self, score):
        """Return EF by first score"""
        return MAX_EF - (MAX_EF - MIN_EF) / 5 * score


learn_arithmetic = LearnArithmetic()
review_hander = ReviewHander()


# -*- coding: utf-8 -*-
from rwords.review_arithmetic import learn_arithmetic


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

    def test_get_EF_by_first_score(self):
        assert abs(learn_arithmetic.get_EF_by_first_score(3) - 2.02) <0.001
        assert learn_arithmetic.get_EF_by_first_score(5) == learn_arithmetic.MIN_EF
        assert learn_arithmetic.get_EF_by_first_score(0) == learn_arithmetic.MAX_EF

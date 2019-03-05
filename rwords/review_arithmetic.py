import datetime


class LearnArithmetic:
    """
    LearnArithmetic:
        SuperMemo 5
        https://shop.supermemo.com/english/ol/sm5.htm
    """
    MAX_EF = 2.5
    MIN_EF = 1.3
    min_review_interval = 3
    fraction = 0.8

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
            _n = OF_matrix[n-1][0]
            _EF = OF_matrix[n-1][1]
            return self._get_OF(n, EF) * self._get_IF(_n, _EF, OF_matrix)

    def _get_OF(self, n, EF):
        """Return optimum factor"""
        if n < 1:
            return self.min_review_interval
        return EF

    def _get_new_EF(self, EF, q):
        """Return new EF when learn(review) a word"""
        new_EF = EF + (0.1 - (5-q) * (0.08 + (5 - q) * 0.02))
        new_EF = self.MIN_EF if new_EF < self.MIN_EF else new_EF
        return new_EF

    def _get_new_OF_matrix(self, q, OF_matrix):
        """Return new OF_matrix when learn(review) a word"""
        n = len(OF_matrix)
        OF = OF_matrix[n-1][1]
        OF1 = OF * (0.72 + q * 0.07)
        OF2 = (1 - self.fraction) * OF + self.fraction * OF1
        OF_matrix.append((n, OF2))
        return OF_matrix

    def get_EF_by_first_score(self, score):
        """Return EF by first score"""
        return (self.MAX_EF - self.MIN_EF) / 5 * score + self.MIN_EF


learn_arithmetic = LearnArithmetic()

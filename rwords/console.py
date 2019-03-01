# -*-coding: utf8 -*-
import time
import json

from rwords.core import utills, settings


class ConsoleHander:
    """Command Line ConsoleHander"""

    def msg(self, msg):
        """Return msg to console"""
        print(msg)

    def error(self, errmsg):
        """Return error msg to console"""
        print("Error: {}".format(errmsg))

    def warning(self, warnign_msg):
        """Return warning msg to console"""
        print("Warning: {}".format(warnign_msg))

    def question(self, question_msg, chars=''):
        """Return question to console and Return ret to q"""
        hint = u"({})".format(u'/'.join(chars)) if chars else ''
        print(u'Q: {} {}'.format(question_msg, hint))
        q = utills.read_char(chars=chars)
        return q

    def input(self, question):
        txt = input(u'I:{}?'.format(question))
        return txt

    def learn_word(self, word_info):
        """Return the score of learn word"""
        self.msg(u"[' {} ']".format(word_info['word_name']))
        self.music(word_info['mp3']['path'])
        chr = self.question(u"Q: [j] 完全不会;  [k] 有印象; [l] 认识; [e] 熟悉", chars=u'jkle')
        self.msg('')
        self.msg(u"[' {} ']".format(word_info['word_name']))
        for tran_mean in word_info['tran_means']:
            self.msg(u'[{}] {}'.format(tran_mean['part'], '; '.join(json.loads(tran_mean['means']))))
        self.msg('')
        ret = self.question(u"[t] 答对了; [f] 答错了", chars=u'tf') if chr != 'j' else ''

        key = chr + ret
        key2score = {
            'j': 0, 'kf': 0, 'lf': 1, 'ef': 2, 'kt': 3, 'lt': 4, 'et': 5,
        }
        score = key2score[key]
        return score

    def review_words_page(self, word_infos, page, offset, word_count):
        """Review all words in memory store."""
        self.msg('ID\tword\t\tmin_mean\tEF\tnext review time\tcreate time\t')
        for word_info in word_infos:
            tran_means = word_info['tran_means']
            min_mean = json.loads(tran_means[0]['means'])[0]
            min_mean = min_mean.split(u'，')[0]
            line = u"{id}\t{word_name}\t\t{means}\t\t{EF}\t{next_review_time}\t\t{create_time}".format(
                id=word_info['id'],
                word_name=word_info['word_name'],
                ph=word_info['ph'],
                means=min_mean[: 10],
                EF=word_info['word_factor']["EF"],
                next_review_time=word_info['word_factor']['next_review_time'][: 10],
                create_time=word_info['create_time'][: 10],
            )
            self.msg(line)
        self.msg('page:{}\t\toffset:{}\t\tcount:{}'.format(page, offset, word_count))
        chr = self.question(u"[q]quit; [n]next page; [p]previous page [v] view detail;", chars=u'qnpv')
        return chr

    def view_word_info(self, word_info):
        self.msg(u"[ {} ]".format(word_info['word_name']))
        self.msg('')
        for tran_mean in word_info['tran_means']:
            self.msg(u'[{}] {}'.format(tran_mean['part'], '; '.join(json.loads(tran_mean['means']))))
        self.msg('')
        self.msg("EF: {}".format(word_info['word_factor']['EF']))
        self.msg("next_review_time: {}".format(word_info['word_factor']['next_review_time'][: 10]))
        self.msg("create_time: {}".format(word_info['create_time'][: 10]))
        self.msg('')
        self.msg('Q: {} {}'.format(u"[q]quit; [r]read;", u"({})".format(u'/'.join(u'qr'))))
        while True:
            chr = utills.read_char(chars='qr')
            if chr == 'r':
                self.music(word_info['mp3']['path'])
            elif chr == 'q':
                break
        return None

    def music(self, path):
        """paly music"""
        if not path:
            return False
        file_path = settings.BASE_DIR + path

        if settings.PYTHON_VERSION_3:  # compatibility py2
            import io as _io
        else:
            import StringIO as _io

        with utills.redirect_stdout(_io.StringIO()):
            import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        return True


console_hander = ConsoleHander()

# -*-coding: utf8 -*-
import time

from rwords.core import utills, settings


class Returns:
    """Command Line Returns"""

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


return_hander = Returns()

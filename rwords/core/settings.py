import os
import sys

# base settings
PYTHON_VERSION_3 = False if sys.version_info < (3, 0) else True
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = "/data/db/sqlite.db"
MP3_DIR = "/data/mp3/"

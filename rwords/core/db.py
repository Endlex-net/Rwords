import os
import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rwords.core import settings

db_path = settings.BASE_DIR + settings.DB_PATH
sql_url = 'sqlite:///{}'.format(db_path)
engine = create_engine(sql_url, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope(session=None):
    if session:
        yield session
    else:
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


def init_db():
    """Init db if sqlit.db is not create"""
    if not os.path.exists(db_path):
        from rwords.models import SysInfo
        Base.metadata.create_all(engine)

        # init some sys_info
        with session_scope() as session:
            session.add_all([
                SysInfo(key='review_list_time', value=datetime.datetime.now().strftime("%Y-%m-%d"))
            ])


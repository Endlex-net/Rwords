# -*-coding:utf8-*-
import enum

from sqlalchemy import Column, Integer, String, DateTime,  Float, Enum
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship

from rwords.core.db import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word_name = Column(String, unique=True, comment="单词")
    ph = Column(String(32), comment="英式音标")
    mp3 = relationship("Mp3", uselist=False, backref="word",)
    tran_means = relationship('TranMean', backref="word")
    word_factor = relationship("WordFactor", uselist=False, backref='word')
    create_time = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return "<Word({}: name='{}')>".format(self.id, self.word_name)


class TranMean(Base):
    __tablename__ = "means"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(Word.id))
    part = Column(String(10), comment="词性")
    means = Column(String(100), comment="含义")  # 解释 json([])


class Mp3(Base):
    __tablename__ = "mp3s"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(Word.id))
    url = Column(String(100), comment="网络url")
    path = Column(String(100), comment="本地下载地址")


class WordFactor(Base):
    __tablename__ = "word_factor"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(Word.id))
    EF = Column(Float, comment="easiness factor")
    OF_matrix = relationship("OptimumFactorMatrix")
    number = Column(Integer, comment="已复习次数")  # 出现一天算一次
    next_review_time = Column(DateTime)


class OptimumFactorMatrix(Base):
    __tablename__ = "OF_matrix"

    id = Column(Integer, primary_key=True)
    word_factor_id = Column(Integer, ForeignKey(WordFactor.id))
    OF = Column(Float, comment="optimal factor")
    number = Column(Integer, comment="复习次数")


class ReviewList(Base):
    __tablename__ = "review list"

    class WordType(enum.Enum):
        new = 0
        review = 1
        repeat = 3

    id = Column(Integer, primary_key=True)
    word_id = Column(ForeignKey(Word.id))
    word = relationship(Word, uselist=False)
    w_type = Column(Enum(WordType), comment="复习类型")
    repeat_count = Column(Integer, comment="重复次数")

    def __repr__(self):
        return "<ReviewList({}:word={})>".format(self.id, self.word.word_name)


class SysInfo(Base):
    __tablename__ = 'sys_info'

    id = Column(Integer, primary_key=True)
    key = Column(String, comment="key")
    value = Column(String, comment="value")
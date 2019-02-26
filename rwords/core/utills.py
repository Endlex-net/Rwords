# -*-coding: utf-8-*-
import sys
import datetime
import json
from contextlib import contextmanager

import requests
import readchar
from sqlalchemy.ext.declarative import DeclarativeMeta

from rwords.core import settings


def download_mp3(url, name):
    """download mp3 to local"""
    mp3_path = "{}{}.mp3".format(settings.MP3_DIR, name)
    r = requests.get(url)
    with open(settings.BASE_DIR + mp3_path, "wb") as mp3:
        mp3.write(r.content)
    return mp3_path


def read_char(chars=''):
    """Return a char from console"""
    hint = "({})".format('/'.join(chars)) if chars else ''
    while 1:
        chr = readchar.readchar()
        if (not chars) or (chr in chars):
            return chr
        print('options:{}'.format(hint))


def new_alchemy_encoder(revisit_self = False, fields_to_expand = []):
    """Return a json encoder for sqlachemy obj"""
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__, DeclarativeMeta)):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def dumps_alchemy(c, args):
    """dumps sqlalchemy obj"""
    return json.loads(json.dumps(c, cls=new_alchemy_encoder(False, args), check_circular=False))

@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target # replace sys.stdout
    try:
        yield new_target # run some code with the replaced stdout
    finally:
        sys.stdout = old_target # restore to the previous value
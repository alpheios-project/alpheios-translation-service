from atservices.models import Miss, Translation
import datetime


def insert_misses(db):
    """ Add all misses fixtures

    :param db: DB instance
    """

    Misses = [
        Miss(
            at=datetime.datetime(year=2018, month=1, day=1, hour=21, minute=0, second=0),
            lemma_lang="eng", lemma="bbq", translation_lang="fre", client="They"),
        Miss(
            at=datetime.datetime(year=2018, month=1, day=1, hour=20, minute=0, second=0),
            lemma_lang="fre", lemma="appétit", translation_lang="eng", client="Bocuse"),
        Miss(
            at=datetime.datetime(year=2018, month=1, day=1, hour=19, minute=0, second=0),
            lemma_lang="lat", lemma="lascivus", translation_lang="fre", client="Collatinus-Lemmatize")
    ]

    for x in Misses:
        db.session.add(x)
    db.session.commit()


Translations = [
#    Translation()
]

import os

FIXTURE_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_path(*paths):
    return os.path.join(FIXTURE_DATA_DIR, *paths)
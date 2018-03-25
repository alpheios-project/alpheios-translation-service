from unittest import TestCase
from ..fixtures import get_path

from atservices import create_app
from atservices.corpora.collatinus import CollatinusCorpus
from atservices.models import Translation


class TestCollatinusCorpus(TestCase):
    """ Tests for the modele Translation

    """
    def setUp(self):
        self.app, self.db = create_app("test")
        self.db.create_all(app=self.app)
        self.client = self.app.test_client()

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def test_ingest(self):
        """ Test that data are correctly ingested
        """
        with self.app.app_context():
            corpus = CollatinusCorpus("lat", "fre", source_file=get_path("collatinus.data"))
            corpus.ingest()

            results = corpus.translate(["abacus", "abalieno"], "fre")
            self.assertEqual(
                results,
                [
                    {"in": "abacus", "map": "abacus",
                     "translations": ["counting-board; side-board; slab table; panel; square stone on top of column;"]},
                    {"in": "abalieno", "map": "abalieno",
                     "translations": ["to transfer (sale/contract); to remove, take away, dispose of; to numb/deaden;"]}
                ],
                "Lemmatisation of ingested data should be possible"
            )
            results = corpus.translate(["abacus", "abalieno"], "eng")
            self.assertEqual(
                results,
                [
                    {"in": "abacus", "map": "abacus",
                     "translations": []},
                    {"in": "abalieno", "map": "abalieno",
                     "translations": []}
                ],
                "Lemmatisation of ingested data should be possible"
            )

            self.assertEqual(
                Translation.query.count(), 2,
                "Only two lemma should have been recorded"
            )

    def test_ingest_double_translation(self):
        """ Test that data are correctly ingested even when multiple corpora are
        used for the same language
        """
        with self.app.app_context():
            corpus = CollatinusCorpus("lat", "fre", source_file=get_path("collatinus.data"))
            corpus.ingest()
            corpus = CollatinusCorpus("lat", "fre", source_file=get_path("collatinus-ext.data"))
            corpus.ingest()

            results = corpus.translate(["abacus", "abalieno", "a"], "fre")
            self.assertEqual(
                results,
                [
                    {"in": "abacus", "map": "abacus",
                     "translations": ["counting-board; side-board; slab table; panel; square stone on top of column;",
                                      "Another one bites the dust"]},
                    {"in": "abalieno", "map": "abalieno",
                     "translations": ["to transfer (sale/contract); "
                                      "to remove, take away, dispose of; to numb/deaden;"]},
                    {"in": "a", "map": "a",
                     "translations": ["b"]},
                ],
                "Lemmatisation of ingested data should be possible"
            )
            results = corpus.translate(["abacus", "abalieno", "a"], "eng")
            self.assertEqual(
                results,
                [
                    {"in": "abacus", "map": "abacus",
                     "translations": []},
                    {"in": "abalieno", "map": "abalieno",
                     "translations": []},
                    {"in": "a", "map": "a",
                     "translations": []},

                ],
                "Lemmatisation of ingested data should be possible"
            )

            self.assertEqual(
                Translation.query.count(), 4,
                "Only two lemma should have been recorded"
            )

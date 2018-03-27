from unittest import TestCase
import json

from atservices import create_app
from atservices.corpora.collatinus import CollatinusCorpus
from atservices.models import Miss
from atservices.errors import NoInputError

from ..fixtures import get_path


class TestLatinBlueprint(TestCase):
    """ Tests for the modele Translation

    """
    def setUp(self):
        self.app, self.db = create_app("test")
        self.app.config['SERVER_NAME'] = 'localhost'
        self.db.create_all(app=self.app)
        self.client = self.app.test_client()

        with self.app.app_context():
            corpus = CollatinusCorpus("lat", "fre", source_file=get_path("collatinus.data"))
            corpus.ingest()
            corpus = CollatinusCorpus("lat", "unk", source_file=get_path("collatinus-ext.data"))
            corpus.ingest()

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def test_main_route(self):
        """ Test the list of language supported"""

        main_url = "http://localhost/lat"
        response = self.client.get("/lat/")
        data = json.loads(response.data.decode())
        self.assertEqual(

            sorted(data, key=lambda item: item["lang"]),
            # Test results should be ordered by item.lang
            [
                {"lang": "fre", "uri": main_url+"/fre"},
                {"lang": "unk", "uri": main_url+"/unk"}
            ],
            "Routes should reflect available corpora"
        )

    def test_no_input_failure(self):
        """ Test that forgetting input results in an error"""

        response = self.client.get("/lat/eng")
        self.assertEqual(
            response.status_code, 400,
            " The error code is correct"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(
            data, {"message": NoInputError.message},
            "Error message should code from error class"
        )

    def test_lemmatisation_route(self):
        """ Test the lemmatisation service route """

        results = self.client.get("/lat/fre?input=abacus,abalieno,a&client=ZERO")
        data = json.loads(results.data.decode())

        self.assertEqual(
            data,
            [
                {"in": "abacus", "map": "abacus",
                 "translations": ["counting-board; side-board; slab table; panel; square stone on top of column;"]},
                {"in": "abalieno", "map": "abalieno",
                 "translations": ["to transfer (sale/contract); "
                                  "to remove, take away, dispose of; to numb/deaden;"]},
                {"in": "a", "map": "a",
                 "translations": []},
            ],
            "Lemmatisation of ingested data should be possible"
        )

    def test_registered_misses(self):
        """ Test the lemmatisation service route """

        results = self.client.get("/lat/fre?input=a&client=ZERO")
        data = json.loads(results.data.decode())

        self.assertEqual(
            data, [{"in": "a", "map": "a", "translations": []}],
            "Lemmatisation of ingested data should be possible"
        )

        with self.app.app_context():
            self.assertEqual(
                len(Miss.query.filter(
                    Miss.translation_lang == "fre",
                    Miss.lemma == "a",
                    Miss.lemma_lang == "lat",
                    Miss.client == "ZERO"
                ).all()),
                1,
                "There should be 1 Miss record"
            )


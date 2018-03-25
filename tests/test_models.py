from atservices.models import Miss, Translation
from unittest import TestCase
from .fixtures import insert_misses
from atservices import create_app


class TestMiss(TestCase):
    def setUp(self):
        self.app, self.db = create_app("test")
        self.db.create_all(app=self.app)
        self.client = self.app.test_client()

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def test_absolute_clear(self):
        """ Check that complete clear is efficient
        """
        with self.app.app_context():
            insert_misses(self.db)

            self.assertEqual(
                Miss.query.count(), 3,
                "There should be 3 miss record from fixtures after insertion of misses"
            )
            Miss.clear_up_to()
            self.assertEqual(
                Miss.query.count(), 0,
                "All records should have been cleared"
            )

    def test_conditional_clear(self):
        """ Check that conditional clear is efficient
        """
        with self.app.app_context():
            insert_misses(self.db)

            self.assertEqual(
                Miss.query.count(), 3,
                "There should be 3 miss record from fixtures after insertion of misses"
            )
            Miss.clear_up_to(date="2018-01-01 19:59:00")
            self.assertEqual(
                Miss.query.count(), 2,
                "All records should have been cleared"
            )

    def test_csv_dump(self):
        """ Check that CSV dumps works
        """

        with self.app.app_context():
            insert_misses(self.db)
            self.assertEqual(
                Miss.get_csv(),
                """at	lemma	lemma_lang	translation_lang	client
2018-01-01 19:00:00	lascivus	lat	fre	Collatinus-Lemmatize
2018-01-01 20:00:00	appétit	fre	eng	Bocuse
2018-01-01 21:00:00	bbq	eng	fre	They""",
                "CSV DUMP should be correct"
            )

    def test_record_misses(self):
        """ Check that misses are registered
        """
        with self.app.app_context():
            result = Miss.register_misses([
                {"in": "lemma", "map": "map", "translations": []}
            ], "inp", "out", client="Client")

            self.assertEqual(
                Miss.query.count(), 1,
                "A record should have been done"
            )

    def test_record_misses_multiple(self):
        """ Check that misses are registered but not found data
        """
        with self.app.app_context():
            result = Miss.register_misses([
                {"in": "lemma1", "map": "map", "translations": []},
                {"in": "lemma2", "map": "map", "translations": ["hello"]},
                {"in": "lemma3", "map": "map", "translations": []}
            ], "inp", "out", client="Client")

            self.assertEqual(
                [(m.lemma, m.client) for m in Miss.query.all()],
                [("lemma1", "Client"), ("lemma3", "Client")],
                "A record should have been done"
            )


class TestTranslation(TestCase):
    """ Tests for the modele Translation

    """
    def setUp(self):
        self.app, self.db = create_app("test")
        self.db.create_all(app=self.app)
        self.client = self.app.test_client()

    def tearDown(self):
        self.db.drop_all(app=self.app)

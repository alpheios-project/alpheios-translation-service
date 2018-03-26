from unittest import TestCase
import os
import shutil
import requests_cache


# Using a requests cache to speed up ZIP downloading routines
requests_cache.install_cache("demo_cache")


from atservices import create_app
from atservices.scripts.collatinus import (
    download_collatinus_corpora,
    ingest_collatinus_corpora,
    check_collatinus_corpora,
    basedir_collatinus,
    change_basedir,
    collatinus_corpora
)


class TestCollatinusScripts(TestCase):
    """ Tests for the modele Translation

    """

    calls = []

    class QuickMock:
        @staticmethod
        def echo(message):
            TestCollatinusScripts.calls.append(message)

    def setUp(self):
        self.app, self.db = create_app("test")
        self.db.create_all(app=self.app)
        self.client = self.app.test_client()
        self.old = tuple([] + list(basedir_collatinus))
        self.current = change_basedir(
            os.path.split(
                os.path.abspath(
                    os.path.dirname(__file__)
                )
            ) +
            ("test_data", )
        )
        TestCollatinusScripts.calls = []

    def tearDown(self):
        self.db.drop_all(app=self.app)
        shutil.rmtree(os.path.join(*self.current), ignore_errors=True)
        change_basedir(self.old)

    def test_download(self):
        """ Test that data download works """
        self.assertEqual(
            check_collatinus_corpora(), False,
            "Data should not be available"
        )

        download_collatinus_corpora(cli=self.QuickMock)

        self.assertEqual(
            len(TestCollatinusScripts.calls), len(collatinus_corpora())
        )
        self.assertEqual(
            check_collatinus_corpora(), True,
            "Data should be available"
        )

    def test_download_without_cli(self):
        """ Test that data download works even when we do not use a CLI to emit message """
        self.assertEqual(
            check_collatinus_corpora(), False,
            "Data should not be available"
        )

        download_collatinus_corpora()

        self.assertEqual(
            check_collatinus_corpora(), True,
            "Data should be available"
        )

    def test_ingest_without_download(self):
        """ Test ingest without download """
        with self.app.app_context():
            with self.assertRaises(FileNotFoundError):
                ingest_collatinus_corpora()

            ingest_collatinus_corpora(self.QuickMock)
            self.assertEqual(
                TestCollatinusScripts.calls,
                ["[ERROR] No corpus found"],
                "An error message should have been displayed"
            )

    def test_ingest_(self):
        """ Test ingest with download """
        with self.app.app_context():
            download_collatinus_corpora()
            ingest_collatinus_corpora()
            # Need to figure what to test here.
            # Length of lemmas would be stupid because data can change.
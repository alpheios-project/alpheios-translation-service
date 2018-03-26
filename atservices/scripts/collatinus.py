import requests
import os
import glob
import zipfile
import io

from .. import basedir
from ..corpora.collatinus import CollatinusCorpus


LANGS = [
    ("eng", "lemmes.en"),
    ("eng", "lem_ext.en"),
    ("fre", "lemmes.fr"),
    ("fre", "lem_ext.fr"),
    ("por", "lemmes.pt"),  # Portuguese
    ("ita", "lemmes.it"),  # Italian
    ("ger", "lemmes.de"),  # German
    ("cat", "lemmes.ca"),  # Catalan
    ("glg", "lemmes.gl"),  # Galician
    ("spa", "lemmes.es"),  # Spanish
]

basedir_collatinus = basedir, "data", "collatinus"


def change_basedir(val):
    global basedir_collatinus
    basedir_collatinus = val
    return val


def collatinus_corpora():  # List of corpora from Collatinus sources
    global basedir_collatinus
    return [
        CollatinusCorpus("lat", lang, os.path.join(*basedir_collatinus, file))
        for lang, file in LANGS
    ]


def download_collatinus_corpora(cli=None):
    """ Download and extract the collatinus corpus
    """
    data = requests.get("https://github.com/biblissima/collatinus/archive/master.zip")
    file = zipfile.ZipFile(io.BytesIO(data.content))

    base = os.path.join(*basedir_collatinus)

    if not os.path.exists(base):
        os.makedirs(base)

    # For each corpus of the project
    for _, filename in LANGS:
        zip_path = os.path.join("collatinus-master", "bin", "data", filename)  # File in the ZIP
        extraction_path = os.path.join(base, filename)

        with open(extraction_path, mode="wb") as target_file:
            target_file.write(file.read(zip_path))

        if cli:
            cli.echo("--- Extracting {} to {}".format(zip_path, extraction_path))


def check_collatinus_corpora():
    """ Check if the corpora translations files were downloaded

    :return: Indicator of files availability
    :rtype: bool
    """

    downloaded = glob.glob(os.path.join(*basedir_collatinus, "*"))
    return len(downloaded) == len(collatinus_corpora())


def ingest_collatinus_corpora(cli=None):
    """ Ingest the corpora

    :param cli: Class, object or models that allows to use a ".echo()" function that
    will provide return information to the user
    """
    if not check_collatinus_corpora():
        if cli:
            cli.echo("[ERROR] No corpus found")
            return
        else:
            raise FileNotFoundError("The corpus were not downloaded.")
    for corpus in collatinus_corpora():
        count = corpus.ingest()
        if cli:
            cli.echo(
                "--- {count} words ingested "
                "in the database for {lang}".format(
                    count=count,
                    lang=corpus.translation_lang
                )
            )

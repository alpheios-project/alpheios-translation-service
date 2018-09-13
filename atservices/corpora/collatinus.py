from .base import Corpus
from ..models import Translation, db
import re


class CollatinusCorpus(Corpus):

    def __init__(self, lang, translation_lang=None, source_file=None):
        super(CollatinusCorpus, self).__init__(lang)
        self.translation_lang = translation_lang
        self.source_file = source_file

    @staticmethod
    def _make_tokens(line):
        """ Creates a token dictionary for a given line of Collatinus data

        :param line: Line from collatinus data
        :return: Dictionary with separated value for the token translation
        """
        line = line.split("!")[0].split(":")
        lemma, details = line[0], ":".join(line[1:])
        # some translations can be split into multiple
        translations = re.split(r'\d\s*[-\.]\s*',details)
        tokens = []
        for translation in translations:
            if translation:
                # clean up any trailing definition separators
                clean = re.sub(r'\s*-\s*$','',translation)
                tokens.append(
                    {
                        "translation": clean,
                        "lemma": lemma
                        }
                        )
        return tokens

    def ingest(self):
        """ Ingest given file and store its content for given lang
        """
        registered = 0
        with open(self.source_file) as source_file:
            for line in source_file.readlines():
                line = line.strip()
                # There is quite a number of files that are not completely nicely
                # written.
                # Normally :
                #   - ! means the line is commented
                #   - a colon : is separating translation and lang
                if not line.startswith("!")\
                        and ":" in line:
                    tokens = self._make_tokens(line)
                    for token in tokens:
                        db.session.add(Translation(
                            translation_lang=self.translation_lang,
                            lemma_lang=self.lang,
                            **token
                            ))
                        registered += 1
        db.session.commit()
        return registered

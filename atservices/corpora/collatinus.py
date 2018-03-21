from .base import Corpus
from ..models import Translation, db


class CollatinusCorpus(Corpus):

    def __init__(self, lang, translation_lang=None, source_file=None):
        super(CollatinusCorpus, self).__init__(lang)
        self.translation_lang = translation_lang
        self.source_file = source_file

    @staticmethod
    def _make_token(line):
        """ Creates a token dictionary for a given line of Collatinus data

        :param line: Line from collatinus data
        :return: Dictionary with separated value for the token translation
        """
        line = line.split("!")[0].split(":")
        lemma, translation = line[0], ":".join(line[1:])
        return {
            "translation": translation,
            "lemma": lemma
        }

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
                    db.session.add(Translation(
                        translation_lang=self.translation_lang,
                        lemma_lang=self.lang,
                        **self._make_token(line)
                    ))
                    registered += 1
        db.session.commit()
        return registered

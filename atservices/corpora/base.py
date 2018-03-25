from ..models import Translation, db
from abc import abstractmethod


class Corpus(object):
    """ A corpus is both an object for treating input data and building
    the database


    :param lang: Language of the lemmas
    """
    # Used for input correction
    _MAPPING_INPUT = {}
    # Used for translation correction
    _MAPPING_OUTPUT = {}

    def __init__(self, lang):
        self._lang = lang

    @property
    def capacities(self):
        """ Retrieves lang that the database holds translations for

        :return:
        """
        for lang, *_ in db.session.query(
            Translation.translation_lang
        ).filter(
            Translation.lemma_lang == self.lang
        ).group_by(
            Translation.translation_lang
        ).all():
            yield lang

    @abstractmethod
    def ingest(self, *args, **kwargs):
        """ Ingest data from a specific file or other kind of
        resources to put them into the database

        :return: Number of record inserted in the database
        :rtype: int
        """
        raise NotImplementedError()

    @property
    def mapping(self):
        """ For test purposes or documentation on the API

        :return: Dictionary representation of input and OUTPUT
        """
        return {
            "in": self._MAPPING_INPUT,
            "out": self._MAPPING_OUTPUT
        }

    @property
    def lang(self):
        return self._lang

    def translate(self, words, output_lang):
        """ Translate a list of words into an output lang

        :param words: List of words to translate
        :type words: [str]
        :param output_lang: Language in which to translate
        :type output_lang: str
        :return: List of translations
        """

        # We do the mapping from the client
        # Note : we might want the mapping to be done at ingestion time later (?)
        mapped = [
            (original, self.mapped_to(original))
            for original in words
        ]

        # We find translations
        translations = self._translate(
            [m for _, m in mapped],
            output_lang
        )

        # We order translation given the input order
        return [
            {
                "in": word,
                "map": mapped_value,
                "translations": translations.get(mapped_value, [])
            }
            for word, mapped_value in mapped
        ]

    def _translate(self, words, lang):
        """ Find translation for a multiple lemmas

        :param words: Lemmas needing translations
        :param lang: Lang to translate to
        :return: Dictionary of results where lemma is the key
        """
        lemmas = {}
        for token in Translation.query.filter(
            db.and_(
                Translation.lemma_lang == self.lang,
                Translation.translation_lang == lang,
                Translation.lemma.in_(set(words))
            )
        ).order_by(Translation.lemma).all():
            if token.lemma not in lemmas:
                lemmas[token.lemma] = [token.translation]
            else:
                lemmas[token.lemma].append(token.translation)

        return lemmas

    def mapped_to(self, word):
        """ For a given lemma, translate the input lemma into the dataset
        used value

        .. example:: Client is expected to send data such as "factus"
        but source translation only has "facio". The input is mapped to
        facio and the response keeps this information

        :param word: Word to check equivalency for
        :return: Word or equivalency
        """
        if word in self._MAPPING_INPUT:
            return self._MAPPING_INPUT[word]
        return word

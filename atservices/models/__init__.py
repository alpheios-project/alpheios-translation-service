from .. import db
import datetime


class Translation(db.Model):
    """ Translation of objects

    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lemma_lang = db.Column(db.String(3), index=True, nullable=False)
    translation_lang = db.Column(db.String(3), index=True, nullable=False)
    lemma = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.String(255), nullable=False)


class Miss(db.Model):
    """ Missed valued in the database

    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    at = db.Column(db.DateTime)
    lemma = db.Column(db.String(255), nullable=False)
    lemma_lang = db.Column(db.String(3), nullable=False)
    translation_lang = db.Column(db.String(3), nullable=False)
    client = db.Column(db.String(255))

    @staticmethod
    def get_csv():
        """ Gets a CSV dump of the Miss table

        :return: String CSV representation of the CSV
        """
        columns = ["at", "lemma", "lemma_lang", "translation_lang", "client"]
        csv = [columns]
        for data in Miss.query.all():
            csv.append(
                [
                    data.at,
                    data.lemma,
                    data.lemma_lang,
                    data.translation_lang,
                    data.client
                ]
            )

    @staticmethod
    async def register_misses(results, lemma_lang, translation_lang, client=""):
        """ Register misses in the translation database

        :param results: List of results from Corpus.translate()
        :param lemma_lang: Lang of the words given to the service
        :param translation_lang: Lang in which we wanted to translate
        :param client: Name of the client
        """
        for result in results:
            if not result["translations"]:
                db.session.add(Miss(
                    at=datetime.datetime.now()),
                    lemma=result["in"],
                    lemma_lang=lemma_lang,
                    translation_lang=translation_lang,
                    client=client
                )
        db.session.commit()

    @staticmethod
    def clear_up_to(date=None):
        """ Clear data up to today (By default) or the given date

        :param date: Date up to which we want to delete results
        """
        Miss.query.filter(Miss.at <= (date or datetime.datetime.now())).remove()


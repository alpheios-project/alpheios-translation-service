from .. import db


class Translation(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lemma_lang = db.Column(db.String(3), index=True, nullable=False)
    translation_lang = db.Column(db.String(3), index=True, nullable=False)
    lemma = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.String(255), nullable=False)

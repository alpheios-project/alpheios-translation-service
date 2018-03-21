from flask import Blueprint, request
from ..corpora.base import Corpus
from ..errors import NoInputError
from ..utils import generic_response

latin_api = Blueprint(
    'latin_api',
    __name__,
    url_prefix="/lat"
)
latin_corpus = Corpus("lat")


latin_copyright = """Latin translations are provided through the data made openly \
availably by http://biblissima.com/ and Collatinus"""


def response(content):
    json = generic_response(content)
    json.headers["Thanks-To"] = latin_copyright
    return json


@latin_api.route("/<output_lang>")
def translate(output_lang):
    """ Translate a given sentence of lemmas (!) into a given sentence

    Query parameters :

        - input : string formed of multiple lemmas separated by spaces

    :return: JSON Response with the content translater
    """
    input_sentence = request.args.get("input", None)
    if not input_sentence or not output_lang:
        raise NoInputError()
    words = input_sentence.split()
    return response(latin_corpus.translate(words, output_lang))

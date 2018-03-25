from flask import Blueprint
from ..corpora.base import Corpus
from ..utils import generic_response
from .base import capacities_builder, translate_builder


latin_api = Blueprint('latin_api', __name__, url_prefix="/lat")
latin_corpus = Corpus("lat")


latin_copyright = """Latin translations are provided through the data made openly \
availably by http://biblissima.com/ and Collatinus"""


def response(content):
    """ Formatting of response for JSONify

    :param content: Content to put to json
    :return: JSON Response
    """
    json = generic_response(content)
    json.headers["Thanks-To"] = latin_copyright
    return json


@latin_api.route("/")
def capacities():
    return capacities_builder(latin_corpus, response)


@latin_api.route("/<output_lang>")
def translate(output_lang):
    """ Translate a given sentence of lemmas (!) into a given sentence

    Query parameters :

        - input : string formed of multiple lemmas separated by spaces
        - client: string representing the name of the client

    :return: JSON Response with the content translater
    """
    return translate_builder(latin_corpus, output_lang, response)

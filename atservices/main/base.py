from flask import request, url_for
from ..models import Miss
from ..errors import NoInputError
from ..utils import generic_response


def capacities_builder(corpus, response_callback=None):
    """ Generates a capacities route based on a corpus

    :param corpus: Corpus to use
    :param response_callback: Callback that will be used to generated response
    :return: JSON Response
    """
    return (response_callback or generic_response)([
        {
            "lang": lang,
            "uri": url_for(".translate", output_lang=lang, _external=True)
        }
        for lang in corpus.capacities
    ])


def translate_builder(corpus, output_lang, response_callback=None):
    """ Translate a given sentence of lemmas (!) into a given sentence

    Query parameters :

        - input : string formed of multiple lemmas separated by comma
        - client: string representing the name of the client

    eg. ?input=lascivus puella&client=Collatinus

    :return: JSON Response with the content translater
    """
    input_sentence = request.args.get("input", None)
    client = request.args.get("client", "")

    if not input_sentence or not output_lang:
        raise NoInputError()

    words = input_sentence.split(",")
    results = corpus.translate(words, output_lang)

    Miss.register_misses(results, corpus.lang, output_lang, client)
    return (response_callback or generic_response)(results)

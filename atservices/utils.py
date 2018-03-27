from flask import jsonify
from flask.json import JSONEncoder


class NonEscapingJsonEncoder(JSONEncoder):
    """ This encoders avoid escaping UTF8 characted (eg. é into \u0133)"""
    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(NonEscapingJsonEncoder, self).__init__(**kwargs)


def generic_response(content):
    """ Creates a generic response

    :param content: Content that needs to be jsonified
    :return: JSON Response
    """
    json = jsonify(content)
    json.headers["Provided-by"] = "This service was built and funded by Alpheios.net"
    return json

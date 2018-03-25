from flask import jsonify


def generic_response(content):
    """ Creates a generic response

    :param content: Content that needs to be jsonified
    :return: JSON Response
    """
    json = jsonify(content)
    json.headers["Provided-by"] = "This service was built and funded by Alpheios.net"
    return json

from flask import jsonify


class NoInputError(Exception):
    message = "Input was missing"


def register_error_handler(app):
    """ Register a error handler on the blueprint

    :param blueprint: Blueprint on which to register the handler
    :type blueprint: flask.Blueprint or flask.Flask
    """
    @app.errorhandler(NoInputError)
    def no_input_error(error):
        response = jsonify({"message": error.message})
        response.status_code = 400
        return response
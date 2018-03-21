from flask import jsonify


def generic_response(content):
    json = jsonify(content)
    json.headers["Provided-by"] = "This service was built and funded by Alpheios.net"
    return json

"""Entry point for creating the flask app."""

import flask

from app.routes import resources


def create_app():
    """Create the flask app.

    :return: a flask app
    :rtype: flask.Flask
    """
    app = flask.Flask(__name__)
    url_prefix_delivery = f"/shortener"
    app.register_blueprint(resources.API_BP, url_prefix=url_prefix_delivery)

    # pylint: disable=unused-variable
    @app.errorhandler(404)
    def page_not_found(error):
        return flask.jsonify(errors=error.code, messages=str(error)), error.code

    @app.errorhandler(400)
    @app.errorhandler(422)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return flask.jsonify({"errors": messages}), err.code, headers
        return flask.jsonify({"errors": messages}), err.code

    return app


def _debug():
    """Run a Flask debug server."""
    flask_app = create_app()

    flask_app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    _debug()

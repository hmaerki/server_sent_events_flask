import os
import time
import json
import flask

import jinja2

APP = flask.Flask(__name__)
# This will force exceptions when a variable is missing in a template
APP.jinja_env.undefined = jinja2.StrictUndefined
APP.secret_key = b'_6#y2L"Ftrer\n\xec]/'
APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


def log_request(request):
    APP.logger.warning(f"request.accept_encodings: {request.accept_encodings}")
    APP.logger.warning(f"request.accept_mimetypes: {request.accept_mimetypes}")
    APP.logger.warning(f"request.access_route: {request.access_route}")
    APP.logger.warning(f"request.base_url: {request.base_url}")
    APP.logger.warning(f"request.charset: {request.charset}")
    APP.logger.warning(f"request.headers: {request.headers}")
    APP.logger.warning(f"request.is_json: {request.is_json}")
    APP.logger.warning(f"request.method: {request.method}")
    APP.logger.warning(f"request.referrer: {request.referrer}")
    APP.logger.warning(f"request.remote_addr: {request.remote_addr}")
    APP.logger.warning(f"request.scheme: {request.scheme}")
    APP.logger.warning(f"request.url: {request.url}")


@APP.route("/server_sent_events_stream")
def server_sent_events_stream():
    log_request(flask.request)

    def generate():
        try:
            APP.logger.warning("generate()")
            for i in range(20):
                APP.logger.warning(f"generate(): {i}")
                time.sleep(0.4)
                color = ("black", "black", "black", "blue", "red")[i % 5]
                html = f'<span style="color: {color}">{i},</span>'
                d = {"html": html}
                data = f"data: {json.dumps(d)}\n\n"
                yield data
        except Exception as e:
            APP.logger.warning(f"generate() Exception {e}")
            APP.log_exception(e)
            raise
        finally:
            APP.logger.warning("generate() done")

    return flask.Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache",
        "Connection": "keep-alive"},
    )


@APP.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    PORT = os.environ.get("FLASK_RUN_PORT", 5000)
    PORT = int(PORT)
    APP.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)

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


@APP.route("/server_sent_events_stream")
def server_sent_events_stream():
    def generate():
        for i in range(1000000):
            time.sleep(0.4)
            color = ('black', 'black', 'black', 'blue', 'red')[i%5]
            html = f'<span style="color: {color}">{i},</span>'
            # html = f'<span>{i}</span>'
            d = {"html": html }
            data = f"data: {json.dumps(d)}\n\n"
            yield data 

    return flask.Response(generate(), mimetype="text/event-stream")

@APP.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    PORT = os.environ.get("FLASK_RUN_PORT", 5000)
    PORT = int(PORT)
    APP.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)

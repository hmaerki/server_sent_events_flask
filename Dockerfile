FROM python:3.9.5-slim-buster

LABEL maintainer="hmaerki@github.com"

# RUN apt-get update \
#   && apt-get install -y util-linux procps \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt \
  && rm -rf /root/.cache

ENV FLASK_APP app/webapp.py
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_DEBUG FALSE
ENV FLASK_ENV production


# Uncomment the following two lines for debugging
# ENV FLASK_DEBUG TRUE
# ENV FLASK_ENV development

# Default port of Flask is 5000
EXPOSE 5000

WORKDIR /home/flask

ENV PYTHONPATH /home/flask
COPY ./app /home/flask/app
COPY ./cert_https /home/cert_https

CMD ["flask", "run"]
# CMD ["flask", "run", "--cert=/home/cert_https/cert.pem", "--key=/home/cert_https/key.pem"]

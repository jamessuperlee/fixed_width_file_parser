FROM            python:3.8.1-slim as base

WORKDIR         /opt/code/fwf_parser/

RUN             pip install -U pip

COPY            requirements.txt requirements.txt

FROM            base as app

COPY            fwf_parser/ fwf_parser/
COPY            setup.py setup.py
RUN             pip install .

ENTRYPOINT      ["parse"]

FROM            base as test

COPY            requirements_dev.txt requirements_dev.txt
RUN             pip install -r requirements_dev.txt

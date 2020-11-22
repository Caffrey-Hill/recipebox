#!/bin/sh

if [[ ! -d venv ]]; then
  python3 -m virtualenv venv
fi

export FLASK_APP=recipebox
export FLASK_ENV=development
export RECIPEBOX_SETTINGS=$PWD/dev.cfg
venv/bin/pip3 install .
venv/bin/python3 -m flask init-db
venv/bin/python3 -m flask run

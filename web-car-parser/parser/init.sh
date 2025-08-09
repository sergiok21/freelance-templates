#!/bin/bash

set -e

exec gunicorn --bind 0.0.0.0:8080 parser.wsgi:application

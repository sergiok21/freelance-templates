#!/bin/sh

set -e

export PYTHONPATH=.
export DJANGO_SETTINGS_MODULE=photo.photo.settings.test
pytest

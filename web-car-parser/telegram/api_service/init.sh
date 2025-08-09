#!/bin/bash

set -e

cd api_service

exec gunicorn --bind 0.0.0.0:8081 api_service.wsgi:application

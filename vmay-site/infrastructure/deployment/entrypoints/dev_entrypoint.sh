#!/bin/sh

set -e

echo "=== Run tests ==="
cd /app
/app/entrypoints/test_entrypoint.sh

echo "=== Start django server ==="
cd /app/photo
/app/entrypoints/app_entrypoint.sh

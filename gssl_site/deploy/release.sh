#!/usr/bin/env bash
# Release the current checkout: install, check, migrate, collect static.
#
# Run as the gssl user, after `git pull`:
#   sudo -u gssl /srv/gssl/app/gssl_site/deploy/release.sh
# then reload the site:
#   sudo systemctl reload gssl
#
# Stops at the first failure, so a broken release never reaches the reload.
set -euo pipefail

VENV="${VENV:-/srv/gssl/venv}"
export DJANGO_ENV_FILE="${DJANGO_ENV_FILE:-/etc/gssl/gssl.env}"
export DJANGO_SETTINGS_MODULE=config.settings.prod

cd "$(dirname "$0")/.."

"$VENV/bin/pip" install --quiet -r requirements.txt
"$VENV/bin/python" manage.py check --deploy --fail-level WARNING
"$VENV/bin/python" manage.py migrate --noinput
"$VENV/bin/python" manage.py collectstatic --noinput --verbosity 0

echo "Ready: $(git rev-parse --short HEAD). Now run: sudo systemctl reload gssl"

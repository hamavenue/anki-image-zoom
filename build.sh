#!/usr/bin/env bash
# Package src/ as an .ankiaddon for AnkiWeb or manual install.
# The archive must hold the add-on's files at its root, with no enclosing folder.
set -euo pipefail
cd "$(dirname "$0")"
rm -f image_zoom.ankiaddon
(cd src && zip -q -r ../image_zoom.ankiaddon . -x '__pycache__/*' -x '*.pyc' -x 'meta.json')
echo "built image_zoom.ankiaddon"

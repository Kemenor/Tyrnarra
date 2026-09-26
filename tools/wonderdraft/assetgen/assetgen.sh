#!/bin/bash
# Run assetgen.py in its own gitignored virtualenv (numpy, scipy, pillow), created on first run.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -x "$DIR/.venv/bin/python" ] || ! "$DIR/.venv/bin/python" -c "import numpy, scipy, PIL" 2>/dev/null; then
    echo "assetgen: setting up $DIR/.venv (numpy, scipy, pillow)..." >&2
    python3 -m venv "$DIR/.venv" >&2
    "$DIR/.venv/bin/pip" install -q --disable-pip-version-check numpy scipy pillow >&2
fi
exec "$DIR/.venv/bin/python" "$DIR/assetgen.py" "$@"

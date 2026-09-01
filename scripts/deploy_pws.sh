#!/usr/bin/env bash
# Minimal deploy helper for PWS (run from your local machine that has SSH access)
# Usage:
#   export PWS_SSH="user@host"
#   export PWS_PROJECT_DIR="/path/to/project/on/server"
#   export VENV_PATH="/path/to/venv/on/server"    # optional
#   export RESTART_CMD="sudo systemctl restart gunicorn"  # optional
#   ./scripts/deploy_pws.sh

set -euo pipefail

: "${PWS_SSH:?set PWS_SSH (user@host)}"
: "${PWS_PROJECT_DIR:?set PWS_PROJECT_DIR}
"

SSH="$PWS_SSH"
PROJECT_DIR="$PWS_PROJECT_DIR"
VENV_PATH="${VENV_PATH:-}"
RESTART_CMD="${RESTART_CMD:-}"

echo "Starting deploy to $SSH:$PROJECT_DIR"

ssh "$SSH" bash -s -- "$PROJECT_DIR" "$VENV_PATH" "$RESTART_CMD" <<'EOF'
set -euo pipefail
PROJECT_DIR="$1"
VENV_PATH="$2"
RESTART_CMD="$3"

cd "$PROJECT_DIR"

# Ensure .env.prod has PRODUCTION=False
if [ -f .env.prod ]; then
  if grep -q '^PRODUCTION=' .env.prod; then
    sed -i 's/^PRODUCTION=.*/PRODUCTION=False/' .env.prod || true
  else
    echo 'PRODUCTION=False' >> .env.prod
  fi
else
  echo 'PRODUCTION=False' > .env.prod
fi

# Activate virtualenv if given
if [ -n "$VENV_PATH" ]; then
  if [ -f "$VENV_PATH/bin/activate" ]; then
    # shellcheck disable=SC1090
    source "$VENV_PATH/bin/activate"
  else
    echo "Warning: venv not found at $VENV_PATH, continuing without venv"
  fi
fi

pip install -r requirements.txt || true

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

if [ -n "$RESTART_CMD" ]; then
  echo "Running restart command: $RESTART_CMD"
  eval "$RESTART_CMD"
fi

echo "Deploy finished on remote host."
EOF

echo "Done."

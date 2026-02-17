#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${ROOT_DIR}/backend"
python3 -m pip install --upgrade pip
python3 -m pip install flask flask-cors python-dotenv sqlalchemy oracledb pymysql

cd "${ROOT_DIR}/frontend"
npm install

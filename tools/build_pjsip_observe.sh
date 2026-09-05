#!/usr/bin/env bash
set -euo pipefail
PJ=${PJPROJECT_ROOT:-/opt/atlas/pjproject}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck disable=SC1091
source "$PJ/build.mak"
cc -O2 -Wall -o "$ROOT/tools/pjsip_observe" "$ROOT/tools/pjsip_observe.c" \
  $APP_CFLAGS $APP_LDFLAGS $APP_LDLIBS
echo "built $ROOT/tools/pjsip_observe"

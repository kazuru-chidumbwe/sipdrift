#!/bin/bash
# Start sipdrift Kamailio observe listener (Host B / lab).
set -euo pipefail
export PATH="/usr/sbin:/usr/bin:/bin:${PATH:-}"
ROOT="${SIPDRIFT_ROOT:-/opt/atlas/repos/sipdrift}"
CFG="$ROOT/tools/kamailio/sipdrift-observe.cfg"
PIDFILE=/tmp/sipdrift-kamailio.pid
OBS=/tmp/sipdrift-kamailio-obs.json
RUNDIR=/tmp/sipdrift-kamailio-run
KAMAILIO_BIN="${KAMAILIO_BIN:-$(command -v kamailio || true)}"
if [[ -z "$KAMAILIO_BIN" && -x /usr/sbin/kamailio ]]; then
  KAMAILIO_BIN=/usr/sbin/kamailio
fi
if [[ -z "$KAMAILIO_BIN" ]]; then
  echo "kamailio binary not found (tried PATH and /usr/sbin/kamailio)" >&2
  exit 2
fi

mkdir -p "$RUNDIR"
# also help distro default if run_dir ignored
sudo mkdir -p /var/run/kamailio 2>/dev/null || true
sudo chown "$(id -u)":"$(id -g)" /var/run/kamailio 2>/dev/null || true

if [[ ! -f "$CFG" ]]; then
  echo "missing $CFG" >&2
  exit 2
fi

# Stop previous instance
if [[ -f "$PIDFILE" ]]; then
  kill "$(cat "$PIDFILE")" 2>/dev/null || true
  rm -f "$PIDFILE"
fi
pkill -f "kamailio.*sipdrift-observe.cfg" 2>/dev/null || true
sleep 0.3
rm -f "$OBS"

# Validate config
"$KAMAILIO_BIN" -f "$CFG" -c

# Foreground-friendly daemonize with pid
"$KAMAILIO_BIN" -f "$CFG" -P "$PIDFILE" -DD -E &
sleep 0.8
if [[ ! -f "$PIDFILE" ]]; then
  # some builds write pid late
  sleep 0.8
fi
echo "kamailio observe listening (bin=$KAMAILIO_BIN cfg=$CFG pidfile=$PIDFILE)"
ss -ulnp | grep 5090 || netstat -ulnp 2>/dev/null | grep 5090 || true

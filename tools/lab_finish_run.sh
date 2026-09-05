#!/bin/bash
set -euo pipefail
cd /opt/atlas/repos/sipdrift
python3 tools/gen_extra_fixtures.py >/dev/null || true
python3 tools/gen_torture_fixtures.py
python3 tools/normalize_fixtures.py
: > fixtures/malformed_start.sip
/opt/atlas/venvs/sipdrift/bin/pip install -q -e '.[dev]'
export SIPDRIFT_SOFIA_OBSERVE=/opt/atlas/repos/sipdrift/tools/sofia_observe
export SIPDRIFT_PJSIP_OBSERVE=/opt/atlas/repos/sipdrift/tools/pjsip_observe
# kill stale responders
pkill -f sip_udp_responder.py 2>/dev/null || true
/opt/atlas/venvs/sipdrift/bin/python -m pytest -q
/opt/atlas/venvs/sipdrift/bin/python -m sipdrift.cli fixtures | wc -l
/opt/atlas/venvs/sipdrift/bin/python tools/run_hostb_experiments.py

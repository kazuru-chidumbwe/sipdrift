#!/bin/bash
set -euo pipefail
cd /opt/atlas/repos/sipdrift
python3 tools/gen_extra_fixtures.py >/dev/null
python3 tools/normalize_fixtures.py >/dev/null
# malformed must stay empty
: > fixtures/malformed_start.sip
cd tools
make sofia
make pjsip PJDIR=/opt/atlas/pjproject
ls -la sofia_observe pjsip_observe
echo '--- sofia 200 ---'
./sofia_observe ../fixtures/response_200_min.sip
echo '--- pjsip 200 ---'
./pjsip_observe ../fixtures/response_200_min.sip
echo '--- pjsip invite ---'
./pjsip_observe ../fixtures/invite_min.sip
echo '--- pjsip compact ---'
./pjsip_observe ../fixtures/compact_via.sip
cd /opt/atlas/repos/sipdrift
/opt/atlas/venvs/sipdrift/bin/pip install -q -e '.[dev]'
export SIPDRIFT_SOFIA_OBSERVE=/opt/atlas/repos/sipdrift/tools/sofia_observe
export SIPDRIFT_PJSIP_OBSERVE=/opt/atlas/repos/sipdrift/tools/pjsip_observe
/opt/atlas/venvs/sipdrift/bin/python -m sipdrift.cli drivers
/opt/atlas/venvs/sipdrift/bin/python -m sipdrift.cli fixtures | wc -l
/opt/atlas/venvs/sipdrift/bin/python tools/run_hostb_experiments.py

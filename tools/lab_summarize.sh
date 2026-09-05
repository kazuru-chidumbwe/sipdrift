#!/bin/bash
set -euo pipefail
PACK=/opt/atlas/sipdrift-packs/sipdrift-hostb-20260905T010835Z
python3 - <<'PY'
import json
from pathlib import Path
p = Path("/opt/atlas/sipdrift-packs/sipdrift-hostb-20260905T010835Z/E-suite-builtin-vs-sofia-lab.json")
d = json.loads(p.read_text())
print("summary", d["summary"])
for c in d["cases"]:
    if c["status"] == "diverge":
        print("DIVERGE", c["fixture_id"])
        print(" notes:", c["notes"])
        print(" left:", c["left"]["start_line"], c["left"]["via"], c["left"]["cseq"])
        print(" right:", c["right"]["start_line"], c["right"]["via"], c["right"]["cseq"])
p2 = Path("/opt/atlas/sipdrift-packs/sipdrift-hostb-20260905T010835Z/E-suite-pjsip-lab-vs-sofia-lab.json")
d2 = json.loads(p2.read_text())
print("pjsip-vs-sofia", d2["summary"])
for c in d2["cases"]:
    if c["status"] in ("diverge", "error"):
        print(c["status"].upper(), c["fixture_id"], c["notes"][:2] if c["notes"] else [])
PY
cd /opt/atlas/repos/sipdrift
/opt/atlas/venvs/sipdrift/bin/python -m pytest -q 2>&1 | tail -50

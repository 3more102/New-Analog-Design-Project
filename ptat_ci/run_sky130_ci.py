#!/usr/bin/env python3
"""Minimal reproducible SKY130/ngspice execution harness for the PTAT project.

This CI harness is intentionally small. It runs the same two sensor concepts
used by the ISSCC27 notebook: (1) ideal equal-current PTAT reference and
(2) a first-order PMOS-mirror-biased implementation. Raw CSVs and a manifest
are uploaded by GitHub Actions and are not treated as project evidence until
retrieved and independently validated.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

TEMPS = (-40, -20, 0, 25, 50, 75, 100, 125)
CORNERS = ("tt", "ff", "ss")
VDD = 1.8
IBIAS = 100e-9
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_model() -> Path:
    roots = [
        Path(os.environ.get("PDK_ROOT", "")),
        Path.home() / "pdk",
        Path.home() / ".volare",
    ]
    candidates = []
    for root in roots:
        if not str(root) or not root.exists():
            continue
        candidates.extend(root.rglob("sky130.lib.spice"))
    if not candidates:
        raise SystemExit("sky130.lib.spice not found")
    preferred = [p for p in candidates if "sky130A/libs.tech/ngspice" in str(p)]
    return sorted(preferred or candidates)[0]


def run_ngspice(netlist: str, stem: str) -> dict[str, float]:
    net = RESULTS / f"{stem}.spice"
    log = RESULTS / f"{stem}.log"
    net.write_text(netlist, encoding="utf-8")
    proc = subprocess.run(
        ["ngspice", "-b", "-o", str(log), str(net)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else proc.stdout
    if proc.returncode != 0:
        raise RuntimeError(f"ngspice failed for {stem}:\n{text[-4000:]}")
    match = re.search(r"PTAT_RESULT\s+([^\n\r]+)", text)
    if not match:
        raise RuntimeError(f"PTAT_RESULT missing for {stem}:\n{text[-4000:]}")
    values = [float(x) for x in match.group(1).split()]
    if len(values) != 7:
        raise RuntimeError(f"Expected 7 values, got {values!r}")
    return dict(zip(
        ("vgs_small_v", "vgs_large_v", "dvgs_v", "supply_current_a", "power_w", "branch_small_a", "branch_large_a"),
        values,
    ))


def ideal_netlist(model: Path, corner: str, temp: int) -> str:
    return f"""* PTAT ideal-current reference\n.lib \"{model}\" {corner}\n.temp {temp}\nVDD vdd 0 {VDD}\nI1 vdd v1 DC {IBIAS}\nI2 vdd v2 DC {IBIAS}\nXMN1 v1 v1 0 0 sky130_fd_pr__nfet_01v8 L=0.50 W=1.00\nXMN2 v2 v2 0 0 sky130_fd_pr__nfet_01v8 L=0.50 W=8.00\n.control\nset noaskquit\nop\nlet dvgs=v(v1)-v(v2)\nlet isupply=-i(VDD)\nlet psupply=v(vdd)*isupply\necho PTAT_RESULT $&v(v1) $&v(v2) $&dvgs $&isupply $&psupply {IBIAS} {IBIAS}\nquit\n.endc\n.end\n"""


def mirror_netlist(model: Path, corner: str, temp: int) -> str:
    return f"""* PTAT PMOS-mirror-biased implementation\n.lib \"{model}\" {corner}\n.temp {temp}\nVDD vdd 0 {VDD}\nIREFBIAS pref 0 DC {IBIAS}\nXMPREF pref pref vdd vdd sky130_fd_pr__pfet_01v8 L=1.00 W=4.00\nXMP1 p1 pref vdd vdd sky130_fd_pr__pfet_01v8 L=1.00 W=4.00\nXMP2 p2 pref vdd vdd sky130_fd_pr__pfet_01v8 L=1.00 W=4.00\nVPROBE1 p1 v1 DC 0\nVPROBE2 p2 v2 DC 0\nXMN1 v1 v1 0 0 sky130_fd_pr__nfet_01v8 L=0.50 W=1.00\nXMN2 v2 v2 0 0 sky130_fd_pr__nfet_01v8 L=0.50 W=8.00\n.control\nset noaskquit\nop\nlet dvgs=v(v1)-v(v2)\nlet isupply=-i(VDD)\nlet psupply=v(vdd)*isupply\nlet ib1=abs(i(VPROBE1))\nlet ib2=abs(i(VPROBE2))\necho PTAT_RESULT $&v(v1) $&v(v2) $&dvgs $&isupply $&psupply $&ib1 $&ib2\nquit\n.endc\n.end\n"""


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    fields = ["temp_c", "vgs_small_v", "vgs_large_v", "dvgs_v", "supply_current_a", "power_w", "branch_small_a", "branch_large_a"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if shutil.which("ngspice") is None:
        raise SystemExit("ngspice not found")
    model = find_model()
    print("ngspice:", subprocess.check_output(["ngspice", "-v"], text=True, stderr=subprocess.STDOUT).splitlines()[0])
    print("model:", model)

    generated = []
    for topology, builder in (("ideal", ideal_netlist), ("mirror", mirror_netlist)):
        for corner in CORNERS:
            rows = []
            for temp in TEMPS:
                vals = run_ngspice(builder(model, corner, temp), f"{topology}_{corner}_{temp:+d}C")
                vals["temp_c"] = temp
                rows.append(vals)
            out = RESULTS / f"{topology}_{corner}.csv"
            write_csv(out, rows)
            generated.append(out)

    manifest = {
        "status": "PASS",
        "pdk_model": str(model),
        "pdk_model_sha256": sha256(model),
        "pdk_version": os.environ.get("PDK_VERSION", "unknown"),
        "vdd_v": VDD,
        "bias_current_a": IBIAS,
        "temperatures_c": list(TEMPS),
        "corners": list(CORNERS),
        "files": {p.name: sha256(p) for p in generated},
    }
    (RESULTS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

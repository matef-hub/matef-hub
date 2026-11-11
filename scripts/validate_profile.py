#!/usr/bin/env python3
"""Offline GitHub profile asset and link checks, no network requests."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
readme=(root/"README.md").read_text(encoding="utf-8")
errors=[]
refs=re.findall(r'(?:src|href)="(\./assets/[^"]+\.svg)"',readme)
expected={
    "v2-hero","v2-ahkam","v2-agenda","v2-deadlines",
    "v2-smart","v2-management","v2-research",
    "v2-research-pipeline","v2-tech-matrix"
}
expected.update(f"v2-icon-{x}" for x in ("ahkam","agenda","deadlines","smart","management","research"))
for stem in expected:
    if f"./assets/{stem}.svg" not in refs:
        errors.append(f"Unreferenced intended SVG: {stem}")
for ref in refs:
    path=root/ref.removeprefix("./")
    if not path.exists():
        errors.append(f"Missing image: {ref}")
for svg in sorted((root/"assets").glob("v2-*.svg")):
    try:
        parsed=ET.parse(svg)
        elem=parsed.getroot()
        if not elem.tag.endswith("svg"):
            errors.append(f"Not an SVG document: {svg}")
        if not elem.find("{http://www.w3.org/2000/svg}title") is not None:
            errors.append(f"Missing accessible title: {svg}")
        if not elem.find("{http://www.w3.org/2000/svg}desc") is not None:
            errors.append(f"Missing accessible description: {svg}")
    except ET.ParseError as exc:
        errors.append(f"Malformed XML {svg}: {exc}")
for name in ("ahkam-app","agenda","Egyptian-Legal-Deadlines-Calculator","SmartLawyer","Legal-management-666","smart-lawyer-ai-training"):
    if f"https://github.com/matef-hub/{name}" not in readme:
        errors.append(f"Missing verified repository link: {name}")
if len(set(refs)) != len(expected):
    errors.append(f"Expected {len(expected)} unique V2 illustration links, found {len(set(refs))}")
if "not a claimed application screenshot" not in readme:
    errors.append("Missing illustration authenticity disclaimer")
if errors:
    for err in errors:
        print("ERROR:", err, file=sys.stderr)
    sys.exit(1)
print(f"Verified {len(set(refs))} linked illustrations and six project destinations.")

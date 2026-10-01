#!/usr/bin/env python3
"""Merge multiple NeTEx datasets into a single zip.

The _stops.xml file of each input is renamed using the input's file name
without the .zip extension, so the inputs do not collide, e.g.:
    norway.zip: _stops.xml -> _stops_norway.xml
    sweden.zip: _stops.xml -> _stops_sweden.xml

Usage: merge_netex.py <output-zip> <input-zip> [<input-zip> ...]
"""
import os
import sys
import zipfile


def dataset_name(path: str) -> str:
    base = os.path.basename(path)
    return base[:-4] if base.lower().endswith(".zip") else base


def merge(output: str, inputs: list[str]) -> None:
    tmp = output + ".tmp"
    seen = set()
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as out:
        for src in inputs:
            stops_name = f"_stops_{dataset_name(src)}.xml"
            renamed = False
            with zipfile.ZipFile(src) as zin:
                for info in zin.infolist():
                    if info.is_dir():
                        continue
                    name = info.filename
                    if os.path.basename(name) == "_stops.xml":
                        name = os.path.join(os.path.dirname(name), stops_name)
                        renamed = True
                    if name in seen:
                        sys.exit(f"Duplicate entry {name} found when merging {src}")
                    seen.add(name)
                    with zin.open(info) as fin, out.open(name, "w", force_zip64=True) as fout:
                        while chunk := fin.read(1 << 20):
                            fout.write(chunk)
            if not renamed:
                sys.exit(f"No _stops.xml found in {src}")
            print(f"Added {src} (_stops.xml -> {stops_name})")
    os.replace(tmp, output)
    print(f"Wrote {output} with {len(seen)} entries")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    merge(sys.argv[1], sys.argv[2:])

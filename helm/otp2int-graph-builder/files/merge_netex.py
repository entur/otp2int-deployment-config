#!/usr/bin/env python3
"""Merge multiple NeTEx datasets into a single zip.

The _stops.xml file of each input is renamed using the input's file name
without the .zip extension, so the inputs do not collide, e.g.:
    norway.zip: _stops.xml -> _stops_norway.xml
    sweden.zip: _stops.xml -> _stops_sweden.xml

Usage: merge_netex.py <output-zip> <input-zip> [<input-zip> ...]
"""
import json
import logging
import os
import sys
import zipfile
from datetime import datetime, timezone


class CloudLoggingFormatter(logging.Formatter):
    """Format records as JSON so Google Cloud Logging picks up the severity."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc)
        entry = {
            "timestamp": timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "severity": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            entry["message"] += "\n" + self.formatException(record.exc_info)
        return json.dumps(entry)


log = logging.getLogger("merge_netex")


def fail(message: str) -> None:
    log.error(message)
    sys.exit(1)


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
                        log.warning(f"Skipping directory {info.filename} in {src}")
                        continue
                    name = info.filename
                    if os.path.basename(name) == "_stops.xml":
                        name = os.path.join(os.path.dirname(name), stops_name)
                        renamed = True
                    if name in seen:
                        fail(f"Duplicate entry {name} found when merging {src}")
                    seen.add(name)
                    with zin.open(info) as fin, out.open(name, "w", force_zip64=True) as fout:
                        while chunk := fin.read(1 << 20):
                            fout.write(chunk)
            if not renamed:
                fail(f"No _stops.xml found in {src}")
            log.info(f"Added {src} (_stops.xml -> {stops_name})")
    os.replace(tmp, output)
    log.info(f"Wrote {output} with {len(seen)} entries")


if __name__ == "__main__":
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CloudLoggingFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    merge(sys.argv[1], sys.argv[2:])

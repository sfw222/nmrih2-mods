"""Verify published packages and rebuild catalog.json. Run from this repository."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "mods"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def version_key(version: str) -> tuple[int, ...]:
    if not re.fullmatch(r"\d+(?:\.\d+)*", version):
        raise ValueError(f"Version must be numeric: {version}")
    return tuple(int(part) for part in version.split("."))


def main() -> None:
    catalog = []
    for mod_root in sorted(MODS.iterdir()):
        if not mod_root.is_dir():
            continue
        versions = [item for item in mod_root.iterdir() if item.is_dir()]
        if not versions:
            continue
        release = max(versions, key=lambda item: version_key(item.name))
        manifest = json.loads((release / "manifest.json").read_text(encoding="utf-8"))
        if manifest["id"] != mod_root.name or manifest["version"] != release.name:
            raise ValueError(f"Manifest identity mismatch: {release}")
        files = []
        for item in manifest["files"]:
            name = item["name"]
            if Path(name).name != name or name in (".", ".."):
                raise ValueError(f"Unsafe filename: {name}")
            path = release / name
            actual = sha256(path)
            if actual != item["sha256"].upper():
                raise ValueError(f"SHA-256 mismatch: {path}")
            files.append({
                "name": name,
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": actual,
                "size": path.stat().st_size,
            })
        catalog.append({
            "id": manifest["id"],
            "name": manifest["name"],
            "version": manifest["version"],
            "notes": manifest.get("notes", ""),
            "files": files,
        })
    output = ROOT / "catalog.json"
    output.write_text(json.dumps({"schema": 1, "mods": catalog}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {len(catalog)} mods: {output}")


if __name__ == "__main__":
    main()

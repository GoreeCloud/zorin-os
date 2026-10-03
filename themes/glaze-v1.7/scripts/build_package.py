#!/usr/bin/env python3
"""Build a deterministic Development archive for the GoreeCloud Glaze theme."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "metadata" / "theme.json"


def copy_payload(destination: Path, package_name: str) -> Path:
    payload = destination / package_name
    payload.mkdir(parents=True)

    shutil.copy2(ROOT / "README.md", payload / "README.md")
    shutil.copytree(ROOT / "metadata", payload / "metadata")
    shutil.copytree(ROOT / "variants", payload / "variants")

    scripts = payload / "scripts"
    scripts.mkdir()
    for name in ("install.sh", "uninstall.sh", "validate.sh"):
        shutil.copy2(ROOT / "scripts" / name, scripts / name)

    return payload


def deterministic_tar_gz(source_root: Path, package_name: str, output: Path) -> None:
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as tf:
                root = source_root / package_name
                paths = [root, *sorted(root.rglob("*"), key=lambda p: p.as_posix())]
                for path in paths:
                    arcname = Path(package_name) / path.relative_to(root)
                    info = tf.gettarinfo(str(path), arcname=str(arcname))
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    if path.is_file():
                        with path.open("rb") as handle:
                            tf.addfile(info, handle)
                    else:
                        tf.addfile(info)


def main() -> int:
    out_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(["bash", str(ROOT / "scripts" / "validate.sh")], check=True)

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    version = metadata["version"]
    package_name = f"goreecloud-glaze-zorin-{version}"
    archive = out_dir / f"{package_name}.tar.gz"
    checksum = out_dir / f"{package_name}.tar.gz.sha256"

    if archive.exists() or checksum.exists():
        raise SystemExit(
            f"Refusing to overwrite an existing build artifact in {out_dir}; "
            "use a clean output directory."
        )

    with tempfile.TemporaryDirectory(prefix="goreecloud-glaze-package-") as temp:
        temp_root = Path(temp)
        copy_payload(temp_root, package_name)
        deterministic_tar_gz(temp_root, package_name, archive)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    print(archive)
    print(checksum.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

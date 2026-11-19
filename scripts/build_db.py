#!/usr/bin/env python3
"""Build a MiSTer Downloader database from the upstream Amstrad latest release."""
import hashlib
import json
import os
import pathlib
import urllib.request
import zipfile
import io

REPO = "renaudguerin/Amstrad_MiSTer"
DB_ID = "renaudguerin_amstrad_cpc_plus"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
BOOT_ROM = f"https://raw.githubusercontent.com/{REPO}/master/roms/boot.rom"
OUT = pathlib.Path("db/db.json.zip")

def fetch(url):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Amstrad-MiSTer-Downloader-DB",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read()

def file_record(data, url, tangle=None):
    record = {
        "hash": hashlib.md5(data).hexdigest(),
        "size": len(data),
        "url": url,
        "overwrite": True,
    }
    if tangle:
        record["tangle"] = [tangle]
    return record

def main():
    release = json.loads(fetch(API))
    assets = [a for a in release.get("assets", []) if a["name"].lower().endswith(".rbf")]
    if not assets:
        raise RuntimeError("Latest upstream release has no .rbf asset.")
    # If a release ever contains more than one RBF, prefer the Amstrad build.
    assets.sort(key=lambda a: ("amstrad" not in a["name"].lower(), a["name"]))
    asset = assets[0]
    rbf_data = fetch(asset["browser_download_url"])
    boot_data = fetch(BOOT_ROM)

    files = {
        f"_Computer/{asset['name']}": file_record(
            rbf_data, asset["browser_download_url"], "amstrad_cpc_plus_core"
        ),
        "Games/Amstrad/boot.rom": file_record(boot_data, BOOT_ROM),
    }
    folders = {
        "_Computer/": {},
        "Games/": {},
        "Games/Amstrad/": {},
    }
    database = {
        "v": 1,
        "db_id": DB_ID,
        "timestamp": int(__import__("time").time()),
        "files": files,
        "folders": folders,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(database, separators=(",", ":"), sort_keys=True).encode()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("db.json", raw)

    print(f"Built {OUT}")
    print(f"Release: {release.get('tag_name')} ({asset['name']})")
    print(f"RBF bytes: {len(rbf_data)}; boot.rom bytes: {len(boot_data)}")

if __name__ == "__main__":
    main()

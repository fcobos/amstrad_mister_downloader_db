# Amstrad MiSTer custom Downloader database

This repository builds a MiSTer Downloader database for
https://github.com/renaudguerin/Amstrad_MiSTer

## Setup

1. Create a **public** GitHub repository for these files.
2. Upload the contents of this folder to its `main` branch.
3. In the repository, open **Settings → Actions → General → Workflow permissions**
   and allow read/write permissions (or keep the workflow's explicit contents: write permission).
4. Run **Actions → Build MiSTer Downloader database → Run workflow** once.
5. Confirm that `db/db.json.zip` has been created in the repository.
6. Add the following section to `/media/fat/downloader.ini` on your MiSTer,
   replacing `YOUR_GITHUB_USER/YOUR_REPOSITORY`:

```ini
[renaudguerin_amstrad_cpc_plus]
db_url = https://raw.githubusercontent.com/YOUR_GITHUB_USER/YOUR_REPOSITORY/main/db/db.json.zip
description = Renaud Guerin Amstrad CPC Plus/GX4000 core
```

7. Run Update All as usual.

The workflow refreshes the database every six hours and can also be run manually.
It takes the newest `.rbf` asset from the upstream GitHub latest release, and
downloads the upstream `roms/boot.rom` when building the database. It calculates
the MD5 hashes and byte sizes required by MiSTer Downloader.

## Install paths

- Core: `_Computer/Amstrad_YYYYMMDD.rbf`
- Boot ROM: `Games/Amstrad/boot.rom`

The core releases use date-stamped filenames. The database uses a Downloader
`tangle` group so that an older dated core is treated as the previous version
of the same core, rather than accumulating indefinitely.

Keep a backup of your SD card before first use. This is a community-maintained
custom database, not an official database maintained by MiSTer or the core author.

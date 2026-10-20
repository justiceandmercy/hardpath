# hardpath

`hardpath` scans source code for hardcoded absolute filesystem paths (e.g. `/Users/...`, `/home/...`, `C:\...`) that make projects non-portable.

## Features

- Detects Unix absolute paths under common roots (`/home`, `/Users`, `/root`, `/tmp`, `/var`, `/opt`, `/usr`, `/etc`, `/mnt`, `/Volumes`).
- Detects Windows drive-letter paths (`C:\...`).
- Detects quoted multi-segment absolute paths.
- Skips binary files and common build/dependency directories.
- Text and JSON output formats.
- Non-zero exit code on findings (for CI).

## Install

```sh
pip install .
```

Or run directly:

```sh
python hardpath.py .
```

## Usage

```sh
# Scan current directory
hardpath .

# Scan a specific path
hardpath src/

# JSON output
hardpath . --format json

# Fail in CI if any found
hardpath . --fail
```

Example output:

```
src/config.py:8: /Users/alice/project/data
lib/io.py:22: /tmp/scratchpad
```

## License

MIT

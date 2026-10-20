import os
import re
from pathlib import Path

PATTERNS = [
    re.compile(r'(?<![A-Za-z0-9_])/(?:home|Users|root|tmp|var|opt|usr|etc|mnt|Volumes)(?:/[A-Za-z0-9_.-]+)+'),
    re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:\\(?:[A-Za-z0-9_.-]+\\)+[A-Za-z0-9_.-]*'),
    re.compile(r'["\']/(?:[A-Za-z0-9_.-]+/){2,}[A-Za-z0-9_.-]*["\']'),
]

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.tox'}
SKIP_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.bin', '.exe', '.so', '.dylib', '.pyc', '.woff', '.woff2'}


def is_binary(path):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(8192)
        return b'\x00' in chunk
    except OSError:
        return True


def scan_file(path):
    findings = []
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f, 1):
                if 'http://' in line or 'https://' in line:
                    continue
                for pat in PATTERNS:
                    for m in pat.finditer(line):
                        val = m.group(0).strip('"\'')
                        findings.append((i, val))
    except OSError:
        return findings
    return findings


def scan(root):
    root = Path(root)
    if root.is_file():
        fnds = scan_file(root)
        return {str(root): fnds} if fnds else {}
    results = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in SKIP_EXTS:
                continue
            if is_binary(p):
                continue
            fnds = scan_file(p)
            if fnds:
                results[str(p)] = fnds
    return results

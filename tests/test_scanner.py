import os
import tempfile

from scanner import scan, scan_file


def test_detects_unix_home_path():
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write('DATA = "/home/alice/project/data"\n')
        name = f.name
    try:
        assert scan_file(name) == [(1, '/home/alice/project/data')]
    finally:
        os.unlink(name)


def test_detects_users_path():
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write('x = "/Users/bob/code"\n')
        name = f.name
    try:
        assert scan_file(name)
    finally:
        os.unlink(name)


def test_detects_windows_path():
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write('x = "C:\\Users\\bob\\code"\n')
        name = f.name
    try:
        assert scan_file(name)
    finally:
        os.unlink(name)


def test_ignores_relative_and_urls():
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write('u = "https://example.com/home/x"\n')
        f.write('p = "./relative/path"\n')
        name = f.name
    try:
        assert scan_file(name) == []
    finally:
        os.unlink(name)


def test_scan_directory_skips_git():
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, '.git'))
    with open(os.path.join(d, '.git', 'config'), 'w') as f:
        f.write('path = /home/x/y\n')
    with open(os.path.join(d, 'a.py'), 'w') as f:
        f.write('p = "/tmp/scratch"\n')
    try:
        res = scan(d)
        assert 'a.py' in ''.join(res.keys()) or any('a.py' in k for k in res)
        assert not any('.git' in k for k in res)
    finally:
        import shutil
        shutil.rmtree(d)

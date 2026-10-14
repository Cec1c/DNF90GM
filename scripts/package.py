"""Package only binaries, documentation and a placeholder config."""
import argparse
import hashlib
from pathlib import Path
import tarfile
import zipfile
from build import ROOT, build

def package(version):
    release = ROOT / 'dist' / version
    release.mkdir(parents=True, exist_ok=True)
    common = ['README.md', 'README.zh-CN.md', 'NOTICE.md', 'config/gm.example.json',
              'docs/DEPLOYMENT.md', 'docs/MIGRATION.md', 'docs/BENEFITS.md',
              'docs/COMPATIBILITY.md', 'docs/PROVENANCE.md']
    checksums = []
    for goos in ('windows', 'linux'):
        binary = build(goos, 'amd64')
        archive = release / ('DNF90GM-' + version + '-' + goos + '-amd64' + ('.zip' if goos == 'windows' else '.tar.gz'))
        files = [(binary, binary.name)] + [(ROOT/p, p) for p in common]
        if goos == 'windows':
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
                for path, name in files: z.write(path, name)
        else:
            with tarfile.open(archive, 'w:gz') as z:
                for path, name in files:
                    info = z.gettarinfo(str(path), name)
                    info.uid = info.gid = 0
                    info.uname = info.gname = ''
                    info.mode = 0o755 if path == binary else 0o644
                    with path.open('rb') as stream: z.addfile(info, stream)
        checksums.append(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name)
    (release/'SHA256SUMS').write_text('\n'.join(checksums)+'\n', encoding='utf-8')
    return release

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('version')
    args = parser.parse_args()
    import re
    if not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', args.version): parser.error('use vMAJOR.MINOR.PATCH')
    print(package(args.version))

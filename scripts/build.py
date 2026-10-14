"""Build this repository only; no server checkout, database, or deployment."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def build(goos, arch):
    out = ROOT / 'dist' / (goos + '-' + arch)
    out.mkdir(parents=True, exist_ok=True)
    binary = out / ('DNF90GM.exe' if goos == 'windows' else 'DNF90GM')
    env = os.environ | {'GOOS': goos, 'GOARCH': arch, 'CGO_ENABLED': '0'}
    subprocess.run(['go', 'build', '-tags', 'timetzdata', '-buildvcs=false',
                    '-mod=readonly', '-trimpath', '-ldflags=-s -w', '-o', str(binary),
                    './cmd/gmtool'], cwd=ROOT, env=env, check=True)
    return binary

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('goos', nargs='?', choices=['windows', 'linux'], default='windows' if os.name == 'nt' else 'linux')
    parser.add_argument('arch', nargs='?', choices=['amd64', 'arm64'], default='amd64')
    args = parser.parse_args()
    print(build(args.goos, args.arch))

"""Verify GM builds without a neighboring game checkout or game listeners."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
mod = (ROOT/'go.mod').read_text(encoding='utf-8')
assert 'replace ' not in mod, 'local module replacement is not allowed'
assert 'longheng.io/server' not in mod, 'game module dependency is not allowed'
assert not (ROOT/'go.work').exists(), 'build must not rely on a workspace'
output = subprocess.check_output(['go', 'list', '-buildvcs=false', '-mod=readonly',
                                  '-deps', '-f', '{{.ImportPath}}', './cmd/gmtool'], cwd=ROOT, text=True)
for path in output.splitlines():
    assert 'longheng.io/server' not in path
    assert '/dnfbridge' not in path and '/cmd/server/' not in path
print('PASS: standalone module, no game executable/bridge dependency')

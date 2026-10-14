# DNF90GM

This repository owns the independent GM process, Web UI, PVF item lookup, bulk
mail jobs, benefit rules, and MariaDB adapters. It does not run game listeners.
Read `docs/PROVENANCE.md`, `docs/COMPATIBILITY.md`, and `changlog.md` before changes.

- Keep binaries, credentials, PVF, player data, and local evidence in ignored
  `runtime/`, `dist/`, or `.cache/`. Do not commit real configuration.
- Preserve account/mail transactions and receipt keys. Never test by granting
  real player assets. Database integration tests require disposable databases.
- Do not add a relative dependency on a ServerS5A3 checkout or import its
  `internal` packages. Imported compatibility code is pinned in the manifest;
  review updates against the schema/API contract and retain provenance.
- Game API failures are not evidence that a character is offline.
- Existing campaign IDs, signup snapshots and receipts must survive migration.
- Windows entry points use BAT/Python; do not add PowerShell wrappers.
- Validate `go list -buildvcs=false ./...`, `go test -buildvcs=false -count=1 ./...`,
  `go vet ./...`, `python scripts/check_boundary.py`, and both release builds.
  Run `python scripts/test_mysql.py` for database-affecting changes (Docker).
  UI changes also require `python scripts/test_browser.py` (Playwright).
- Update the changelog and both README languages when behavior changes.

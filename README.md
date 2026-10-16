<div align="center">

# DNF90GM

![Go](https://img.shields.io/badge/Go-1.26.5-00ADD8?style=flat-square&logo=go&logoColor=white)
![Database](https://img.shields.io/badge/Database-MariaDB-003545?style=flat-square&logo=mariadb)
![Platforms](https://img.shields.io/badge/Platforms-Windows%20%7C%20Linux-2563EB?style=flat-square)

Manage ServerS5A3 90CN accounts, search PVF items, and send item-mail benefits from your browser. Each benefit rule keeps delivery receipts and skips characters it has already rewarded.

[简体中文](README.zh-CN.md) ｜ [Quick start](#quick-start) ｜ [Deployment](docs/DEPLOYMENT.md) ｜ [Migration](docs/MIGRATION.md)

</div>

> [!IMPORTANT]
> Before deployment, prepare a compatible ServerS5A3 MariaDB database, matching PVF, and credentials for private game API v1. Supported versions are listed in the [compatibility contract](docs/COMPATIBILITY.md).

## What it does

- Web login, account/character lookup, PVF item search and existing GM operations.
- Send an item by ID and quantity using transactional mail and persistent receipts.
- Preview and backfill existing characters, pause/resume benefit rules, and automatically deliver to eligible new characters.
- Reuse the same rule to skip previous recipients, including after restart or mail deletion.
- Query game-owned online state and activity settings through an authenticated private API.

**Each benefit rule sends one item in one mail.** Create separate rules for multiple items, and reuse the original rule to backfill the same grant. A new rule creates its own delivery history and starts a new grant. Read [benefit semantics](docs/BENEFITS.md).

## Quick start

Install Go 1.26.5 and Python 3.10+, then:

```sh
git clone https://github.com/Cec1c/DNF90GM.git
cd DNF90GM
python scripts/build.py windows amd64
```

For Linux use `python3 scripts/build.py linux amd64`. Copy `config/gm.example.json`
to `runtime/gm.json`, fill in the existing database mapping, PVF SHA256, private
game API secret and a unique management password. Make the state directory writable.

```text
dist/windows-amd64/DNF90GM.exe --config runtime/gm.json --check
dist/windows-amd64/DNF90GM.exe --config runtime/gm.json --init-schema
```

Open `http://127.0.0.1:18112/` on the GM host. Linux uses
`./dist/linux-amd64/DNF90GM`. `--check` validates config syntax only;
`--init-schema` initializes GM tables and starts the service. Creating/enabling
reward rules remains an explicit administrator action. Existing enabled rules resume scanning.

Windows also provides `BUILD.bat` and `START_GM.bat`. The [deployment guide](docs/DEPLOYMENT.md)
covers binaries, Linux Docker, private access and every config field.

## How GM and the game work together

GM owns its HTTP server, credentials, PVF index, jobs and scanner. The game owns
login, character creation, native gameplay and mail claiming. GM retains the
existing MariaDB asset transactions and calls the private API for runtime state.

The standalone Go module includes a pinned snapshot of the business and repository
compatibility code, so it can be built and deployed independently.
Launcher Hub and remembered token login are available through optional external integrations.
For an existing installation, follow [migration instructions](docs/MIGRATION.md)
to preserve campaign IDs, signup snapshots and all delivery receipts.

## Development

```sh
python scripts/check_boundary.py
go test -buildvcs=false -count=1 ./...
go vet ./...
python scripts/test_mysql.py
```

The last command creates a disposable MariaDB Docker container and removes it
after testing; test DSNs must point to test databases. For browser verification,
run `pip install playwright`, `python -m playwright install chromium`, then
`python scripts/test_browser.py` to exercise the UI with mocked requests.
Create both platform archives with `python scripts/package.py v0.1.0`.

## Sources

Extracted from [Cec1c/ServerS5A3](https://github.com/Cec1c/ServerS5A3), derived from
[16ww/servers5a3](https://gitgud.io/16ww/servers5a3). Source paths and hashes are in
[PROVENANCE.md](docs/PROVENANCE.md). Imported code retains its existing attribution
and licensing status, documented in [NOTICE.md](NOTICE.md).

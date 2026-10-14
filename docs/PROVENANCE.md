# Source provenance

Extracted from [Cec1c/ServerS5A3](https://github.com/Cec1c/ServerS5A3)
commit [`721927e6f6e36598d81126d50ac6fd7466710ccf`](https://github.com/Cec1c/ServerS5A3/commit/721927e6f6e36598d81126d50ac6fd7466710ccf),
derived from [16ww/servers5a3](https://gitgud.io/16ww/servers5a3).

`source-manifest.json` records source/target paths and SHA256 for the selected
GM production and test dependency closure. Go imports were renamed from
`longheng.io/server` to `github.com/Cec1c/DNF90GM`. `go mod tidy` removed dependencies
used only by the game. The two game source fixtures are text-only test inputs.
Test paths were adapted to those pinned fixtures; no game application or bridge
is linked into GM. The manifest records the extraction baseline, not a claim
that later changes retain those original hashes.

After extraction, inherited workstation paths in source comments were replaced
with relative project references. Initial hashes remain as historical provenance;
these comment edits do not change the executable or its data contract.

Shared repository/domain adapters are an explicitly pinned source snapshot,
not a second independently invented asset or wallet implementation. Keep their
transaction boundaries and document intentional changes in the changelog.

The separate-process/DB/PVF workflow was also researched against
[Liuxiny/86jp_DfoGmTool](https://github.com/Liuxiny/86jp_DfoGmTool),
snapshot `13a45286166643f9e0f7bfce81c9ac67134dd848`; its C# implementation and SQLite
schema were not copied into this project.

No PVF, player database, runtime credentials, launcher signing keys, or deployed
configuration is included. See [NOTICE](../NOTICE.md) for attribution.

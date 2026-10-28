---
title: ESDM installation, checksums and update check
summary: Download URLs and published SHA256 checksums for esdm 0.15.0 on all platforms, post-download steps, and the daily update check with its opt-out variable.
tags: [esdm, installation, checksums, supply-chain, tooling]
status: draft
sources: [https://www.esdm.io/getting-started/installing-esdm/, https://www.esdm.io/getting-started/updating-esdm/]
updated: 2026-10-28
---

# ESDM installation, checksums and update check

Pre-built, **unsigned** single binaries. URL pattern:
`https://esdm.s3.fr-par.scw.cloud/<version>/esdm-<os>-<arch>[.exe]`.

## esdm 0.15.0 — published SHA256 (install page, 2026-10-28)

| OS / arch | File | Size | SHA256 |
|---|---|---|---|
| linux/amd64 | `esdm-linux-amd64` | 9.6 MB | `db76e45729e5318023120143356df461dbddfbedf2108111c0d8b7b595f42a84` |
| linux/arm64 | `esdm-linux-arm64` | 8.8 MB | `5076335000631e8701cf07fc610dcc86c806c7422fd86ad68eea27b212820019` |
| darwin/arm64 | `esdm-darwin-arm64` | 9.1 MB | `ea11a2629447b54a8475b67d30d01215b74fc61fe563c4715119c73d6f823f88` |
| darwin/amd64 | `esdm-darwin-amd64` | 9.8 MB | `b4e0009243fb5ed822fbade6e8f469395227feba95269b1e59afbe33fad14705` |
| windows/arm64 | `esdm-windows-arm64.exe` | 9.0 MB | `8cdd0a01f740e4d1833f839ad96865bf202b748c18550659b873ff77a03b39ca` |
| windows/amd64 | `esdm-windows-amd64.exe` | 9.9 MB | `0f82f30bbe73f0c68ec6633851599f3a1cf2c1f1e663cb6815b7b13f6abda5e7` |

Verified on 2026-10-28: the downloaded `esdm-linux-amd64` hashed to exactly the
published value. `esdm version` prints:

```
esdm: v0.15.0
Revision: 5cbe12a9b682c72d0cb5ad2f79d63207705b6bde
```

## Post-download steps

- Rename to `esdm` (`esdm.exe` on Windows), `chmod a+x esdm`.
- macOS: `xattr -d com.apple.quarantine esdm`. Windows: `Unblock-File .\esdm.exe`.
- Verify with `./esdm version`.

## Updating

No self-updater. An update = same procedure as install with a new version, then
`esdm update-schema` in the model directory (see
[project-layout-and-files.md](project-layout-and-files.md)).

## Update check (network!)

Since 0.10.0, any command in an **interactive terminal** does at most one HTTP GET per
day to `https://www.esdm.io/version.json` (`{"version": "0.15.0"}`) and prints a hint if
outdated. Suppressed when stdout/stderr is not a TTY, when `CI` is set, or for dev
builds. Disable entirely:

```sh
export ESDM_DISABLE_UPDATE_CHECK=true
```

## Relevance for the LIMS (own conclusion)

The `limtool esdm` wrapper should pin version + per-platform SHA256 from the table
above, verify before `chmod`, install to `.tools/bin/`, and set
`ESDM_DISABLE_UPDATE_CHECK=true` in the child environment so runs are reproducible
and offline. The checksums come from the HTML page only (no separate checksum file was
found), so they must be copied into the wrapper by hand on every upgrade.

---
title: Upstream upgrade log
summary: Chronological record of every pinned-version upgrade of architecturekit, EventSourcingDB and ESDM, with what broke and which feedback ids it touched.
tags: [upstream-feedback, dependencies, versioning]
status: current
updated: 2026-10-28
---

# Upstream upgrade log

Policy: [ADR-0008](../adr/0008-exact-version-pins-with-deliberate-upgrades.md). Newest first.
Check for updates: `uv run --project tools limtool deps outdated`.

| Date | Tool | From → To | What broke / changed | Feedback ids |
|---|---|---|---|---|
| 2026-10-28 | all | — → architecturekit 0.21.0, eventsourcingdb crate 4.0.4, ESDB image 1.2.0, esdm 0.15.0 | initial pins | — |

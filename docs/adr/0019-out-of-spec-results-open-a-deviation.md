---
title: "ADR-0019: Out-of-spec results open a deviation"
summary: Evaluation against the pinned specification is automatic; an off result opens a lightweight deviation aggregate resolved by retest, resample, concession or rejection before any disposition or report is issued.
tags: [adr, domain, deviation, oos, disposition, e-signature]
status: accepted
updated: 2026-10-28
---

# ADR-0019: Out-of-spec results open a deviation

## Context

Margarine: rejection needs the head of analytics' counter-signature and separate archiving.
OH number: "action taken if off" (chat 2026-10-28). Both are the same mechanism.

## Decision

Three separate facts:

1. **Evaluation** — automatic, deterministic against the
   [pinned specification](0018-specification-pinned-at-order-creation-with-binding-and-agreed-limits.md):
   result, limit, limit source, verdict.
2. **Deviation** — an off verdict automatically opens a deviation (core aggregate), resolved
   by exactly one of: **retest** (same sample), **resample**, **concession** (accept with
   justification), **confirmed rejection**.
3. **Disposition / report** — issued only after the deviation is closed. Required signatures
   (e.g. counter-signature) and retention class come from the regulatory profile
   ([ADR-0003](0003-compliance-baseline-and-regulatory-profiles.md)), not code.

- A retest **never replaces** the original result; the reported result references the
  deviation that justifies it.
- The profile may allow an immediate **provisional hold** event (e.g. to the gate) while a
  deviation is open.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Evaluation → deviation → disposition (this) | One mechanism for both scenarios; no "testing into compliance" | Human decision on every off result |
| Off verdict is final | Fast | No retest/concession path; GxP OOS practice impossible |
| Full CAPA module in core | Complete | Scope explosion — [backlog #2](../discussions/po-decision-backlog.md) |

## Consequences

- No off result reaches a requester, ERP or gate without a human decision.
- The deviation must be linkable from an external CAPA system; full CAPA stays out for now.
- Time-critical cases (truck at the gate) depend on the provisional hold.

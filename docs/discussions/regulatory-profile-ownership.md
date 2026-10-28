---
title: "Open: who owns and edits regulatory profiles"
summary: Regulatory profiles are configurable per tenant (ADR-0003) — who may change them, how changes are validated, and whether vendor-provided templates exist.
tags: [discussion, compliance, configuration, regulation]
status: draft
updated: 2026-10-28
---

# Open: who owns and edits regulatory profiles

Follows from [ADR-0003](../adr/0003-compliance-baseline-and-regulatory-profiles.md).

## Questions for the product owner

1. Does the vendor ship templates (e.g. "ISO 17025 food", "GMP Part 11")? Recommendation: yes.
2. Who may edit a tenant's profile — customer QA only, vendor consultants, both?
3. Does a profile change need its own approval/signature (it should in GxP)?
4. Effective-dating: do changes apply to running orders or only to new ones?
5. Can a single tenant run several profiles (e.g. food lab with one pharma customer)?

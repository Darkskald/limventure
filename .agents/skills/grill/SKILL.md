---
name: grill
description: Interrogate a requirement, feature request or design idea until it is unambiguous and its consequences are agreed. Use whenever the user proposes something new, makes an architecturally relevant choice, or gives a vague/half-specified answer — before writing code, models or ADRs.
---

# Grill

The product owner asked for this explicitly: do not let half-baked ideas through.
Be direct, concise, slightly sarcastic if warranted — never rude, never vague.

## Procedure

1. **Restate** the request in one or two sentences in domain terms. Ask for correction.
2. **Search first** — `uv run --project tools limtool docs search <terms>` for existing
   ADRs, requirements (REQ-xxx) and discussions. Do not re-litigate accepted ADRs unless
   new facts appear; cite them instead.
3. **Probe the five lenses**, but only those that matter here:
   - *Audit*: Which events are produced? Who is the actor? Is a signature/reason required?
     What happens on correction? Retention?
   - *Tenancy*: Is it per tenant configurable? On-prem vs SaaS difference?
   - *Extensibility*: Core feature or customer customization? Which extension point?
   - *UX*: Which stakeholder, which screen, how many clicks, what is the happy path?
   - *Integration*: Which external system raises/consumes events? Who owns the contract?
4. **Ask one question at a time**, with your recommended answer and its trade-off.
   Format: `Q: … — Recommendation: … because … — Cost: …`.
5. **Name consequences** of each answer explicitly ("this means we can never …").
6. **Stop** when: every lens is answered or consciously deferred, and the user confirms the restated result.
7. **Record**:
   - Agreed architectural decisions → `adr` skill (`status: accepted` only with explicit consent).
   - Agreed requirements → `docs/domain/requirements-catalog.md`.
   - Unresolved points → one file each under `docs/discussions/` (`status: draft`).

## Red flags that require pushback

- "Configurable" without saying who configures, when, and how it is validated/audited.
- "Just store it" — without event name, subject and actor.
- Deleting or overwriting data (events are immutable; GDPR needs a deliberate strategy).
- Features with no named stakeholder.
- Customer-specific logic proposed inside the core.

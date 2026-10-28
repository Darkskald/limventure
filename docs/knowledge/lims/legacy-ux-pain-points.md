---
title: "Known UX pain points of legacy LIMS"
summary: "Survey and review evidence on why lab users dislike legacy LIMS — hard to use, poorly integrated, inflexible, slow, costly to change — and design responses."
tags: [lims, ux, usability, pain-points, adoption]
status: draft
sources:
  - https://astrixinc.com/wp-content/uploads/2019/04/LIMS-Survey-Summary-Report-Final.pdf
  - https://astrixinc.com/wp-content/uploads/2020/06/061820-2019-LIMS-Market-Survey-Report1.pdf
  - https://www.limswiki.org/index.php/LII:Laboratory_Informatics_Buyer%27s_Guide_for_Medical_Diagnostics_and_Research/Closing_remarks
  - https://www.sapiosciences.com/blog/6-of-the-worst-lims-reviews-on-g2/
  - https://clarkstonconsulting.com/wp-content/uploads/2025/03/Supporting-a-Clinical-LIMS-Enhancement-for-a-Global-Biopharmaceutical-Company.pdf
  - https://www.lablynx.com/resources/articles/addressing-the-discontent-among-lab-managers-with-their-current-lims-solutions/
  - https://www.shotuk.org/resources/script-surveys/
updated: 2026-10-28
---

# Known UX pain points of legacy LIMS

## Evidence

| Source | Finding |
|---|---|
| Astrix LIMS survey 2019 (≈100 respondents, 79 % with LIMS) | Nearly half: LIMS had neutral effect or **decreased** efficiency; only 27 % highly satisfied; 18 % "cumbersome"; only half say LIMS strongly promotes data integrity; root cause often missing strategic planning |
| Astrix 2019 (deployed LIMS subset) | 25 % report poor user adoption / lack of ease of use as significant challenge; integration only "moderate" |
| Astrix market report (survey early 2020) | Top challenges: disconnected systems 36 %, training 34 %, ease of use 32 %, outdated system 32 %, user adoption 24 % |
| Astrix 2016 via LIMSwiki buyer's guide | LIMS perceived as difficult to use and lacking integration; dissatisfaction main reason to replace |
| G2 review analysis (vendor blog, Sapio) | Complaints cluster: inflexible/complicated, poor performance, lack of integration, support |
| Clarkston biopharma case | Users reported performance problems and difficulty of use; 18-question survey to find root causes |
| SHOT SCRIPT surveys (UK transfusion) | Several deficiencies in current LIMS reported by professionals |

Caveat: much commentary comes from vendors with products to sell; Astrix is a
consultancy. Treat percentages as indicative.

## Recurring pain points (synthesis of the above)

1. **Click-heavy, form-centric UI** mirroring database tables instead of tasks.
2. **Transcription** from instruments/paper → errors, second-person checks, slowness.
3. **Inflexibility**: changing a workflow requires vendor consultants or scripting in
   a proprietary language; customisations break on upgrade ("upgrade lock-in").
4. **Integration gaps** with ERP, instruments, ELN → re-keying, spreadsheets on the side.
5. **Performance**: slow screens, long-running reports, batch jobs.
6. **Training burden** and poor discoverability; jargon-heavy screens.
7. **Compliance friction**: re-authentication pop-ups and reason dialogs everywhere,
   even where risk does not justify them.
8. **Reporting**: rigid report designers; data hard to extract for analysis.
9. **Outdated technology**: thick clients, browser plugins, no mobile/tablet.

## Own conclusions (design responses, not from sources)

| Pain | Response |
|---|---|
| 1, 6 | Task inbox ("my work"), progressive disclosure, scan-to-act, role-specific home |
| 2 | Instrument edge agent; file-drop parsing; never re-key what a machine produced |
| 3 | Declarative configuration + versioned tenant packages surviving upgrades; extension points with stable contracts |
| 4 | Event-driven adapters, published API/webhooks, SAP QM adapter as first-class |
| 5 | CQRS read models tuned per screen; no heavy reporting on the write path |
| 7 | **Risk-based friction**: signature/reason prompts driven by the regulatory profile and data criticality, batch signing within session |
| 8 | Analytical export/projection; template-based reports with preview |
| 9 | Web-first, responsive, keyboard and touch, WCAG 2.2 AA |

Usability testing with real analysts (not just managers who buy) should be part of
the product process; legacy LIMS selection is often done by managers/IT.

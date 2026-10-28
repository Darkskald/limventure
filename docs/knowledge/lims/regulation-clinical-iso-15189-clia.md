---
title: "Regulation: clinical labs (ISO 15189:2022, CLIA 42 CFR 493)"
summary: "Clinical-lab regimes as an optional profile: ISO 15189:2022 data/information control, CLIA test report content, corrected reports, patient data and interoperability (HL7/FHIR)."
tags: [lims, regulation, clinical, iso-15189, clia, hl7, gdpr]
status: draft
sources:
  - https://www.iso.org/standard/76677.html
  - https://www.sas.admin.ch/dam/sas/de/dokumente/Wie%20wird%20meine%20Stelle%20akkreditiert/Gesetzliche%20Grundlagen/ea15189_kap7.pdf.download.pdf/EA%20LC%20TTT%20ISO%2015189%20-%20Chapter%207.pdf
  - https://www.law.cornell.edu/cfr/text/42/493.1291
  - https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/CMS/Survey-and-Cert-Letter-14-11.pdf
  - https://hl7.org/fhir/R4/diagnosticreport.html
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj
updated: 2026-10-28
---

# Regulation: clinical labs (ISO 15189, CLIA)

Clinical diagnostics is "possibly" in scope. It changes the domain substantially:
patient identity, orders from clinicians, health data protection. Many vendors
separate LIS (clinical) from LIMS (QC/research) for this reason.

## ISO 15189:2022

- Medical laboratories — requirements for quality and competence; 2022 edition
  restructured to align with ISO/IEC 17025:2017 and integrated point-of-care testing.
- Clause 7.6 "Control of data and information management"; European accreditation
  training material (EA LC) notes no major changes vs. the 2012 edition requirements.
- Pre-examination, examination and post-examination processes (7.2–7.4) map to
  order entry/specimen handling, testing, and result reporting/release.

## CLIA — 42 CFR 493.1291 (test report)

- (c) report must show positive patient identification, lab name/address, report date,
  test performed, specimen source when appropriate, result with units or
  interpretation, and condition/disposition of specimens not meeting acceptability.
- (d) reference intervals available to authorized persons.
- (f)/(l) release to authorized persons; patients may receive completed reports
  directly (CMS S&C letter 14-11, 2014).
- (k) corrected reports: notify promptly, issue corrected report, **retain both
  original and corrected** report.
- Frequent CMS survey citations concern missing report elements and reference ranges.

## Interoperability

- HL7 v2 (ORM/ORU) and HL7 FHIR (`ServiceRequest`, `Specimen`, `Observation`,
  `DiagnosticReport`) are the clinical integration lingua franca; LOINC for test codes.
- LIMSpec §22 "Clinical and public health data management", §25 "Health information
  technology".

## Privacy

Patient data are special-category personal data (GDPR Art. 9); erasure and access
rights interact with retention duties (GDPR Art. 17(3)(b),(c) exemptions for legal
obligations and public health). See [event-sourcing-fit.md](event-sourcing-fit.md).

## Own conclusions (not from sources)

- Treat clinical as a separate **profile plus module set** (patient, order, specimen,
  reference ranges, critical-value call-backs), not as configuration of the QC core.
- Personal data must never be embedded in immutable events in clear text if a
  clinical profile is ever enabled — this constrains the core event design from day
  one even if clinical ships late.
- Recommend the PO explicitly decide whether clinical is in scope for the first
  three years; it raises regulatory surface (IVDR questions in the EU, CLIA in the US).

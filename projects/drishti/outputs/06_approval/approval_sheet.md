# Approval sheet - An Indian cement manufacturer sees its real safety number - and changes it

**For:** Ritu Saxena, Corporate Communications | **Copy:** Pooja Menon, Corporate Legal; Meenakshi Iyer, Head EHS; Rajiv Bhandari, Unit Head | **Reply by:** 2026-11-18 | **Our reference:** CS-2026-001 (anonymised case study, cement safety analytics)

## 1. Your choice (tick one)

|  | Option | What it means | What we publish |
| --- | --- | --- | --- |
| ☐ | Anonymised | Described only as 'an Indian cement manufacturer'. Nothing below country level; no capacity, plant count or headcount; no images of premises, people, vehicles or signage (clause 15.2) | The attached text and media, exactly as approved, on PredCo's website, LinkedIn and sales deck |
| ☐ | Named, later | Your company named, only when your leadership wishes and after a fresh review of an updated pack (clause 15.1) | Nothing now; a new pack will be sent for approval |
| ☐ | Internal use only | Used only inside PredCo for training and delivery lessons; never shown to anyone outside PredCo | Nothing outside PredCo |
| ☐ | No | We do not use it in any form | Nothing |

You can withdraw any approval later by written notice; we stop new use within 30 days (clause 15.4).

## 2. Exactly what would be used

- Text: `04_case_study.md` (attached in full, four short versions).
- Media: `05_media/chart_compliance_cohorts.png` - Chart drawn from recomputed project data (not a screenshot)
- Media: `05_media/chart_gate_turnaround.png` - Chart drawn from project data; causes labelled
- Media: `05_media/architecture_generic.png` - Illustration: generic redrawn architecture, no addresses or names
- Media: `05_media/case_study_slide.pptx` - One slide for the sales deck (draft)
- Media: `05_media/gate_payback_calculator.html` - Interactive calculator; reader enters their own numbers
- Nothing else: no logo, no photo of premises, people or vehicles, no screenshot of your systems.

## 3. Every number and where it comes from

| Claim | Value | Your record | How it was worked out |
| --- | --- | --- | --- |
| CR-03: gate truck-turnaround analytics added, with KPI K5 (-15% turnaround by end September vs the manual register) | "KPI K5 added: average in-to-out truck turnaround; baseline = manual gate register Jun–Jul 2026; target −15% by end Sep." | `03_commercial/change_requests_CR01-CR03.md:26` | quoted from the record |
| All cameras live | "stores ST-01..ST-10 live; 146/146 cameras" | `08_github/git_log.txt:6` | quoted from the record |
| Retention: video 30 days, alert snapshots 180 days; no facial recognition | "Video retained for 30 days; alert snapshots for 180 days; no facial recognition or biometric processing" | `01_contract/MSA_confidentiality_and_publicity_extract.md:43` | quoted from the record |
| Vendor certifications | "Deployment on premise, hybrid or cloud. SOC 2 and ISO 27001." | `12_vendor/vendor_profile_team_achievements.md:7` | quoted from the record |
| SOC 2 covers company controls; on-prem adds a deployment checklist mapped to ISO 27001 Annex A | "For on-prem we add a deployment checklist mapped to ISO 27001 Annex A controls." | `06_email/B_2026-02-17_to_03-02_security_review.md:35` | quoted from the record |
| Legal decides not to proceed with face recognition in 2026 and asks for proof of removal | "Decision: we will not proceed with face recognition in 2026." | `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:40` | quoted from the record |
| CR-02: face-recognition attendance removed from scope with a credit | "CR-02 — Remove face-recognition attendance (R8)" | `03_commercial/change_requests_CR01-CR03.md:12` | quoted from the record |
| Incident: about 41 hours with no usable video on 22 of the 40 pilot cameras after an NVR firmware update | "(about 41 hours), 22 of the 40 pilot cameras" | `04_delivery/incident_report_INC-0611.md:9` | quoted from the record |
| Fixes: no-frames alarm after 5 minutes, 24-hour notice before NVR firmware changes, daily 08:00 camera health message | "Stream health monitor (release v1.4): alarms when a camera delivers no frames for 5 minutes" | `04_delivery/incident_report_INC-0611.md:27` | quoted from the record |
| Change control: contractor gives 24 hours notice before firmware changes | "the CCTV contractor informs PredCo 24 hours before any NVR firmware change" | `04_delivery/incident_report_INC-0611.md:28` | quoted from the record |
| Detector retrained on 4,200 labelled site frames on an on-premise training box | "Retrained detector on 4,200 labelled site frames (on-premise training box)." | `08_github/CHANGELOG.md:16` | quoted from the record |
| Field engineer on site 61 days | "on site 61 days" | `12_vendor/vendor_profile_team_achievements.md:17` | quoted from the record |
| Effort about 1,150 person-hours Feb-Sep | "Effort: about 1,150 person-hours, Feb to Sep 2026 (timesheets)." | `12_vendor/vendor_profile_team_achievements.md:20` | quoted from the record |
| KPI K1 definition and target | "\| K1 \| PPE compliance \| Persons observed wearing both helmet and vest ÷ persons observed, on pilot cameras \| Camera-measured, pilot weeks 1–2 \| ≥ 90% \| Average of last 4 pilot weeks \|" | `02_scoping/2026-03-05_BRD_v2_signed.md:45` | quoted from the record |
| Manual safety-walk compliance, Q4 2025 | 73.8% | `07_data/baseline_manual_safety_walks_2025Q4.csv` | sum(fully_compliant) = 651; sum(people_observed) = 882; 100 x 651 / 882 = 73.8095 |
| K1 PPE compliance, pilot weeks 1-2 | 68.9% | `07_data/viewos_weekly_zone_metrics.csv` | sum(ppe_compliant) = 9,978; sum(persons_observed) = 14,486; 100 x 9,978 / 14,486 = 68.8803 |
| PoC false alarms were 23% (sack-pallet strips read as vests, dust hiding helmets) | "False alarms in the PoC were 23%." | `05_meetings/2026-04-17_poc_review_transcript.txt:19` | quoted from the record |
| False alarms, pilot weeks 1-2 (EHS sample, scaled) | 19.8% | `07_data/viewos_weekly_zone_metrics.csv` | sum(alerts_false_verified) = 113; sum(alerts_raised) = 571; 100 x 113 / 571 = 19.7898 |
| K4 false alarms, last 2 pilot weeks | 9.7% | `07_data/viewos_weekly_zone_metrics.csv` | sum(alerts_false_verified) = 15; sum(alerts_raised) = 155; 100 x 15 / 155 = 9.6774 |
| Acceptance condition for K3: control room phones the in-charge if an alert is not acknowledged in 5 minutes | "Control room to phone the area in-charge if an alert is not acknowledged in 5 minutes (from 1 Aug)." | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:21` | quoted from the record |
| K3 acknowledgement minutes, pilot weeks 1-2 (alert-weighted) | 8.6 min | `07_data/viewos_weekly_zone_metrics.csv` | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 4,929.3 / 571 = 8.6327 |
| Acknowledgement minutes, pilot cameras, last 4 weeks (after phone rule) | 2.1 min | `07_data/viewos_weekly_zone_metrics.csv` | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 453.9 / 218 = 2.0821 |
| Physical tail-pulley guards go in; vendor 2 m pre-zone warning deployed | "after the tail-pulley guards went in on 12 August" | `05_meetings/2026-09-18_QBR_transcript.txt:16` | quoted from the record |
| Breaches change vs pilot baseline, after guards | -77.3% | `evidence ledger` | r = K2_post = 1.265; b = K2_base = 5.58 -> 100 * (r - b) / b = -77.33 |
| Supervisor survey respondents | 18 | `07_data/supervisor_survey_sep2026.csv` | rows matching filter = 18 |
| Would recommend to another unit: Yes | 15 | `07_data/supervisor_survey_sep2026.csv` | rows matching filter = 15 |
| K1 PPE compliance, last 4 pilot weeks | 91.1% | `07_data/viewos_weekly_zone_metrics.csv` | sum(ppe_compliant) = 26,081; sum(persons_observed) = 28,634; 100 x 26,081 / 28,634 = 91.0840 |
| K1 result reported in the certificate | "\| K1 PPE compliance \| 68.9% \| 91.1% (last 4 weeks) \| ≥ 90% \| Met \|" | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:11` | quoted from the record |
| PPE compliance, pilot cameras, last 4 weeks (31 Aug-27 Sep) | 94.4% | `07_data/viewos_weekly_zone_metrics.csv` | sum(ppe_compliant) = 28,611; sum(persons_observed) = 30,302; 100 x 28,611 / 30,302 = 94.4195 |
| PPE compliance, cameras added after the pilot, last 4 weeks | 87.2% | `07_data/viewos_weekly_zone_metrics.csv` | sum(ppe_compliant) = 70,221; sum(persons_observed) = 80,528; 100 x 70,221 / 80,528 = 87.2007 |
| Turnaround change, camera data only (first 2 weeks vs dispatch-slot period) | -24.1% | `evidence ledger` | s = gate_anpr_slots = 67.24; f = gate_anpr_first = 88.54 -> 100 * (s - f) / f = -24.06 |
| Minutes removed after dispatch slots began | 15.5 min | `evidence ledger` | w = gate_anpr_wb = 82.79; s = gate_anpr_slots = 67.24 -> w - s = 15.54 |
| Minutes removed in the week after the client's gate-infrastructure upgrade | 5.8 min | `evidence ledger` | f = gate_anpr_first = 88.54; w = gate_anpr_wb = 82.79 -> f - w = 5.754 |
| Detention change, September vs Jun-Jul average | -67.8% | `evidence ledger` | s = det_sep = 3.9; b = det_junjul = 12.1 -> 100 * (s - b) / b = -67.77 |
| Pilot accepted with conditions: K1 and K4 met, K2 and K3 missed | "Decision: accepted with conditions under BRD §5." | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:16` | quoted from the record |
| Signed BRD v2 lowers all four targets and replaces the walk baseline with the camera-measured first two pilot weeks | "PPE target 95% → 90%; restricted zone −70% → −50%; response time 2 → 3 min; false alarms 5% → 10%" | `02_scoping/2026-03-05_BRD_v2_signed.md:14` | quoted from the record |
| Proof of concept goes live on 12 cameras (helmet, vest, tail-pulley zone) | "PoC: 12 cameras, helmet, vest, tail-pulley zone." | `08_github/CHANGELOG.md:30` | quoted from the record |
| Pilot live on 40 cameras with alerts to the control room and text-only messages | "Pilot: 40 cameras, two edge servers, alerts to control room and WhatsApp (text only)." | `08_github/CHANGELOG.md:27` | quoted from the record |
| Release v2.0: plant-wide camera configs, third edge server, gate turnaround analytics live | "Plant-wide: 146 camera configs; third edge server; load balancing across servers." | `08_github/CHANGELOG.md:6` | quoted from the record |

## 4. What we changed, and why

| Change | Why | Rule |
| --- | --- | --- |
| Company described only as 'an Indian cement manufacturer' | No name, logo or rank | MSA 15.1, 15.2(a) |
| No plant, state, region or city; no other units | Location below country level | MSA 15.2(b) |
| No capacity, number of plants, headcount or exact camera count | Each narrows to one plant | MSA 15.2(c); 14.1 |
| No site photo, screenshot or drawing; three new charts/diagram redrawn with metadata removed | The originals show your signboard, logo, people, IP addresses and GPS location in the file | MSA 15.2(d); 14.3 |
| The second weighbridge is described only as 'a separate client investment in gate infrastructure' | Your 12 Aug press release would identify the plant | Combination risk |
| No quotes from the public LinkedIn post; quotes attributed to roles only | The post names the company and project | Combination risk; 14.1 |
| No project name, internal programme names, system names, supplier names or audit rating letters | Internal and identifying | MSA 14.1 |
| No injury counts, no 'zero accidents', no avoided-injury savings, no benchmark savings | Your EHS and finance teams said these cannot be defended | Accuracy; 14.1 (safety records) |
| Missed pilot targets shown as missed (zones −46% vs −50%; acknowledgement 4.9 vs 3.0 min) and how they were fixed | Your BRD definitions only | Accuracy |
| Calendar dates replaced by weeks/months relative to go-live | Dates can be matched to public posts | Combination risk |

The engine also refused 0 draft line(s) that could not be traced to a record or broke a rule (log available on request).

## 5. What we deliberately do not claim

| Not claimed | Why |
| --- | --- |
| Compliance 'from 74% to 97%' (or 96.6%) | Mixes the announced walk score with the best packing week |
| Zero LTIs / zero accidents as a result | Seven months proves nothing; client refused it |
| Avoided or prevented injuries, or their money value | Finance: do not claim avoided LTIs as savings |
| Benchmark savings (Rs 2 Cr, Rs 2.3 Cr) | Finance rejected benchmark returns |
| 'Cement major' / 'leading' / market rank | With the numbers, anyone in the industry knows who it is |
| Restricted-zone entries 'halved' during the pilot | It was −46% against −50% at pilot end |
| Insurance premium reduced | Possible, not realised |
| The whole gate improvement as the vendor's | Client gate investment and logistics slots contributed; finance credits 'a share' |
| SOC 2 covers the on-premises deployment | IT-OT pointed out the SOC 2 report covers company controls, not the on-prem deployment |

## 6. Sign-off

| Role | Name | Decision | Date | Signature |
| --- | --- | --- | --- | --- |
| Corporate Communications (authorised signatory) |  |  |  |  |
| Corporate Legal (in copy; confirms) |  |  |  |  |
| Head EHS (fact check, optional) |  |  |  |  |

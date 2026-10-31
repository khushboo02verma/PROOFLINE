# Project story spine - Drishti (AI safety cameras + gate analytics, Jan-Sep 2026)

Built only from evidence items whose quote was found verbatim in the library. ★ marks a turning point. Names here are internal; the exposure report says what may leave the building.

## Phases

| Phase | From | To | What it was |
| --- | --- | --- | --- |
| First contact and scoping | 2026-01-28 | 2026-03-05 | Inbound email, discovery call, RFQ, security review, proposal, signed BRD v2 with lowered targets |
| Proof of concept | 2026-03-09 | 2026-04-17 | 12 cameras; sponsor change; 23% false alarms nearly stop the project |
| Pilot | 2026-05-04 | 2026-07-06 | 40 cameras incl. kiln; face recognition removed; 41-hour outage; retrain; accepted with conditions |
| Plant-wide and gate | 2026-07-02 | 2026-09-30 | All cameras plus gate analytics; client guards, phone rule and dispatch slots; QBR; case-study request |

## 2026-01

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-01-28 | Asked for | Inbound email after a vendor LinkedIn post: ~146 security cameras, serious incidents last year, manual audits not giving the true picture; cannot replace cameras | Arvind Rao (Head EHS) | `06_email/A_2026-01-28_inbound_and_first_reply.md:11` | e01 |

## 2026-02

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-02-06 | Happened | Discovery call: four lost-time injuries in 2025, safety walks around seventy-something percent vs a corporate target of 90 | Arvind Rao | `02_scoping/2026-02-06_discovery_call_transcript.txt:10` | e02 |
| 2026-02-06 | Quote | ★ Vendor warns up front that the camera number will look worse than the walk score | Neha Sharma (PredCo) | `02_scoping/2026-02-06_discovery_call_transcript.txt:24` | e03 |
| 2026-02-06 | Decided | IT-OT sets the hard rule: nothing to cloud, no internet from the OT network, no footage leaves the plant | Farhan Siddiqui (Head IT & OT Security) | `02_scoping/2026-02-06_discovery_call_transcript.txt:56` | e04 |
| 2026-02-06 | Asked for | Sponsor asks for face-recognition attendance; vendor advises parking it for privacy-law reasons | Rajiv Bhandari | `02_scoping/2026-02-06_discovery_call_transcript.txt:42` | e06 |
| 2026-02-06 | Asked for | Sponsor raises truck queues and detention charges at the gate; parked as a later phase | Rajiv Bhandari | `02_scoping/2026-02-06_discovery_call_transcript.txt:46` | e07 |
| 2026-02-14 | Happened | RFQ issued: helmet, vest, restricted zones, real-time alerts, reports, existing cameras, on-premises only; face recognition and harness optional | Lokesh Jain (Procurement) | `02_scoping/2026-02-14_RFQ_ACWL-BHD-EHS-2026-07.md:11` | e08 |
| 2026-02-15 | Problem | February 2026 burn injury at a hot zone without a face shield (motivated CR-01) | EHS register | `07_data/ehs_register_monthly_2025_2026.csv:15` | e96 |
| 2026-02-17 | Problem | Security review raises three blockers: model updates pulled from vendor registry, VPN support, snapshot images on WhatsApp | Farhan Siddiqui | `06_email/B_2026-02-17_to_03-02_security_review.md:11` | e09 |
| 2026-02-17 | Problem | Gatekeeper challenges whether the SOC 2 report covers on-premises deployment | Farhan Siddiqui | `06_email/B_2026-02-17_to_03-02_security_review.md:17` | e09b |
| 2026-02-19 | Changed | Vendor redesigns: updates as signed packages via jump host, jump-host-only access, alerts carry text only and the image stays on the plant console | Neha Sharma | `06_email/B_2026-02-17_to_03-02_security_review.md:33` | e10 |
| 2026-02-24 | Happened | Proposal v1 promises 95% PPE compliance, -70% zone entries, <2 min response, <5% false alarms | PredCo | `02_scoping/2026-02-24_PredCo_proposal_v1.md:37` | e12 |

## 2026-03

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-03-02 | Decided | IT-OT approves text-only alerts and clears the proof of concept | Farhan Siddiqui | `06_email/B_2026-02-17_to_03-02_security_review.md:45` | e11 |
| 2026-03-02 | Happened | Security pack took 3 review rounds; jump-host design changed | PredCo / client IT-OT | `04_delivery/project_tracker.csv:3` | t02 |
| 2026-03-05 | Changed | ★ Signed BRD v2 lowers all four targets and replaces the walk baseline with the camera-measured first two pilot weeks | Client EHS + PredCo (BRD v2 signatories) | `02_scoping/2026-03-05_BRD_v2_signed.md:14` | e13 |
| 2026-03-09 | Happened | Proof-of-concept purchase order issued (12 cameras, 6 weeks) | Arvind Rao (within delegation) | `03_commercial/purchase_orders.md:12` | e15 |
| 2026-03-19 | Happened | Proof of concept goes live on 12 cameras (helmet, vest, tail-pulley zone) | PredCo | `08_github/CHANGELOG.md:30` | e16 |
| 2026-03-31 | Happened | ★ The client's original champion (Head EHS) leaves the company mid-project | Arvind Rao | `06_email/C_2026-03-31_EHS_handover.md:11` | e17 |

## 2026-04

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-04-07 | Happened | A new Head EHS takes over and asks for every false alarm and the counting rules before the review | Client | `06_email/C_2026-03-31_EHS_handover.md:31` | e19 |
| 2026-04-17 | Happened | PoC review: compliance on camera 61% in the first two weeks, 78% in week five; tail-pulley entries 47 to 19 | Neha Sharma | `05_meetings/2026-04-17_poc_review_transcript.txt:11` | e20 |
| 2026-04-17 | Problem | ★ PoC false alarms were 23% (sack-pallet strips read as vests, dust hiding helmets) | Karthik Raman (PredCo) | `05_meetings/2026-04-17_poc_review_transcript.txt:19` | e21 |
| 2026-04-17 | Decided | Condition set: under 10% false alarms every week, checked by EHS's own sample; alerts go to the area in-charge | Meenakshi Iyer | `05_meetings/2026-04-17_poc_review_transcript.txt:25` | e23 |
| 2026-04-17 | Quote | ★ The snapshot settled arguments with contractor gang leaders | Shift in-charge, packing | `05_meetings/2026-04-17_poc_review_transcript.txt:27` | e24 |
| 2026-04-17 | Decided | Pilot approved on 40 cameras, with the kiln platform added; new Head EHS owns it | Rajiv Bhandari | `05_meetings/2026-04-17_poc_review_transcript.txt:47` | e26 |
| 2026-04-17 | Decided | Retraining must happen on site; images never leave | Farhan Siddiqui | `05_meetings/2026-04-17_poc_review_transcript.txt:43` | e27c |
| 2026-04-22 | Changed | CR-01: kiln platform hot-zone detection (face shield) replaces the 'area to be confirmed' | Meenakshi Iyer; approved by Rajiv Bhandari | `03_commercial/change_requests_CR01-CR03.md:5` | e28 |
| 2026-04-22 | Decided | Counting rules agreed with EHS: one person per camera per 10-minute window | EHS + PredCo | `08_github/README.md:19` | e29 |

## 2026-05

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-05-04 | Happened | Pilot purchase order issued (40 cameras, 8 weeks) | Rajiv Bhandari | `03_commercial/purchase_orders.md:22` | e30 |
| 2026-05-11 | Happened | Pilot live on 40 cameras with alerts to the control room and text-only messages | PredCo | `08_github/CHANGELOG.md:27` | e31 |
| 2026-05-14 | Problem | ★ Corporate Legal finds face-recognition attendance was never referred to Legal and puts it on hold | Pooja Menon (Corporate Legal) | `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:11` | e32 |
| 2026-05-20 | Decided | Legal decides not to proceed with face recognition in 2026 and asks for proof of removal | Pooja Menon | `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:40` | e34 |
| 2026-05-26 | Changed | CR-02: face-recognition attendance removed from scope with a credit | Pooja Menon | `03_commercial/change_requests_CR01-CR03.md:12` | e34b |

## 2026-06

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-06-02 | Happened | Release v1.2 removes the face module from the installed software; client IT verifies the package hash | Karthik Raman; verified by client IT-OT | `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:54` | e35 |
| 2026-06-09 | Problem | ★ Incident: about 41 hours with no usable video on 22 of the 40 pilot cameras after an NVR firmware update | Client CCTV contractor / PredCo | `04_delivery/incident_report_INC-0611.md:9` | e36 |
| 2026-06-12 | Changed | Fixes: no-frames alarm after 5 minutes, 24-hour notice before NVR firmware changes, daily 08:00 camera health message | PredCo + client IT | `04_delivery/incident_report_INC-0611.md:27` | e38 |
| 2026-06-15 | Happened | ★ Detector retrained on 4,200 labelled site frames on an on-premise training box | PredCo | `08_github/CHANGELOG.md:16` | e40 |
| 2026-06-26 | Quote | ★ Client credits its own actions: safety week, daily toolbox talks, suspending two contractor gangs | Meenakshi Iyer | `05_meetings/2026-06-26_steering_committee_transcript.txt:22` | e41 |
| 2026-06-26 | Decided | ★ Finance rejects the vendor's benchmark-based ~2 crore return estimate | Sunil Kedia (AGM Finance) | `05_meetings/2026-06-26_steering_committee_transcript.txt:36` | e43 |
| 2026-06-26 | Decided | Decision to go plant-wide on all cameras plus the gate, using finance's numbers not benchmarks | Rajiv Bhandari | `05_meetings/2026-06-26_steering_committee_transcript.txt:48` | e44 |
| 2026-06-26 | Decided | Plant-wide decision | Rajiv Bhandari | `05_meetings/2026-06-26_steering_committee_transcript.txt:48` | e44b |

## 2026-07

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-07-01 | Problem | ★ Client stops the vendor's capex summary: it mixed the manual walk score with the best packing week | Meenakshi Iyer | `06_email/E_2026-07-01_pilot_results_numbers.md:36` | e46 |
| 2026-07-02 | Changed | CR-03: gate truck-turnaround analytics added, with KPI K5 (-15% turnaround by end September vs the manual register) | Rajiv Bhandari | `03_commercial/change_requests_CR01-CR03.md:26` | e51 |
| 2026-07-02 | Problem | Client warns a second weighbridge (its own separate investment) will be commissioned in August | Client | `03_commercial/change_requests_CR01-CR03.md:27` | e52 |
| 2026-07-06 | Decided | Vendor commits to BRD definitions only | Neha Sharma | `06_email/E_2026-07-01_pilot_results_numbers.md:57` | e47b |
| 2026-07-06 | Decided | Pilot accepted with conditions: K1 and K4 met, K2 and K3 missed | Head EHS, Unit Head, PredCo Delivery Manager | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:16` | e48 |
| 2026-07-06 | Changed | Acceptance condition for K2: the client installs physical guards at the conveyor tail pulleys; vendor adds a 2 m pre-zone warning | Client maintenance | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:19` | e49 |
| 2026-07-06 | Changed | Acceptance condition for K3: control room phones the in-charge if an alert is not acknowledged in 5 minutes | Client control room | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:21` | e50 |
| 2026-07-10 | Decided | Shift-change locker corridor excluded from alerts at shift change - logged as a rule change, no hidden exceptions | Meenakshi Iyer | `09_feedback/whatsapp_Drishti-Packing_group_export.txt:24` | e54 |
| 2026-07-14 | Happened | Plant-wide purchase order issued | Client corporate (capex approved 9 Jul) | `03_commercial/purchase_orders.md:37` | e53 |
| 2026-07-24 | Problem | Scale-up batch 1 slipped a week after a client PoE switch failure | Client IT | `04_delivery/project_tracker.csv:22` | t21 |

## 2026-08

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-08-03 | Happened | Release v2.0: plant-wide camera configs, third edge server, gate turnaround analytics live | PredCo | `08_github/CHANGELOG.md:6` | e55 |
| 2026-08-04 | Happened | Control-room escalation after 5 minutes without acknowledgement switched on | PredCo / client control room | `08_github/git_log.txt:10` | e56 |
| 2026-08-12 | Happened | Physical tail-pulley guards go in; vendor 2 m pre-zone warning deployed | Client maintenance + PredCo | `05_meetings/2026-09-18_QBR_transcript.txt:16` | e57 |
| 2026-08-12 | Problem | Public press release names the client's second weighbridge at this unit - mentioning a weighbridge would identify the client | Client press release (public) | `11_public/ardent_public_profile.md:15` | e99 |
| 2026-08-12 | Happened | Tail-pulley guards (client action) planned for July, completed 12 Aug | Client maintenance | `04_delivery/project_tracker.csv:27` | t26 |
| 2026-08-18 | Happened | Client's second weighbridge commissioned | Client (own capex) | `07_data/gate_truck_turnaround_daily.csv:80` | e58 |
| 2026-08-24 | Problem | Cause of late payment: service GRN not confirmed by the user department | Lokesh Jain | `06_email/F_2026-08-21_to_09-03_payment_GRN.md:25` | e61b |
| 2026-08-25 | Happened | ★ Client logistics starts dispatch slots using the queue alerts | Client logistics | `07_data/gate_truck_turnaround_daily.csv:87` | e59 |
| 2026-08-31 | Happened | All cameras live | PredCo | `08_github/git_log.txt:6` | e60 |

## 2026-09

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-09-03 | Happened | Two overdue invoices paid after goods-receipt (GRN) delay | Lokesh Jain | `06_email/F_2026-08-21_to_09-03_payment_GRN.md:37` | e61 |
| 2026-09-10 | Happened | Group safety pre-assessment: provisionally B+, up from C last year | Group corporate assessor | `05_meetings/2026-09-18_QBR_transcript.txt:32` | e62 |
| 2026-09-12 | Decided | Plant-wide go-live signed off; 60-day stabilisation under way | Client + PredCo | `04_delivery/project_tracker.csv:29` | t28 |
| 2026-09-14 | Happened | Client pays a bonus to gangs above 95% compliance | Meenakshi Iyer | `09_feedback/whatsapp_Drishti-Packing_group_export.txt:27` | e92 |
| 2026-09-18 | Quote | ★ Vendor says the gate gain cannot be split cleanly between its queue view and the client's dispatch slots | Neha Sharma | `05_meetings/2026-09-18_QBR_transcript.txt:28` | e65 |
| 2026-09-18 | Decided | ★ Case study allowed only anonymised: no plant name, state, capacity or photos of people; via Legal and Corporate Comms | Rajiv Bhandari | `05_meetings/2026-09-18_QBR_transcript.txt:44` | e68 |
| 2026-09-18 | Problem | A competitor plant is 40 km away - the sponsor's real fear | Rajiv Bhandari | `05_meetings/2026-09-18_QBR_transcript.txt:40` | e69 |
| 2026-09-18 | Problem | A previous vendor used the logo without asking | Rajiv Bhandari | `05_meetings/2026-09-18_QBR_transcript.txt:44` | e69b |
| 2026-09-22 | Decided | Finance: credit the project with 'a share', not a number, until Oct-Dec data | Sunil Kedia | `06_email/G_2026-09-22_finance_value_estimate.md:17` | e71 |
| 2026-09-23 | Problem | Vendor sales draft claims 97% compliance, zero accidents and 2.3 crore saved - none survives checking | PredCo sales (unreviewed) | `12_vendor/sales_deck_draft_notes_2026-09-23.md:5` | e100 |
| 2026-09-24 | Problem | Vendor asks the plant head for a quick WhatsApp go-ahead with an overclaiming headline | Aarav Malhotra | `06_email/H_2026-09-24_to_09-30_case_study_permission.md:13` | e75 |
| 2026-09-25 | Decided | Refused: not on WhatsApp, not by him alone; 'cement major' with those numbers identifies the client | Rajiv Bhandari | `06_email/H_2026-09-24_to_09-30_case_study_permission.md:28` | e76 |
| 2026-09-28 | Decided | Legal sets the process: full pack to Corporate Comms with Legal in copy, ten business days before first use | Pooja Menon | `06_email/H_2026-09-24_to_09-30_case_study_permission.md:44` | e77 |
| 2026-09-28 | Decided | Legal: list every number and its source | Pooja Menon | `06_email/H_2026-09-24_to_09-30_case_study_permission.md:46` | e77b |
| 2026-09-28 | Decided | Legal wants two options: not identifiable at all, or named | Pooja Menon | `06_email/H_2026-09-24_to_09-30_case_study_permission.md:47` | e78 |
| 2026-09-28 | Decided | Do not use her April remark about her previous plant | Meenakshi Iyer | `06_email/H_2026-09-24_to_09-30_case_study_permission.md:61` | e80 |
| 2026-09-29 | Problem | An award nomination naming the client was submitted without approval and withdrawn | PredCo | `12_vendor/vendor_profile_team_achievements.md:27` | e81 |
| 2026-09-30 | Problem | The client's Head EHS has publicly linked the client, the project name and the vendor on LinkedIn - quoting it would identify the client | Meenakshi Iyer (public post) | `09_feedback/linkedin_post_2026-09-30_Meenakshi_Iyer.md:11` | e82 |

## 2026-10

| Date | Type | What | Who decided / said | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-10-27 | Happened | Final group safety audit scheduled | Group corporate | `05_meetings/2026-09-18_QBR_transcript.txt:32` | e119 |

## What changed between promise and delivery

| Date | Change | Source |
| --- | --- | --- |
| 2026-02-19 | Vendor redesigns: updates as signed packages via jump host, jump-host-only access, alerts carry text only and the image stays on the plant console | `06_email/B_2026-02-17_to_03-02_security_review.md:33` |
| 2026-03-05 | Signed BRD v2 lowers all four targets and replaces the walk baseline with the camera-measured first two pilot weeks | `02_scoping/2026-03-05_BRD_v2_signed.md:14` |
| 2026-04-22 | CR-01: kiln platform hot-zone detection (face shield) replaces the 'area to be confirmed' | `03_commercial/change_requests_CR01-CR03.md:5` |
| 2026-05-26 | CR-02: face-recognition attendance removed from scope with a credit | `03_commercial/change_requests_CR01-CR03.md:12` |
| 2026-06-12 | Fixes: no-frames alarm after 5 minutes, 24-hour notice before NVR firmware changes, daily 08:00 camera health message | `04_delivery/incident_report_INC-0611.md:27` |
| 2026-07-02 | CR-03: gate truck-turnaround analytics added, with KPI K5 (-15% turnaround by end September vs the manual register) | `03_commercial/change_requests_CR01-CR03.md:26` |
| 2026-07-06 | Acceptance condition for K2: the client installs physical guards at the conveyor tail pulleys; vendor adds a 2 m pre-zone warning | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:19` |
| 2026-07-06 | Acceptance condition for K3: control room phones the in-charge if an alert is not acknowledged in 5 minutes | `04_delivery/pilot_acceptance_certificate_2026-07-06.md:21` |

## Delays and how they were overcome (from the project tracker)

Source: `04_delivery/project_tracker.csv`. Tasks that finished after their planned end, or are not done.

| Task | What | Owner | Planned end | Actual end | Slip | Tracker note |
| --- | --- | --- | --- | --- | --- | --- |
| T02 | Security pack and architecture note to IT-OT | N. Sharma | 2026-02-20 | 2026-03-02 | +10 d | 3 review rounds with F. Siddiqui; jump host design changed |
| T04 | BRD v2 sign-off | N. Sharma | 2026-03-03 | 2026-03-05 | +2 d | KPI targets revised by EHS |
| T05 | Edge server install (loan unit) in server room | V. Anand | 2026-03-13 | 2026-03-16 | +3 d | Server room access card delay |
| T06 | Connect 12 camera streams | V. Anand | 2026-03-16 | 2026-03-19 | +3 d | 2 cameras 352x288 only, replaced by PK2-07 and PK2-09 |
| T07 | Zone polygons for tail pulley | N. Sharma | 2026-03-17 | 2026-03-18 | +1 d |  |
| T10 | CR-01 kiln hot-zone rule | N. Sharma | 2026-05-08 | 2026-05-12 | +4 d | Face-shield class needs 600 more site images |
| T11 | Scale to 40 cameras + 2nd edge server | V. Anand | 2026-05-08 | 2026-05-10 | +2 d |  |
| T13 | Face module for R8 | K. Raman | 2026-05-29 | 2026-05-20 | Cancelled | CR-02 (Legal) |
| T14 | Remove face module from build + written confirmation | K. Raman | 2026-05-29 | 2026-06-02 | +4 d | Release v1.2 |
| T16 | Retrain on site images (4200 frames) | K. Raman | 2026-06-12 | 2026-06-14 | +2 d | Release v1.3 deployed 15 Jun |
| T18 | Stream health monitor | K. Raman | 2026-06-19 | 2026-06-24 | +5 d | Release v1.4 (deployed with scale) |
| T20 | Pilot acceptance | M. Iyer | 2026-07-03 | 2026-07-06 | +3 d | Accepted with conditions (K2/K3 remediation) |
| T21 | 3rd edge server + cameras batch 1 (packing, conveyor) | V. Anand | 2026-07-17 | 2026-07-24 | +7 d | Batch 1 slipped 1 week: PoE switch failure, client IT |
| T22 | Cameras batch 2 (kiln, raw mill, cement mill) | V. Anand | 2026-07-31 | 2026-08-07 | +7 d |  |
| T23 | ANPR cameras G1-G4 + weighbridge feed (CR-03) | N. Sharma | 2026-08-01 | 2026-08-03 | +2 d | Gate analytics live 3 Aug |
| T24 | Cameras batch 3 (gate yard, stores) | V. Anand | 2026-08-14 | 2026-08-21 | +7 d |  |
| T25 | Control room escalation: phone call if alert not acked in 5 min | S. Qureshi | 2026-07-31 | 2026-08-04 | +4 d | Remediation for K3 |
| T26 | Conveyor tail pulley physical guards (client) | Ardent maintenance | 2026-07-31 | 2026-08-12 | +12 d | Remediation for K2 (client action) |
| T27 | All 146 cameras live | V. Anand | 2026-08-28 | 2026-08-31 | +3 d |  |
| T30 | 60-day stabilisation | S. Qureshi | 2026-11-11 | - | In progress |  |

## Data-quality issues found while reading

- 04_delivery/project_tracker.csv line 22: 1 unquoted comma(s) in 'task', repaired
- 04_delivery/project_tracker.csv line 23: 2 unquoted comma(s) in 'task', repaired
- 04_delivery/project_tracker.csv line 25: 1 unquoted comma(s) in 'task', repaired

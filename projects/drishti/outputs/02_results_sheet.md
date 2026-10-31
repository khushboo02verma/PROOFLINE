# Results sheet

Every number below is recomputed from the raw exports in `07_data` (or from a cited line where no raw data exists). The working column shows the calculation. Where sources disagree, the table says which one was used and why.

## K1 - PPE compliance (helmet and vest)

| Field | Value |
| --- | --- |
| Definition | Persons observed wearing both helmet and vest / persons observed. A person = one tracked person per camera per 10-minute window (one person on two cameras counts twice). |
| Baseline | 68.9% (camera-measured, pilot weeks 1-2 (11-24 May), 40 pilot cameras, per BRD v2) |
| Measurement window | Average of last 4 pilot weeks (8 Jun-5 Jul), ratio of sums |
| Method | Recomputed from the weekly export: sum(ppe_compliant) / sum(persons_observed), pilot cohort only |
| Final number | **91.1%** pilot result (BRD window); **94.4%** pilot cameras, Sep; **89.2%** all cameras, Sep |
| Target | ≥ 90% (BRD v2; proposal had promised 95%) |
| Status | MET (91.1% vs 90%). Still above target on pilot cameras in September; all-camera figure is lower because areas added later started lower. |
| What else contributed | Client: safety week in April, daily toolbox talks from May, two contractor gangs suspended in May (identified from snapshots), gang bonus for >95% in Sep. Vendor: on-site retrain on 4,200 frames (15 Jun) cut false alarms so supervisors trusted the alerts. |
| Honest worth | +22.2 points in 8 weeks on a like-for-like camera measure. The pilot areas held at ~94% three months later. It is a leading indicator; it does not by itself prove fewer injuries. |

**Where sources disagree**

| Source says | Where | Used? | Why |
| --- | --- | --- | --- |
| 74% -> 96.6%, 'a 31% improvement' | 06_email/E (vendor email, 1 Jul); 12_vendor/sales deck notes say 74% -> 97% | No | 74% is the announced manual walk score (BRD says not comparable); 96.6% is the packing pilot cameras in their best week (recomputed: K1_packing_best). Client rejected this in writing. |
| 61% in first two weeks, 78% in week five | 05_meetings PoC review (17 Apr) | Context only | PoC: 12 cameras, different scope and window; not the BRD baseline. |
| Manual walk score 73.8% (882 people) | BRD v2 §4; recomputed from 07_data walks file | Context only | Announced walks (23 of 103 remarks say so), 2 per day, one area; BRD records it 'for reference only'. |
| All-camera line fell from 93.6% to about 86% in August | 10_media dashboard export; QBR | Explained, not hidden | Mix effect: added cameras start low (72% in their first week). Pilot cohort never dropped below 92%. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| K1_base | 68.9% | 8 | sum(ppe_compliant) = 9,978; sum(persons_observed) = 14,486; 100 x 9,978 / 14,486 = 68.8803 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_result | 91.1% | 16 | sum(ppe_compliant) = 26,081; sum(persons_observed) = 28,634; 100 x 26,081 / 28,634 = 91.0840 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_post_pilot | 94.4% | 16 | sum(ppe_compliant) = 28,611; sum(persons_observed) = 30,302; 100 x 28,611 / 30,302 = 94.4195 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_post_all | 89.2% | 44 | sum(ppe_compliant) = 98,832; sum(persons_observed) = 110,830; 100 x 98,832 / 110,830 = 89.1744 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_change_pts | 22.2 pts | 0 | r = K1_result = 91.08; b = K1_base = 68.88 -> r - b = 22.2 | `evidence ledger` |
| K1_final_week | 93.6% | 4 | sum(ppe_compliant) = 6,982; sum(persons_observed) = 7,456; 100 x 6,982 / 7,456 = 93.6427 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_packing_best | 96.6% | 1 | sum(ppe_compliant) = 3,920; sum(persons_observed) = 4,058; 100 x 3,920 / 4,058 = 96.5993 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_post_scale | 87.2% | 28 | sum(ppe_compliant) = 70,221; sum(persons_observed) = 80,528; 100 x 70,221 / 80,528 = 87.2007 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_scale_first | 72.0% | 1 | sum(ppe_compliant) = 1,445; sum(persons_observed) = 2,008; 100 x 1,445 / 2,008 = 71.9622 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_aug_all | 86.8% | 42 | sum(ppe_compliant) = 87,505; sum(persons_observed) = 100,857; 100 x 87,505 / 100,857 = 86.7615 | `07_data/viewos_weekly_zone_metrics.csv` |
| K1_gate_yard | 79.2% | 4 | sum(ppe_compliant) = 13,194; sum(persons_observed) = 16,650; 100 x 13,194 / 16,650 = 79.2432 | `07_data/viewos_weekly_zone_metrics.csv` |
| walk_compliance | 73.8% | 103 | sum(fully_compliant) = 651; sum(people_observed) = 882; 100 x 651 / 882 = 73.8095 | `07_data/baseline_manual_safety_walks_2025Q4.csv` |
| walk_people | 882 | 103 | sum(people_observed) over 103 rows = 882 | `07_data/baseline_manual_safety_walks_2025Q4.csv` |
| walk_count | 103 | 103 | rows matching filter = 103 | `07_data/baseline_manual_safety_walks_2025Q4.csv` |
| walk_announced | 23 | 23 | rows matching filter = 23 | `07_data/baseline_manual_safety_walks_2025Q4.csv` |
| walk_gap | 4.9 pts | 0 | w = walk_compliance = 73.81; b = K1_base = 68.88 -> w - b = 4.929 | `evidence ledger` |

## K2 - Restricted-zone breaches (conveyor tail pulleys, kiln hot zone)

| Field | Value |
| --- | --- |
| Definition | Entries of a tracked person's feet into a zone polygon for > 2 s, per 1,000 camera-hours of usable video, pilot cameras. |
| Baseline | 5.58 (pilot weeks 1-2) |
| Measurement window | Last 4 pilot weeks; re-measured on pilot cameras for the last 4 weeks to 27 Sep |
| Method | sum(breaches) / sum(camera_hours) x 1,000 |
| Final number | **3.00** pilot result (BRD window); **-46.2%** vs baseline at pilot end; **1.26** pilot cameras, Sep; **-77.3%** vs baseline, Sep |
| Target | −50% (BRD v2; proposal had promised −70%) |
| Status | NOT MET at pilot end (−46%). Condition met by September (−77%) after the client installed physical guards on 12 Aug and the vendor added a 2 m pre-zone warning. |
| What else contributed | Mostly the client's physical guards (engineering control). Vendor: detection, pre-zone warning, evidence for where guards were needed. |
| Honest worth | Report as 'missed at pilot end, then fixed together'. Do not credit software alone with −77%. |

**Where sources disagree**

| Source says | Where | Used? | Why |
| --- | --- | --- | --- |
| 'Restricted zone entries down by half' (1 Jul) | 06_email/E vendor email | No | Was −46% against a −50% target; client asked to say that. |
| 'Now 2.7, about minus 50%' (26 Jun) | 05_meetings steering committee | No | Single week, before pilot end; BRD window is last 4 weeks. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| K2_base | 5.58 | 8 | sum(restricted_zone_breaches) = 75; sum(camera_hours) = 13,440; 1000 x 75 / 13,440 = 5.5804 | `07_data/viewos_weekly_zone_metrics.csv` |
| K2_result | 3.00 | 16 | sum(restricted_zone_breaches) = 78; sum(camera_hours) = 25,978; 1000 x 78 / 25,978 = 3.0025 | `07_data/viewos_weekly_zone_metrics.csv` |
| K2_change_pct | -46.2% | 0 | r = K2_result = 3.003; b = K2_base = 5.58 -> 100 * (r - b) / b = -46.19 | `evidence ledger` |
| K2_post | 1.26 | 16 | sum(restricted_zone_breaches) = 34; sum(camera_hours) = 26,880; 1000 x 34 / 26,880 = 1.2649 | `07_data/viewos_weekly_zone_metrics.csv` |
| K2_post_change | -77.3% | 0 | r = K2_post = 1.265; b = K2_base = 5.58 -> 100 * (r - b) / b = -77.33 | `evidence ledger` |

## K3 - Alert acknowledgement time

| Field | Value |
| --- | --- |
| Definition | Minutes from alert to acknowledgement by the area in-charge. |
| Baseline | 8.6 min (pilot weeks 1-2 (BRD says n/a; shown for context)) |
| Measurement window | Last 4 pilot weeks; re-measured last 4 weeks to 27 Sep |
| Method | Alert-weighted mean of weekly zone medians (the library has no alert-level data, so a true median cannot be computed). This reproduces the certificate's 4.9 and 3.5. |
| Final number | **4.9 min** pilot (BRD window); **3.5 min** final pilot week; **2.1 min** pilot cameras, Sep; **2.3 min** all cameras, Sep |
| Target | ≤ 3.0 min (BRD v2; proposal had promised 2) |
| Status | NOT MET at pilot end (4.9 min; the outage week inflated it). Met by September after the client's control-room phone rule (escalation live 4 Aug). |
| What else contributed | Client: control room phones the in-charge after 5 minutes. Vendor: alerts routed to the area in-charge, escalation hook, daily camera health message after the outage. |
| Honest worth | Response time is what the sponsor said he was buying ('response time, not logins'). |

**Where sources disagree**

| Source says | Where | Used? | Why |
| --- | --- | --- | --- |
| 'Alert response 9 min -> 2 min' | 12_vendor sales deck notes | Partly | Direction right; baseline is 8.6 (alert-weighted, weeks 1-2) and 2.1 is the pilot cohort in Sep; must name the phone rule as a cause. |
| 'Under 4 minutes' (1 Jul) | 06_email/E | No | Last-4-week figure was 4.9. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| K3_base | 8.6 min | 8 | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 4,929.3 / 571 = 8.6327 | `07_data/viewos_weekly_zone_metrics.csv` |
| K3_result | 4.9 min | 16 | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 1,748.3 / 357 = 4.8972 | `07_data/viewos_weekly_zone_metrics.csv` |
| K3_final_week | 3.5 min | 4 | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 244.4 / 69 = 3.5420 | `07_data/viewos_weekly_zone_metrics.csv` |
| K3_post_pilot | 2.1 min | 16 | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 453.9 / 218 = 2.0821 | `07_data/viewos_weekly_zone_metrics.csv` |
| K3_post_all | 2.3 min | 44 | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 3,385.0 / 1,464 = 2.3122 | `07_data/viewos_weekly_zone_metrics.csv` |

## K4 - False alarms

| Field | Value |
| --- | --- |
| Definition | Share of alerts marked false in the EHS daily sample review, scaled to the week (EHS labels, not model confidence, since 3 Jun). |
| Baseline | 19.8% (pilot weeks 1-2 (BRD says n/a; PoC was 23%)) |
| Measurement window | Last 2 pilot weeks |
| Method | sum(alerts_false_verified) / sum(alerts_raised) |
| Final number | **9.7%** pilot (BRD window); **12.1%** kiln hot-zone cameras; **6.2%** all cameras, Sep |
| Target | < 10% (BRD v2; proposal had promised 5%) |
| Status | MET, narrowly (9.7%). Kiln hot-zone still above 10% at pilot end (12.1%). |
| What else contributed | Vendor retrain on 4,200 site frames on an on-premise box; client EHS labelled the sample. |
| Honest worth | This is the number that kept the project alive: the Head EHS said 23% 'is how a system dies'. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| K4_base | 19.8% | 8 | sum(alerts_false_verified) = 113; sum(alerts_raised) = 571; 100 x 113 / 571 = 19.7898 | `07_data/viewos_weekly_zone_metrics.csv` |
| K4_result | 9.7% | 8 | sum(alerts_false_verified) = 15; sum(alerts_raised) = 155; 100 x 15 / 155 = 9.6774 | `07_data/viewos_weekly_zone_metrics.csv` |
| K4_kiln_last2 | 12.1% | 2 | sum(alerts_false_verified) = 4; sum(alerts_raised) = 33; 100 x 4 / 33 = 12.1212 | `07_data/viewos_weekly_zone_metrics.csv` |
| K4_post_all | 6.2% | 44 | sum(alerts_false_verified) = 91; sum(alerts_raised) = 1,464; 100 x 91 / 1,464 = 6.2158 | `07_data/viewos_weekly_zone_metrics.csv` |

## K5 - Truck turnaround at the gate (added by CR-03)

| Field | Value |
| --- | --- |
| Definition | Average minutes from gate-in to gate-out per truck. |
| Baseline | 93.5 min (manual gate register 1 Jun-2 Aug (handwritten, rounded to 5 min, 6 days missing) - the contract baseline) |
| Measurement window | Camera data 25 Aug-30 Sep (excl. 11 Sep calibration day) |
| Method | Mean of daily averages |
| Final number | **67.2 min** dispatch-slot period; **-28.1%** vs contract baseline; **-24.1%** vs first 2 weeks of camera data (like-for-like) |
| Target | −15% by end Sep |
| Status | MET on either basis. Quote the like-for-like −24% externally: the register baseline is not comparable. |
| What else contributed | Client gate-infrastructure upgrade (commissioned 18 Aug; ~6 min) and client logistics' dispatch slots run from the queue view (~16 min). Vendor: the queue view and alerts that made slots possible. The vendor itself says the split cannot be made cleanly. |
| Honest worth | Shared credit. The gate dashboard alone (3-17 Aug) did not move turnaround much. |

**Where sources disagree**

| Source says | Where | Used? | Why |
| --- | --- | --- | --- |
| 'June-July manual register said 93 or 94' | QBR | As contract baseline only | Handwritten, rounded to 5 minutes, missing days; method changed on 3 Aug. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| gate_manual_mean | 93.5 min | 57 | mean(avg_turnaround_min) over 57 non-blank rows = 5,330.0 / 57 = 93.5088 | `07_data/gate_truck_turnaround_daily.csv` |
| gate_anpr_slots | 67.2 min | 36 | mean(avg_turnaround_min) over 36 non-blank rows = 2,420.7 / 36 = 67.2417 | `07_data/gate_truck_turnaround_daily.csv` |
| K5_change_vs_register | -28.1% | 0 | s = gate_anpr_slots = 67.24; m = gate_manual_mean = 93.51 -> 100 * (s - m) / m = -28.09 | `evidence ledger` |
| gate_like_for_like | -24.1% | 0 | s = gate_anpr_slots = 67.24; f = gate_anpr_first = 88.54 -> 100 * (s - f) / f = -24.06 | `evidence ledger` |
| gate_manual_missing | 6 | 6 | rows matching filter = 6 | `07_data/gate_truck_turnaround_daily.csv` |
| gate_anpr_first | 88.5 min | 15 | mean(avg_turnaround_min) over 15 non-blank rows = 1,328.1 / 15 = 88.5400 | `07_data/gate_truck_turnaround_daily.csv` |
| gate_anpr_wb | 82.8 min | 7 | mean(avg_turnaround_min) over 7 non-blank rows = 579.5 / 7 = 82.7857 | `07_data/gate_truck_turnaround_daily.csv` |
| gate_step_infra | 5.8 min | 0 | f = gate_anpr_first = 88.54; w = gate_anpr_wb = 82.79 -> f - w = 5.754 | `evidence ledger` |
| gate_step_slots | 15.5 min | 0 | w = gate_anpr_wb = 82.79; s = gate_anpr_slots = 67.24 -> w - s = 15.54 | `evidence ledger` |

## MONEY - Money: transporter detention (the only measured money)

| Field | Value |
| --- | --- |
| Definition | Detention paid to transporters per month, from the client's ERP (finance). |
| Baseline | 12.1 L/month (Jun-Jul average) |
| Measurement window | September (partly estimated to month end) |
| Method | From finance value note; no raw ERP data in the library |
| Final number | **3.9 L/month** September; **-67.8%** change |
| Target | None set |
| Status | Measured, one month only. Finance credits the project with 'a share', not a number. |
| What else contributed | Client gate-infrastructure upgrade (own investment) and dispatch slots; vendor queue view. |
| Honest worth | Client finance's own view: payback a little over two years if half of the detention saving is credited; under 14 months only if the full saving holds AND the insurance premium falls. Benchmark '2 crore' and '2.3 crore' figures are not used: finance rejected them. Avoided-injury savings are not claimed. Insurance is 'possible, not realised'. |

**Where sources disagree**

| Source says | Where | Used? | Why |
| --- | --- | --- | --- |
| 'Rs 2.3 Cr annual savings' incl. Rs 88 L avoided LTIs and Rs 30 L benchmark productivity | 12_vendor sales deck notes | No | Finance: 'We should not claim avoided LTIs as savings'; benchmark rejected at steering committee. |
| 'About Rs 2 crore a year' (benchmark) | 05_meetings steering committee | No | Finance refused it. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| det_junjul | 12.1 L/month | 0 | jun = 11.8 (from e70b, `06_email/G_2026-09-22_finance_value_estimate.md:14`); jul = 12.4 (from e70b, `06_email/G_2026-09-22_finance_value_estimate.md:14`) -> (jun + jul) / 2 = 12.1 | `evidence ledger` |
| det_sep | 3.9 L/month | 0 | s = 3.9 (from e70b, `06_email/G_2026-09-22_finance_value_estimate.md:14`) -> s = 3.9 | `evidence ledger` |
| det_change_pct | -67.8% | 0 | s = det_sep = 3.9; b = det_junjul = 12.1 -> 100 * (s - b) / b = -67.77 | `evidence ledger` |
| spend_total | 107.7 L | 0 | a = 6.5 (from e118, `06_email/G_2026-09-22_finance_value_estimate.md:28`); b = 20.4 (from e118, `06_email/G_2026-09-22_finance_value_estimate.md:28`); c = 80.8 (from e118, `06_email/G_2026-09-22_finance_value_estimate.md:28`) -> a + b + c = 107.7 | `evidence ledger` |

## PEOPLE - What the users say

| Field | Value |
| --- | --- |
| Definition | Paper survey of 18 shift supervisors run by EHS, 14-16 Sep, 1-5 scale. |
| Baseline | none (single survey) |
| Measurement window | 14-16 Sep 2026 |
| Method | Means and counts |
| Final number | **4.2** alerts useful; **1.9** noise; **15** would recommend (of 18) |
| Target | - |
| Status | Positive, with a data-quality caveat: 4 of the 18 comments repeat earlier comments word for word (rows S15-S18 copy S01-S04), so quote comments only from S01-S14 and treat the scores with care. |
| What else contributed | - |
| Honest worth | Supports the user story; not a KPI. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| survey_useful | 4.2 | 18 | mean(alerts_useful_1to5) over 18 non-blank rows = 75.0 / 18 = 4.1667 | `07_data/supervisor_survey_sep2026.csv` |
| survey_noise | 1.9 | 18 | mean(noise_1to5) over 18 non-blank rows = 35.0 / 18 = 1.9444 | `07_data/supervisor_survey_sep2026.csv` |
| survey_yes | 15 | 15 | rows matching filter = 15 | `07_data/supervisor_survey_sep2026.csv` |
| survey_n | 18 | 18 | rows matching filter = 18 | `07_data/supervisor_survey_sep2026.csv` |
| survey_dups | 4 | 18 | 15 non-blank values, 11 distinct -> 4 repeats | `07_data/supervisor_survey_sep2026.csv` |

## SAFETY - Injuries (deliberately not claimed)

| Field | Value |
| --- | --- |
| Definition | Lost-time injuries from the EHS register. |
| Baseline | 4 (calendar 2025) |
| Measurement window | Mar-Sep 2026 |
| Method | Sum of monthly register |
| Final number | **0** Mar-Sep 2026 |
| Target | - |
| Status | NOT CLAIMED. Seven months at roughly one LTI per quarter is not evidence; the client (EHS and finance) said so in writing. Near-miss reports rose, but alerts became loggable as near-misses from 15 Jun, so the rise is partly a definition change. |
| What else contributed | - |
| Honest worth | Zero in external material. |

**Where sources disagree**

| Source says | Where | Used? | Why |
| --- | --- | --- | --- |
| 'Zero LTIs since go-live' / 'zero accidents' | 06_email/E, 06_email/H, sales deck | No | Client: 'proves nothing and the auditors will laugh at it'. |

**Working**

| Metric | Value | Rows | Calculation | Source |
| --- | --- | --- | --- | --- |
| lti_2025 | 4 | 12 | sum(lost_time_injuries) over 12 rows = 4 | `07_data/ehs_register_monthly_2025_2026.csv` |
| lti_mar_sep_2026 | 0 | 7 | sum(lost_time_injuries) over 7 rows = 0 | `07_data/ehs_register_monthly_2025_2026.csv` |
| nearmiss_pre | 19.0 | 5 | mean(near_miss_reports) over 5 non-blank rows = 95.0 / 5 = 19.0000 | `07_data/ehs_register_monthly_2025_2026.csv` |
| nearmiss_post | 43.7 | 3 | mean(near_miss_reports) over 3 non-blank rows = 131.0 / 3 = 43.6667 | `07_data/ehs_register_monthly_2025_2026.csv` |

## All computed metrics

| ID | Name | Value | Filter | Calculation |
| --- | --- | --- | --- | --- |
| K1_base | K1 PPE compliance, pilot weeks 1-2 | 68.9% | {'camera_cohort': 'pilot', 'week_start': {'in': ['2026-05-11', '2026-05-18']}} | sum(ppe_compliant) = 9,978; sum(persons_observed) = 14,486; 100 x 9,978 / 14,486 = 68.8803 |
| K1_result | K1 PPE compliance, last 4 pilot weeks | 91.1% | {'camera_cohort': 'pilot', 'week_start': {'between': ['2026-06-08', '2026-06-29']}} | sum(ppe_compliant) = 26,081; sum(persons_observed) = 28,634; 100 x 26,081 / 28,634 = 91.0840 |
| K1_change_pts | K1 change, percentage points | 22.2 pts | - | r = K1_result = 91.08; b = K1_base = 68.88 -> r - b = 22.2 |
| K1_final_week | K1 final pilot week (all pilot cameras) | 93.6% | {'camera_cohort': 'pilot', 'week_start': '2026-06-29'} | sum(ppe_compliant) = 6,982; sum(persons_observed) = 7,456; 100 x 6,982 / 7,456 = 93.6427 |
| K1_packing_best | Packing pilot cameras, best week (week of 29 Jun) | 96.6% | {'camera_cohort': 'pilot', 'zone': 'packing', 'week_start': '2026-06-29'} | sum(ppe_compliant) = 3,920; sum(persons_observed) = 4,058; 100 x 3,920 / 4,058 = 96.5993 |
| K1_post_pilot | PPE compliance, pilot cameras, last 4 weeks (31 Aug-27 Sep) | 94.4% | {'camera_cohort': 'pilot', 'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(ppe_compliant) = 28,611; sum(persons_observed) = 30,302; 100 x 28,611 / 30,302 = 94.4195 |
| K1_post_scale | PPE compliance, cameras added after the pilot, last 4 weeks | 87.2% | {'camera_cohort': 'scale', 'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(ppe_compliant) = 70,221; sum(persons_observed) = 80,528; 100 x 70,221 / 80,528 = 87.2007 |
| K1_post_all | PPE compliance, all cameras, last 4 weeks | 89.2% | {'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(ppe_compliant) = 98,832; sum(persons_observed) = 110,830; 100 x 98,832 / 110,830 = 89.1744 |
| K1_scale_first | PPE compliance, first week of added cameras (week of 6 Jul) | 72.0% | {'camera_cohort': 'scale', 'week_start': '2026-07-06'} | sum(ppe_compliant) = 1,445; sum(persons_observed) = 2,008; 100 x 1,445 / 2,008 = 71.9622 |
| K1_aug_all | PPE compliance, all cameras, weeks of 3-24 Aug (the dashboard 'dip') | 86.8% | {'week_start': {'between': ['2026-08-03', '2026-08-24']}} | sum(ppe_compliant) = 87,505; sum(persons_observed) = 100,857; 100 x 87,505 / 100,857 = 86.7615 |
| K1_gate_yard | PPE compliance, gate-yard cameras, last 4 weeks | 79.2% | {'zone': 'gate_yard', 'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(ppe_compliant) = 13,194; sum(persons_observed) = 16,650; 100 x 13,194 / 16,650 = 79.2432 |
| K2_base | K2 restricted-zone breaches per 1,000 camera-hours, pilot weeks 1-2 | 5.58 | {'camera_cohort': 'pilot', 'week_start': {'in': ['2026-05-11', '2026-05-18']}} | sum(restricted_zone_breaches) = 75; sum(camera_hours) = 13,440; 1000 x 75 / 13,440 = 5.5804 |
| K2_result | K2 breaches per 1,000 camera-hours, last 4 pilot weeks | 3.00 | {'camera_cohort': 'pilot', 'week_start': {'between': ['2026-06-08', '2026-06-29']}} | sum(restricted_zone_breaches) = 78; sum(camera_hours) = 25,978; 1000 x 78 / 25,978 = 3.0025 |
| K2_change_pct | K2 change vs baseline | -46.2% | - | r = K2_result = 3.003; b = K2_base = 5.58 -> 100 * (r - b) / b = -46.19 |
| K2_post | Breaches per 1,000 camera-hours, pilot cameras, last 4 weeks (after guards) | 1.26 | {'camera_cohort': 'pilot', 'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(restricted_zone_breaches) = 34; sum(camera_hours) = 26,880; 1000 x 34 / 26,880 = 1.2649 |
| K2_post_change | Breaches change vs pilot baseline, after guards | -77.3% | - | r = K2_post = 1.265; b = K2_base = 5.58 -> 100 * (r - b) / b = -77.33 |
| K3_base | K3 acknowledgement minutes, pilot weeks 1-2 (alert-weighted) | 8.6 min | {'camera_cohort': 'pilot', 'week_start': {'in': ['2026-05-11', '2026-05-18']}} | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 4,929.3 / 571 = 8.6327 |
| K3_result | K3 acknowledgement minutes, last 4 pilot weeks | 4.9 min | {'camera_cohort': 'pilot', 'week_start': {'between': ['2026-06-08', '2026-06-29']}} | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 1,748.3 / 357 = 4.8972 |
| K3_final_week | K3 acknowledgement minutes, final pilot week | 3.5 min | {'camera_cohort': 'pilot', 'week_start': '2026-06-29'} | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 244.4 / 69 = 3.5420 |
| K3_post_pilot | Acknowledgement minutes, pilot cameras, last 4 weeks (after phone rule) | 2.1 min | {'camera_cohort': 'pilot', 'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 453.9 / 218 = 2.0821 |
| K3_post_all | Acknowledgement minutes, all cameras, last 4 weeks | 2.3 min | {'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(median_ack_minutes x alerts_raised) / sum(alerts_raised) = 3,385.0 / 1,464 = 2.3122 |
| K4_base | False alarms, pilot weeks 1-2 (EHS sample, scaled) | 19.8% | {'camera_cohort': 'pilot', 'week_start': {'in': ['2026-05-11', '2026-05-18']}} | sum(alerts_false_verified) = 113; sum(alerts_raised) = 571; 100 x 113 / 571 = 19.7898 |
| K4_result | K4 false alarms, last 2 pilot weeks | 9.7% | {'camera_cohort': 'pilot', 'week_start': {'in': ['2026-06-22', '2026-06-29']}} | sum(alerts_false_verified) = 15; sum(alerts_raised) = 155; 100 x 15 / 155 = 9.6774 |
| K4_kiln_last2 | False alarms, kiln hot-zone cameras, last 2 pilot weeks | 12.1% | {'camera_cohort': 'pilot', 'zone': 'kiln', 'week_start': {'in': ['2026-06-22', '2026-06-29']}} | sum(alerts_false_verified) = 4; sum(alerts_raised) = 33; 100 x 4 / 33 = 12.1212 |
| K4_post_all | False alarms, all cameras, last 4 weeks | 6.2% | {'week_start': {'between': ['2026-08-31', '2026-09-21']}} | sum(alerts_false_verified) = 91; sum(alerts_raised) = 1,464; 100 x 91 / 1,464 = 6.2158 |
| outage_hours | Usable camera-hours, pilot, week of 8 Jun (outage week) | 5818 | {'camera_cohort': 'pilot', 'week_start': '2026-06-08'} | sum(camera_hours) over 4 rows = 5,818 |
| outage_lost | Camera-hours lost in outage week (40 cameras x 168 h minus usable) | 902 camera-hours | - | u = outage_hours = 5818 -> 40 * 168 - u = 902 |
| walk_compliance | Manual safety-walk compliance, Q4 2025 | 73.8% | - | sum(fully_compliant) = 651; sum(people_observed) = 882; 100 x 651 / 882 = 73.8095 |
| walk_people | People observed on Q4 2025 walks | 882 | - | sum(people_observed) over 103 rows = 882 |
| walk_count | Number of walks in Q4 2025 | 103 | - | rows matching filter = 103 |
| walk_announced | Walks with remark 'announced on shift WhatsApp group' | 23 | {'remarks': {'contains': 'announced'}} | rows matching filter = 23 |
| walk_gap | Walk score minus camera baseline (points) | 4.9 pts | - | w = walk_compliance = 73.81; b = K1_base = 68.88 -> w - b = 4.929 |
| gate_manual_mean | Truck turnaround, manual register 1 Jun-2 Aug (K5 baseline) | 93.5 min | {'source': {'contains': 'manual'}, 'avg_turnaround_min': {'nonblank': True}} | mean(avg_turnaround_min) over 57 non-blank rows = 5,330.0 / 57 = 93.5088 |
| gate_manual_missing | Manual-register days with no figure | 6 | {'source': {'contains': 'manual'}, 'avg_turnaround_min': {'blank': True}} | rows matching filter = 6 |
| gate_anpr_first | Truck turnaround, camera data, 3-17 Aug (before client gate changes) | 88.5 min | {'date': {'between': ['2026-08-03', '2026-08-17']}} | mean(avg_turnaround_min) over 15 non-blank rows = 1,328.1 / 15 = 88.5400 |
| gate_anpr_wb | Truck turnaround, camera data, 18-24 Aug (after client gate-infrastructure upgrade) | 82.8 min | {'date': {'between': ['2026-08-18', '2026-08-24']}} | mean(avg_turnaround_min) over 7 non-blank rows = 579.5 / 7 = 82.7857 |
| gate_anpr_slots | Truck turnaround, camera data, 25 Aug-30 Sep (dispatch slots), excl. 11 Sep calibration day | 67.2 min | {'date': {'between': ['2026-08-25', '2026-09-30'], 'not_in': ['2026-09-11']}} | mean(avg_turnaround_min) over 36 non-blank rows = 2,420.7 / 36 = 67.2417 |
| K5_change_vs_register | K5 turnaround change vs manual-register baseline (contract definition) | -28.1% | - | s = gate_anpr_slots = 67.24; m = gate_manual_mean = 93.51 -> 100 * (s - m) / m = -28.09 |
| gate_like_for_like | Turnaround change, camera data only (first 2 weeks vs dispatch-slot period) | -24.1% | - | s = gate_anpr_slots = 67.24; f = gate_anpr_first = 88.54 -> 100 * (s - f) / f = -24.06 |
| gate_step_infra | Minutes removed in the week after the client's gate-infrastructure upgrade | 5.8 min | - | f = gate_anpr_first = 88.54; w = gate_anpr_wb = 82.79 -> f - w = 5.754 |
| gate_step_slots | Minutes removed after dispatch slots began | 15.5 min | - | w = gate_anpr_wb = 82.79; s = gate_anpr_slots = 67.24 -> w - s = 15.54 |
| det_junjul | Detention paid, Jun-Jul average (lakh/month) | 12.1 L/month | - | jun = 11.8 (from e70b, `06_email/G_2026-09-22_finance_value_estimate.md:14`); jul = 12.4 (from e70b, `06_email/G_2026-09-22_finance_value_estimate.md:14`) -> (jun + jul) / 2 = 12.1 |
| det_sep | Detention paid, September (finance estimate to month end, lakh) | 3.9 L/month | - | s = 3.9 (from e70b, `06_email/G_2026-09-22_finance_value_estimate.md:14`) -> s = 3.9 |
| det_change_pct | Detention change, September vs Jun-Jul average | -67.8% | - | s = det_sep = 3.9; b = det_junjul = 12.1 -> 100 * (s - b) / b = -67.77 |
| survey_n | Supervisor survey respondents | 18 | - | rows matching filter = 18 |
| survey_useful | Alerts useful (mean, 1-5) | 4.2 | - | mean(alerts_useful_1to5) over 18 non-blank rows = 75.0 / 18 = 4.1667 |
| survey_noise | Alert noise (mean, 1-5, lower is better) | 1.9 | - | mean(noise_1to5) over 18 non-blank rows = 35.0 / 18 = 1.9444 |
| survey_yes | Would recommend to another unit: Yes | 15 | {'would_recommend_other_unit': 'Yes'} | rows matching filter = 15 |
| survey_dups | Survey comments repeated word-for-word | 4 | - | 15 non-blank values, 11 distinct -> 4 repeats |
| lti_2025 | Lost-time injuries, 2025 | 4 | {'month': {'between': ['2025-01', '2025-12']}} | sum(lost_time_injuries) over 12 rows = 4 |
| lti_mar_sep_2026 | Lost-time injuries, Mar-Sep 2026 | 0 | {'month': {'between': ['2026-03', '2026-09']}} | sum(lost_time_injuries) over 7 rows = 0 |
| nearmiss_pre | Near-miss reports per month, Jan-May 2026 | 19.0 | {'month': {'between': ['2026-01', '2026-05']}} | mean(near_miss_reports) over 5 non-blank rows = 95.0 / 5 = 19.0000 |
| nearmiss_post | Near-miss reports per month, Jul-Sep 2026 (definition changed 15 Jun) | 43.7 | {'month': {'between': ['2026-07', '2026-09']}} | mean(near_miss_reports) over 3 non-blank rows = 131.0 / 3 = 43.6667 |
| spend_total | Project spend to date (lakh, before GST, excl. AMC) | 107.7 L | - | a = 6.5 (from e118, `06_email/G_2026-09-22_finance_value_estimate.md:28`); b = 20.4 (from e118, `06_email/G_2026-09-22_finance_value_estimate.md:28`); c = 80.8 (from e118, `06_email/G_2026-09-22_finance_value_estimate.md:28`) -> a + b + c = 107.7 |

# Case study - An Indian cement manufacturer sees its real safety number - and changes it

> STATUS: DRAFT - NOT APPROVED FOR USE. Anonymised under MSA clause 15.2. Requires written approval from the client's Corporate Communications with Legal in copy before first use (see 06_approval).

---

## Version A - for the gatekeeper (procurement, IT security, legal)

### Is this vendor safe to let in, and will I be blamed if it goes wrong?

An Indian cement manufacturer used AI on its existing security cameras to check helmets, vests and restricted zones, and later truck queues at the gate <sup>[e08 `02_scoping/2026-02-14_RFQ_ACWL-BHD-EHS-2026-07.md:11`]</sup> <sup>[e51 `03_commercial/change_requests_CR01-CR03.md:26`]</sup>.
The project ran from a first email to plant-wide use in about seven months <sup>[e01 `06_email/A_2026-01-28_inbound_and_first_reply.md:11`]</sup> <sup>[e60 `08_github/git_log.txt:6`]</sup>.

#### Fact sheet

| Question | Answer <sup>[framing]</sup> |
| --- | --- |
| Where does processing happen? | On edge GPU servers inside the plant's OT network; nothing runs in the cloud <sup>[e86 `01_contract/MSA_confidentiality_and_publicity_extract.md:41`]</sup> <sup>[e04 `02_scoping/2026-02-06_discovery_call_transcript.txt:56`]</sup> |
| Does any data leave the plant? | No internet egress from the servers; video stays on site <sup>[e86b `01_contract/MSA_confidentiality_and_publicity_extract.md:42`]</sup> |
| How do alerts reach phones without images leaving? | The message carries text only; the snapshot opens on a console inside the plant network <sup>[e10 `06_email/B_2026-02-17_to_03-02_security_review.md:33`]</sup> <sup>[e11 `06_email/B_2026-02-17_to_03-02_security_review.md:45`]</sup> |
| How does the vendor get in? | Only through the client's jump host, session recorded, approved per session <sup>[e105 `06_email/B_2026-02-17_to_03-02_security_review.md:14`]</sup> |
| How are updates installed? | As signed packages, installed by the client's own IT team <sup>[e10b `06_email/B_2026-02-17_to_03-02_security_review.md:31`]</sup> |
| How long is footage kept? | Video 30 days, alert snapshots 180 days <sup>[e86c `01_contract/MSA_confidentiality_and_publicity_extract.md:43`]</sup> |
| Is anyone identified? | No: the system detects people and PPE, stores no face templates and identifies no one <sup>[e33 `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:29`]</sup> |
| Certifications | SOC 2 and ISO 27001; because SOC 2 covers company controls, the on-premises deployment adds a checklist mapped to ISO 27001 Annex A <sup>[e87 `12_vendor/vendor_profile_team_achievements.md:7`]</sup> <sup>[e10c `06_email/B_2026-02-17_to_03-02_security_review.md:35`]</sup> |

#### How the risks were handled

IT and OT security raised three blockers before the proof of concept; each was fixed in the design and cleared in writing <sup>[e09 `06_email/B_2026-02-17_to_03-02_security_review.md:11`]</sup> <sup>[e11 `06_email/B_2026-02-17_to_03-02_security_review.md:45`]</sup>.
A face-recognition attendance option was in the original request; corporate legal stopped it on data-protection grounds <sup>[e06 `02_scoping/2026-02-06_discovery_call_transcript.txt:42`]</sup> <sup>[e32 `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:11`]</sup> <sup>[e34 `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:40`]</sup>.
The vendor removed the module from the installed software rather than switching it off, and the client's IT team verified the installed package hash <sup>[e35 `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:54`]</sup> <sup>[e34b `03_commercial/change_requests_CR01-CR03.md:12`]</sup>.
During the pilot, a firmware update by the client's CCTV contractor cut usable video from 22 of the 40 pilot cameras for about 41 hours <sup>[e36 `04_delivery/incident_report_INC-0611.md:9`]</sup>.
The vendor's software still showed those cameras as connected, because it did not check that frames were actually arriving <sup>[e37 `04_delivery/incident_report_INC-0611.md:17`]</sup>.
Responsibility was shared in writing: root cause on the contractor's side, detection gap on the vendor's side <sup>[e39 `04_delivery/incident_report_INC-0611.md:33`]</sup>.
The fixes: an alarm when a camera sends no frames for 5 minutes, 24 hours' notice before any firmware change, and a daily camera health message <sup>[e38 `04_delivery/incident_report_INC-0611.md:27`]</sup> <sup>[e38b `04_delivery/incident_report_INC-0611.md:28`]</sup>.
No safety incident occurred during the gap <sup>[e37b `04_delivery/incident_report_INC-0611.md:23`]</sup>.
Retraining used the plant's own images on a training box inside the plant, so no image left the site <sup>[e40 `08_github/CHANGELOG.md:16`]</sup> <sup>[e27c `05_meetings/2026-04-17_poc_review_transcript.txt:43`]</sup>.
When an alert rule had to change, the client insisted it be logged openly: "I don't want hidden exceptions." <sup>[e54 `09_feedback/whatsapp_Drishti-Packing_group_export.txt:24`]</sup>

#### Will this vendor still be there?

The vendor's field engineer spent 61 days on site, and the team logged about 1,150 person-hours <sup>[e89b `12_vendor/vendor_profile_team_achievements.md:17`]</sup> <sup>[e89 `12_vendor/vendor_profile_team_achievements.md:20`]</sup>.
Every result in this case study uses the definitions the client signed before work began <sup>[e13c `02_scoping/2026-03-05_BRD_v2_signed.md:45`]</sup> <sup>[e47b `06_email/E_2026-07-01_pilot_results_numbers.md:57`]</sup>.

---

## Version B - for the user (plant and shift teams)

### Will this make my shift easier, or add work and embarrass me?

#### Before: a best-case number

Safety compliance used to be counted on announced walks, and shift in-charges warned the floor that a walk was coming <sup>[e02b `02_scoping/2026-02-06_discovery_call_transcript.txt:22`]</sup>.
Those walks said 74% of people wore both helmet and vest <sup>[walk_compliance `07_data/baseline_manual_safety_walks_2025Q4.csv`]</sup>.
The cameras watch every shift, nights and breaks included, and in the first two pilot weeks they found 69% <sup>[K1_base `07_data/viewos_weekly_zone_metrics.csv`]</sup>.
The vendor had warned about this on the very first call: "the first number you see from us will probably look worse than your walk score, not better" <sup>[e03 `02_scoping/2026-02-06_discovery_call_transcript.txt:24`]</sup>.

#### The hard part: false alarms

In the proof of concept, 23% of alerts were false <sup>[e21 `05_meetings/2026-04-17_poc_review_transcript.txt:19`]</sup>.
The new Head of EHS put it plainly: "Twenty-three percent is how a system dies." <sup>[e22 `05_meetings/2026-04-17_poc_review_transcript.txt:21`]</sup>
She set the bar: under ten percent false, every week, checked by her own team, not the vendor's <sup>[e23 `05_meetings/2026-04-17_poc_review_transcript.txt:25`]</sup>.
The vendor retrained the detector on 4,200 labelled frames from the plant's own cameras, on a box inside the plant <sup>[e40 `08_github/CHANGELOG.md:16`]</sup>.
False alarms on the pilot cameras fell from 20% to under 10% by the end of the pilot <sup>[K4_base `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[K4_result `07_data/viewos_weekly_zone_metrics.csv`]</sup>.
Gang leaders noticed within a day; in their words, the new version no longer raised the sack alert <sup>[e40b `09_feedback/whatsapp_Drishti-Packing_group_export.txt:16`]</sup>.

#### The turning point was the photo

A packing shift in-charge described arguing with contractor gang leaders about helmets: "I showed the photo. After that, no argument." <sup>[e24 `05_meetings/2026-04-17_poc_review_transcript.txt:27`]</sup>
The Head of EHS set the rule for how it is used: "Not punishment, proof." <sup>[e25 `05_meetings/2026-04-17_poc_review_transcript.txt:29`]</sup>
Within weeks, gang leaders were checking helmets themselves before the shift started, because nobody wanted their photo in the group <sup>[e45 `05_meetings/2026-06-26_steering_committee_transcript.txt:46`]</sup> <sup>[e91 `09_feedback/whatsapp_Drishti-Packing_group_export.txt:19`]</sup>.
Night shift stayed weaker for longer, and the team said so openly <sup>[e45b `05_meetings/2026-06-26_steering_committee_transcript.txt:46`]</sup>.

#### A normal shift now

An alert goes as a text message to the in-charge of that area, not to a guard in the control room <sup>[e23 `05_meetings/2026-04-17_poc_review_transcript.txt:25`]</sup> <sup>[e10 `06_email/B_2026-02-17_to_03-02_security_review.md:33`]</sup>.
If nobody acknowledges it within 5 minutes, the control room phones the in-charge <sup>[e50 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:21`]</sup>.
Acknowledgement time on the pilot cameras went from nearly 9 minutes in the first two weeks to about 2 minutes <sup>[K3_base `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[K3_post_pilot `07_data/viewos_weekly_zone_metrics.csv`]</sup>.
Where people kept stepping over barriers at conveyor tail pulleys, maintenance installed physical guards, and entries then fell 77% from the start of the pilot <sup>[e49 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:19`]</sup> <sup>[e57 `05_meetings/2026-09-18_QBR_transcript.txt:16`]</sup> <sup>[K2_post_change `evidence ledger`]</sup>.
When people taking helmets off on the way to the lockers at shift change set off alerts, the rule was changed in the open and logged <sup>[e54 `09_feedback/whatsapp_Drishti-Packing_group_export.txt:24`]</sup>.

#### What the people on the floor say

In a survey of 18 supervisors run by the client's safety team, 15 said they would recommend it <sup>[survey_n `07_data/supervisor_survey_sep2026.csv`]</sup> <sup>[survey_yes `07_data/supervisor_survey_sep2026.csv`]</sup>.
One wrote: "Earlier I was blamed for violations I never saw; now I see them first" <sup>[s1 `07_data/supervisor_survey_sep2026.csv:5`]</sup>.
Another: "Response time improved because control room calls directly" <sup>[s2 `07_data/supervisor_survey_sep2026.csv:12`]</sup>.
Not everything is solved: some find the alerts at shift change too many, and some workers still see it as punishment <sup>[s4 `07_data/supervisor_survey_sep2026.csv:10`]</sup> <sup>[s3 `07_data/supervisor_survey_sep2026.csv:11`]</sup>.

#### Credit where it is due

The plant's own teams did much of the work: a safety week, daily toolbox talks, and suspending two contractor gangs who were identified from the snapshots <sup>[e41 `05_meetings/2026-06-26_steering_committee_transcript.txt:22`]</sup> <sup>[e42 `05_meetings/2026-06-26_steering_committee_transcript.txt:24`]</sup>.

---

## Version C - for the buyer (the person who signs)

### Is it worth the money and the risk, and will it make me look good?

#### The headline

Real PPE compliance, measured on camera across every shift, rose from 69% to 91% in an eight-week pilot and met the signed target <sup>[K1_base `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[K1_result `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[c1 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:11`]</sup>.
Three months later the pilot areas held at 94%, while areas added later were at 87% and climbing, as the pilot areas once were <sup>[K1_post_pilot `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[K1_post_scale `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[e64 `05_meetings/2026-09-18_QBR_transcript.txt:12`]</sup>.
Restricted-zone entries are down 77% since the client installed guards where the camera data showed people crossing <sup>[K2_post_change `evidence ledger`]</sup> <sup>[e57 `05_meetings/2026-09-18_QBR_transcript.txt:16`]</sup>.

#### Money, only where it was measured

The client's finance team claimed money only where it could measure it: at the truck gate <sup>[e43b `05_meetings/2026-06-26_steering_committee_transcript.txt:44`]</sup> <sup>[e71 `06_email/G_2026-09-22_finance_value_estimate.md:17`]</sup>.
Truck turnaround fell 24% on like-for-like camera data <sup>[gate_like_for_like `evidence ledger`]</sup>.
Most of that drop came after the client's logistics team started dispatch slots run from the system's queue view; a separate client investment in gate infrastructure also helped <sup>[e59 `07_data/gate_truck_turnaround_daily.csv:87`]</sup> <sup>[gate_step_slots `evidence ledger`]</sup> <sup>[gate_step_infra `evidence ledger`]</sup>.
When finance asked how much was the vendor's, the vendor said: "Honestly, we can't split it cleanly." <sup>[e65 `05_meetings/2026-09-18_QBR_transcript.txt:28`]</sup>
Finance replied: "Good. That's an answer I can defend." <sup>[e66 `05_meetings/2026-09-18_QBR_transcript.txt:30`]</sup>
Transporter detention charges fell 68% from the June-July average to September; that is one month, and finance credits the project with only a share of it <sup>[det_change_pct `evidence ledger`]</sup> <sup>[e71 `06_email/G_2026-09-22_finance_value_estimate.md:17`]</sup>.
On the client's own conservative view, payback is a little over two years <sup>[e72 `06_email/G_2026-09-22_finance_value_estimate.md:31`]</sup>.
The client did not count injuries avoided, and neither do we <sup>[e74 `06_email/G_2026-09-22_finance_value_estimate.md:24`]</sup> <sup>[e67 `05_meetings/2026-09-18_QBR_transcript.txt:36`]</sup>.

#### What the sponsor actually bought

The unit head had bought dashboards before that nobody opened <sup>[e05 `02_scoping/2026-02-06_discovery_call_transcript.txt:38`]</sup>.
The promise was different: "We'd measure response time, not logins." <sup>[e05b `02_scoping/2026-02-06_discovery_call_transcript.txt:40`]</sup>
Alerts on the pilot cameras are now acknowledged in about 2 minutes <sup>[K3_post_pilot `07_data/viewos_weekly_zone_metrics.csv`]</sup>.
The plant's safety pre-assessment improved, and the assessor's note cited "continuous monitoring with evidence-based closure" <sup>[e62 `05_meetings/2026-09-18_QBR_transcript.txt:32`]</sup> <sup>[e63 `05_meetings/2026-09-18_QBR_transcript.txt:32`]</sup>.

#### The risk, honestly

The project had real setbacks and each was handled in the open: a 41-hour camera outage, a privacy stop on face recognition, and two pilot targets missed before being fixed <sup>[e36 `04_delivery/incident_report_INC-0611.md:9`]</sup> <sup>[e34 `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:40`]</sup> <sup>[e48 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:16`]</sup>.
The signed requirements lowered the vendor's own proposed targets before work began, so the results are measured against numbers the client chose <sup>[e13 `02_scoping/2026-03-05_BRD_v2_signed.md:14`]</sup>.

#### The path to scale

It went from a 12-camera proof of concept to 40 pilot cameras to plant-wide use on existing cameras in about five months <sup>[e16 `08_github/CHANGELOG.md:30`]</sup> <sup>[e31 `08_github/CHANGELOG.md:27`]</sup> <sup>[e60 `08_github/git_log.txt:6`]</sup>.
No new cameras were needed for the safety detection <sup>[e01b `06_email/A_2026-01-28_inbound_and_first_reply.md:13`]</sup> <sup>[e55 `08_github/CHANGELOG.md:6`]</sup>.

---

## Forwardable note - for the champion inside the client

### For the Head of EHS to forward to leadership

Subject: what the safety-camera project did, in numbers we can defend <sup>[framing]</sup>

We measured compliance the hard way: on camera, every shift, against the definitions we signed <sup>[e13c `02_scoping/2026-03-05_BRD_v2_signed.md:45`]</sup> <sup>[e47b `06_email/E_2026-07-01_pilot_results_numbers.md:57`]</sup>.
It started lower than our walk scores said, at 69%, and reached 91% in the eight-week pilot <sup>[K1_base `07_data/viewos_weekly_zone_metrics.csv`]</sup> <sup>[K1_result `07_data/viewos_weekly_zone_metrics.csv`]</sup>.
We missed two of the four pilot targets at first, said so, and fixed both with plant actions: tail-pulley guards and a control-room phone rule <sup>[e48 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:16`]</sup> <sup>[e49 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:19`]</sup> <sup>[e50 `04_delivery/pilot_acceptance_certificate_2026-07-06.md:21`]</sup>.
Since then zone entries are down 77% and alerts are acknowledged in about 2 minutes <sup>[K2_post_change `evidence ledger`]</sup> <sup>[K3_post_pilot `07_data/viewos_weekly_zone_metrics.csv`]</sup>.
The credit is shared: our safety week, toolbox talks and firm action on contractor gangs did as much as the cameras <sup>[e41 `05_meetings/2026-06-26_steering_committee_transcript.txt:22`]</sup>.
No video leaves the plant, and the system identifies no one <sup>[e86b `01_contract/MSA_confidentiality_and_publicity_extract.md:42`]</sup> <sup>[e33 `06_email/D_2026-05-14_to_06-02_face_recognition_privacy.md:29`]</sup>.
At the gate, turnaround is down 24% on camera data, with our own dispatch slots doing most of the work <sup>[gate_like_for_like `evidence ledger`]</sup> <sup>[e65 `05_meetings/2026-09-18_QBR_transcript.txt:28`]</sup>.
We do not claim injuries avoided; it is too early and the numbers are too small <sup>[e74 `06_email/G_2026-09-22_finance_value_estimate.md:24`]</sup> <sup>[e67 `05_meetings/2026-09-18_QBR_transcript.txt:36`]</sup>.
Suggested next step: share the approach with peers and decide together whether to extend it <sup>[framing]</sup>

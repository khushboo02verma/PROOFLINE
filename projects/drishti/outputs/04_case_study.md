# Case study - An Indian cement manufacturer sees its real safety number - and changes it

> STATUS: DRAFT - NOT APPROVED FOR USE. Anonymised under MSA clause 15.2. Requires written approval from the client's Corporate Communications with Legal in copy before first use (see 06_approval).

---

## Version A - for the gatekeeper (procurement, IT security, legal)

### Is this vendor safe to let in, and will I be blamed if it goes wrong?

An Indian cement manufacturer used AI on its existing security cameras to check helmets, vests and restricted zones, and later truck queues at the gate.
The project ran from a first email to plant-wide use in about seven months.

#### Fact sheet

| Question | Answer  |
| --- | --- |
| Where does processing happen? | On edge GPU servers inside the plant's OT network; nothing runs in the cloud   |
| Does any data leave the plant? | No internet egress from the servers; video stays on site  |
| How do alerts reach phones without images leaving? | The message carries text only; the snapshot opens on a console inside the plant network   |
| How does the vendor get in? | Only through the client's jump host, session recorded, approved per session  |
| How are updates installed? | As signed packages, installed by the client's own IT team  |
| How long is footage kept? | Video 30 days, alert snapshots 180 days  |
| Is anyone identified? | No: the system detects people and PPE, stores no face templates and identifies no one  |
| Certifications | SOC 2 and ISO 27001; because SOC 2 covers company controls, the on-premises deployment adds a checklist mapped to ISO 27001 Annex A   |

#### How the risks were handled

IT and OT security raised three blockers before the proof of concept; each was fixed in the design and cleared in writing.
A face-recognition attendance option was in the original request; corporate legal stopped it on data-protection grounds.
The vendor removed the module from the installed software rather than switching it off, and the client's IT team verified the installed package hash.
During the pilot, a firmware update by the client's CCTV contractor cut usable video from 22 of the 40 pilot cameras for about 41 hours.
The vendor's software still showed those cameras as connected, because it did not check that frames were actually arriving.
Responsibility was shared in writing: root cause on the contractor's side, detection gap on the vendor's side.
The fixes: an alarm when a camera sends no frames for 5 minutes, 24 hours' notice before any firmware change, and a daily camera health message.
No safety incident occurred during the gap.
Retraining used the plant's own images on a training box inside the plant, so no image left the site.
When an alert rule had to change, the client insisted it be logged openly: "I don't want hidden exceptions."

#### Will this vendor still be there?

The vendor's field engineer spent 61 days on site, and the team logged about 1,150 person-hours.
Every result in this case study uses the definitions the client signed before work began.

---

## Version B - for the user (plant and shift teams)

### Will this make my shift easier, or add work and embarrass me?

#### Before: a best-case number

Safety compliance used to be counted on announced walks, and shift in-charges warned the floor that a walk was coming.
Those walks said 74% of people wore both helmet and vest.
The cameras watch every shift, nights and breaks included, and in the first two pilot weeks they found 69%.
The vendor had warned about this on the very first call: "the first number you see from us will probably look worse than your walk score, not better".

#### The hard part: false alarms

In the proof of concept, 23% of alerts were false.
The new Head of EHS put it plainly: "Twenty-three percent is how a system dies."
She set the bar: under ten percent false, every week, checked by her own team, not the vendor's.
The vendor retrained the detector on 4,200 labelled frames from the plant's own cameras, on a box inside the plant.
False alarms on the pilot cameras fell from 20% to under 10% by the end of the pilot.
Gang leaders noticed within a day; in their words, the new version no longer raised the sack alert.

#### The turning point was the photo

A packing shift in-charge described arguing with contractor gang leaders about helmets: "I showed the photo. After that, no argument."
The Head of EHS set the rule for how it is used: "Not punishment, proof."
Within weeks, gang leaders were checking helmets themselves before the shift started, because nobody wanted their photo in the group.
Night shift stayed weaker for longer, and the team said so openly.

#### A normal shift now

An alert goes as a text message to the in-charge of that area, not to a guard in the control room.
If nobody acknowledges it within 5 minutes, the control room phones the in-charge.
Acknowledgement time on the pilot cameras went from nearly 9 minutes in the first two weeks to about 2 minutes.
Where people kept stepping over barriers at conveyor tail pulleys, maintenance installed physical guards, and entries then fell 77% from the start of the pilot.
When people taking helmets off on the way to the lockers at shift change set off alerts, the rule was changed in the open and logged.

#### What the people on the floor say

In a survey of 18 supervisors run by the client's safety team, 15 said they would recommend it.
One wrote: "Earlier I was blamed for violations I never saw; now I see them first".
Another: "Response time improved because control room calls directly".
Not everything is solved: some find the alerts at shift change too many, and some workers still see it as punishment.

#### Credit where it is due

The plant's own teams did much of the work: a safety week, daily toolbox talks, and suspending two contractor gangs who were identified from the snapshots.

---

## Version C - for the buyer (the person who signs)

### Is it worth the money and the risk, and will it make me look good?

#### The headline

Real PPE compliance, measured on camera across every shift, rose from 69% to 91% in an eight-week pilot and met the signed target.
Three months later the pilot areas held at 94%, while areas added later were at 87% and climbing, as the pilot areas once were.
Restricted-zone entries are down 77% since the client installed guards where the camera data showed people crossing.

#### Money, only where it was measured

The client's finance team claimed money only where it could measure it: at the truck gate.
Truck turnaround fell 24% on like-for-like camera data.
Most of that drop came after the client's logistics team started dispatch slots run from the system's queue view; a separate client investment in gate infrastructure also helped.
When finance asked how much was the vendor's, the vendor said: "Honestly, we can't split it cleanly."
Finance replied: "Good. That's an answer I can defend."
Transporter detention charges fell 68% from the June-July average to September; that is one month, and finance credits the project with only a share of it.
On the client's own conservative view, payback is a little over two years.
The client did not count injuries avoided, and neither do we.

#### What the sponsor actually bought

The unit head had bought dashboards before that nobody opened.
The promise was different: "We'd measure response time, not logins."
Alerts on the pilot cameras are now acknowledged in about 2 minutes.
The plant's safety pre-assessment improved, and the assessor's note cited "continuous monitoring with evidence-based closure".

#### The risk, honestly

The project had real setbacks and each was handled in the open: a 41-hour camera outage, a privacy stop on face recognition, and two pilot targets missed before being fixed.
The signed requirements lowered the vendor's own proposed targets before work began, so the results are measured against numbers the client chose.

#### The path to scale

It went from a 12-camera proof of concept to 40 pilot cameras to plant-wide use on existing cameras in about five months.
No new cameras were needed for the safety detection.

---

## Forwardable note - for the champion inside the client

### For the Head of EHS to forward to leadership

Subject: what the safety-camera project did, in numbers we can defend

We measured compliance the hard way: on camera, every shift, against the definitions we signed.
It started lower than our walk scores said, at 69%, and reached 91% in the eight-week pilot.
We missed two of the four pilot targets at first, said so, and fixed both with plant actions: tail-pulley guards and a control-room phone rule.
Since then zone entries are down 77% and alerts are acknowledged in about 2 minutes.
The credit is shared: our safety week, toolbox talks and firm action on contractor gangs did as much as the cameras.
No video leaves the plant, and the system identifies no one.
At the gate, turnaround is down 24% on camera data, with our own dispatch slots doing most of the work.
We do not claim injuries avoided; it is too early and the numbers are too small.
Suggested next step: share the approach with peers and decide together whether to extend it

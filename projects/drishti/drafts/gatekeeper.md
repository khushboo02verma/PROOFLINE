### Is this vendor safe to let in, and will I be blamed if it goes wrong?

An Indian cement manufacturer used AI on its existing security cameras to check helmets, vests and restricted zones, and later truck queues at the gate [E:e08] [E:e51].
The project ran from a first email to plant-wide use in about seven months [E:e01] [E:e60].

#### Fact sheet

| Question | Answer {framing} |
| --- | --- |
| Where does processing happen? | On edge GPU servers inside the plant's OT network; nothing runs in the cloud [E:e86] [E:e04] |
| Does any data leave the plant? | No internet egress from the servers; video stays on site [E:e86b] |
| How do alerts reach phones without images leaving? | The message carries text only; the snapshot opens on a console inside the plant network [E:e10] [E:e11] |
| How does the vendor get in? | Only through the client's jump host, session recorded, approved per session [E:e105] |
| How are updates installed? | As signed packages, installed by the client's own IT team [E:e10b] |
| How long is footage kept? | Video 30 days, alert snapshots 180 days [E:e86c] |
| Is anyone identified? | No: the system detects people and PPE, stores no face templates and identifies no one [E:e33] |
| Certifications | SOC 2 and ISO 27001; because SOC 2 covers company controls, the on-premises deployment adds a checklist mapped to ISO 27001 Annex A [E:e87] [E:e10c] |

#### How the risks were handled

IT and OT security raised three blockers before the proof of concept; each was fixed in the design and cleared in writing [E:e09] [E:e11].
A face-recognition attendance option was in the original request; corporate legal stopped it on data-protection grounds [E:e06] [E:e32] [E:e34].
The vendor removed the module from the installed software rather than switching it off, and the client's IT team verified the installed package hash [E:e35] [E:e34b].
During the pilot, a firmware update by the client's CCTV contractor cut usable video from 22 of the 40 pilot cameras for about 41 hours [E:e36].
The vendor's software still showed those cameras as connected, because it did not check that frames were actually arriving [E:e37].
Responsibility was shared in writing: root cause on the contractor's side, detection gap on the vendor's side [E:e39].
The fixes: an alarm when a camera sends no frames for 5 minutes, 24 hours' notice before any firmware change, and a daily camera health message [E:e38] [E:e38b].
No safety incident occurred during the gap [E:e37b].
Retraining used the plant's own images on a training box inside the plant, so no image left the site [E:e40] [E:e27c].
When an alert rule had to change, the client insisted it be logged openly: "I don't want hidden exceptions." [E:e54]

#### Will this vendor still be there?

The vendor's field engineer spent 61 days on site, and the team logged about 1,150 person-hours [E:e89b] [E:e89].
Every result in this case study uses the definitions the client signed before work began [E:e13c] [E:e47b].

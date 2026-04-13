# OnePoint — Product Requirements Document (PRD)

> Scope note: this document is the full research draft.  
> Active build scope is now captured in `OnePoint_PRD_MVP.md` and `OnePoint_MVP_2Week_Checklist.md`.

**Status:** Draft v0.1 · Research Input
**Source:** Synthesized from 4 call transcripts (Ali Ann × 2, AlyAnn × 2 — AlyAnn pair deduplicated as identical)
**Owner:** Jero (builder) · **Primary Stakeholder:** Ali Ann (Aly Ann)
**Date:** 2026-04-11

---

## 1. Brand Description

**OnePoint** is a voice-first, cross-surface coordination and care-logging platform built for small, non-medical caregiver teams who support aging or medically-fragile loved ones outside the formal healthcare system. It collapses the scattered reality of modern caregiving — group texts, sticky notes, spreadsheets, memory — into a single, always-on point of truth.

The product is designed around a hard-won insight: families already doing this work are *loosey-goosey* by necessity. They are not licensed, they have no EMR, and they are legally exposed the moment something goes wrong. OnePoint gives them the structure of a clinical team without forcing them to become one: one place to log, one place to hand off shifts, one place to see what's actually happening to the person they love — and, critically, one place that speaks every dialect of technology so that the sister on a flip phone is as present in the loop as the sister running Notion.

**Positioning statement:** *OnePoint is the shared brain for non-medical caregiver teams — voice-native, low-tech inclusive, medically aware, and legally defensible.*

**Why it matters:**
- ~53M unpaid family caregivers in the U.S.; the overwhelming majority coordinate by group text.
- Non-medical companions face real liability exposure without logs (a live concern from the transcripts: one stakeholder is currently defending against a threatened lawsuit, and their logs are what's saving them).
- Care recipients (e.g. dementia + Parkinson's + elevation-sensitive comorbidity) generate signal faster than a text thread can capture.
- Existing tools (EMRs, Notion, shared spreadsheets, CarePredict, CaringBridge) each solve one slice. Nothing unifies voice + web + app + research + wearables + legal record.

---

## 2. Primary Persona & Situational Context

### Ali Ann — Lead Caregiver / Team Coordinator
- Non-medical professional companion, runs a small caregiver practice.
- Works overnight shifts (drives loads at night, prefers the quiet hours).
- Coordinates care across her own family (dad, recently moved) AND a client family (Connie's family).
- Team includes multiple sisters with **mixed tech tolerance**:
  - One sister: "5G-trip" skeptical, will not use smartphone, AI, or modern apps.
  - Another sister (Kansas): no iPhone.
  - Others: comfortable with Google Sheets / Docs / Calendar.
- Self-describes as overbooked, spread thin, prone to dropping balls — explicitly wants OnePoint to be the thing that stops that from happening.

### Connie — Care Recipient (current acute case driving requirements)
- ~120 lbs, ~20 years of dementia, suspected Parkinson's progression.
- Just transitioned from one month at sea level back to Lake of the Pines (high elevation, ~1,500 ft).
- Within a week of return: ER visit, blood pressure "totally out of whack."
- Symptoms worsening: more hallucinations, less verbal/audible, weaker gait (can hold weight, a few steps), increased dementia symptoms.
- UTI already tested and ruled out at ER.
- Not currently tracking blood sugar; no wearable. Family owns a Rolex (non-smart), resistant to Apple Watch because of battery anxiety.
- No current unified log — team is coordinating Connie's care via **group text**.

### Secondary: Ali Ann's Dad
- Parkinson's, dementia-adjacent cognitive changes.
- Recently moved by Ali Ann — active, ongoing relocation project that is an **explicit constraint on Ali Ann's bandwidth** (she has said directly she cannot lose sight of it while OnePoint is being built).
- Referenced in-call as the parallel case that validates the same requirements OnePoint is being built for Connie. Ali Ann is effectively running two care operations at once.

### Tertiary: Prospective Tenant — Longmont Assisted Living Facility (PRIORITIZED GOAL)
- Ali Ann has an **active business goal**: place a qualified tenant into the assisted living facility she is associated with in **Longmont, CO**.
- This is not a side quest. It is a first-class objective of the OnePoint platform and must be treated as one of the primary use cases v0 supports.
- OnePoint should directly serve this goal through lead capture, prospective-resident intake, fit assessment, family communication, and handoff tracking (see §5.11).

---

## 3. Problem Statement

Small, non-medical caregiver teams have no tool built for them. They are forced to choose between:
1. **Consumer tools** (group text, shared spreadsheets, Notion) — no medical context, no research, no legal defensibility, and exclude low-tech family members.
2. **Clinical tools** (EMRs, HIPAA platforms) — require licensing, credentialing, and training they don't have.

The result: critical observations live in text threads that nobody can query, health trends are invisible until an ER visit, low-tech family members are silently locked out of the loop, and the team has no defensible record if a family member turns adversarial.

---

## 4. Goals & Non-Goals

### Goals
- **G1.** Replace the group text as the primary capture surface for care logs.
- **G2.** Make capture effortless — voice-first, zero typing required, hands-free friendly (one-tap record while actively caring for someone).
- **G3.** Include *every* team member regardless of device or tech comfort, down to "just give me a link in a browser."
- **G4.** Turn raw logs into medical insight via automated research agents that consult peer-reviewed sources.
- **G5.** Produce a legally defensible, timestamped audit trail that protects the caregiver.
- **G6.** Meet HIPAA where medical records are involved; be self-hostable where they aren't.
- **G7. (PRIORITIZED — business-critical for Ali Ann)** Actively drive tenant placement into the **Longmont assisted living facility**. OnePoint must directly support lead generation, prospect intake, fit assessment, family/decision-maker coordination, tour scheduling, and move-in handoff — all inside the same unified surface that handles care logs. This is the product's first revenue-adjacent goal and must ship in v0.

### Non-Goals (v1)
- Becoming an EMR. OnePoint links to and ingests from HIPAA-compliant medical record systems; it is not one.
- Replacing licensed clinical judgment. The research agent informs; it does not diagnose.
- Insurance billing, claims, or Medicare integration.
- Generic family scheduling (calendar apps already do this well).

---

## 5. Functional Requirements

### 5.1 Capture Layer — "Hit Record and Talk"
- **FR-1.** Browser-resident voice agent. User opens app/web → taps record → speaks freely; no typing required.
- **FR-2.** Vision-capable agent — can see via camera (useful for "show me this rash / this pill bottle / this blood pressure reading").
- **FR-3.** Stream-of-consciousness tolerant. Users will not speak in perfect sentences. Parsing must handle "she walked to the bathroom and then she said her back hurt and I gave her the blue one" as legitimate input.
- **FR-4.** Automatic separation of a voice log into time-stamped entries + timesheet rows (one capture, two artifacts).
- **FR-5.** Works while the caregiver is physically occupied with the patient (no modal dialogs, no typing, no tapping required beyond the initial record trigger).

### 5.2 Surface Layer — Cross-Device Inclusivity
- **FR-6.** **Native app** (iOS/Android) for the tech-comfortable team members.
- **FR-7.** **Web app** reachable via simple shared link — the low-tech-sister entry point. No install, no signup friction, no modern JS framework gymnastics. If it doesn't work on a skeptical relative's old phone, it fails the requirement.
- **FR-8.** Single shared login link; team members self-identify as "person on duty" per shift.
- **FR-9.** Dashboard shows: who's currently on duty, last N log entries, active alerts, trending vitals, latest research agent findings.

### 5.3 Research Layer — AI Medical Research Agent
- **FR-10.** **Trigger:** every log entry (live or end-of-day batch) spawns an AI research agent.
- **FR-11.** Agent reads patient history + current log + relevant medical context, then queries peer-reviewed medical journals.
- **FR-12.** Output is *cited*, verified, returned to the team as a "here's what the literature says about what you just observed."
- **FR-13.** Agent handles both directions — validates positive signs AND surfaces warning patterns (e.g. "these symptoms combined with this elevation change are associated with X in the literature").
- **FR-14.** Agent outputs are framed so that the team can bring them *to* a licensed professional — never replacing one.
- **FR-15.** Scope examples called out in transcripts: Parkinson's progression, dementia staging, UTI differential, hydration, elevation-related BP instability.

### 5.4 Biometrics & Wearables
- **FR-16.** Integrate with consumer wearables. Priority: **Oura Ring** (explicitly requested), **wristband biometric stickers / patches**, any battery-tolerant device that doesn't require daily charging.
- **FR-17.** Explicitly tolerate the "no Apple Watch" preference (battery-anxiety patients).
- **FR-18.** Data types: heart rate, HRV, sleep, blood oxygen, skin temp, activity, and — where possible — blood pressure and blood glucose (known gap in Connie's current monitoring).
- **FR-19.** Biometrics feed the same timeline as voice logs so that subjective observation and objective data sit side by side.

### 5.5 Historical Backfill
- **FR-20.** **iMessage extractor** — run locally against the Mac iMessage SQLite DB to pull prior care-related conversations.
- **FR-21.** Backfill selected by conversation / participant, not global scrape.
- **FR-22.** Requires explicit per-person consent before extraction.
- **FR-23.** Extracted messages are timestamp-preserved and merged into the OnePoint timeline as backdated log entries.

### 5.6 Visualization
- **FR-24.** Dashboard of metrics: BP trend, weight trend, sleep trend, symptom frequency, shift coverage, etc.
- **FR-25.** Timeline view combining: voice logs, text backfill, wearable data, research agent findings, and ER/clinical events.
- **FR-26.** Per-person filter (the platform supports multiple care recipients per team — Ali Ann is coordinating both Connie and her own dad).

### 5.7 Medical Records & Compliance
- **FR-27.** Link to external medical records via **HIPAA-compliant integration**. Build on an existing open-source HIPAA-compliant medical records platform (see §9 research items) — do not roll our own.
- **FR-28.** Waiver / authorization flow: family member with medical power of attorney must explicitly grant access before records ingest.
- **FR-29.** Self-hostable deployment option for teams that want to own their data end-to-end.

### 5.8 Legal Defensibility
- **FR-30.** Every log entry is immutably timestamped and attributable to a team member.
- **FR-31.** Export — on demand, the team can produce a complete, chronological, attributed care record for legal review.
- **FR-32.** This is a marquee requirement, not a footnote. The current stakeholder has **active litigation exposure**; logs are what protect her. OnePoint's defensibility story is a primary selling point to similar teams.

### 5.9 Family Communication
- **FR-33.** Integrated family video chat capability (referenced as "LifeKit" in transcripts — i.e. a private family Zoom-equivalent embedded in the platform, so video check-ins live in the same shared surface as logs).

### 5.10 Onboarding — The Spreadsheet On-Ramp
- **FR-34.** v0 experience: start from a shared spreadsheet the team already understands, and *mirror* OnePoint against it — duplicates tolerated, no forced migration, no behavior change on day one.
- **FR-35.** The spreadsheet remains editable by the team member who prefers it; OnePoint reads changes through.
- **FR-36.** Over weeks, the center of gravity moves from spreadsheet → OnePoint without ever asking the user to "stop using the spreadsheet."

### 5.11 Tenant Placement — Longmont Assisted Living Pipeline (PRIORITIZED)
This module serves Goal **G7** and is a v0 deliverable, not a future phase. It treats prospective-resident placement with the same first-class status as care logging.

- **FR-37. Facility profile.** OnePoint holds a structured profile for the Longmont assisted living facility: location, license type, levels of care offered, pricing tiers, current vacancy count, amenities, photos, staff ratio, specializations (memory care, Parkinson's, post-acute, etc.). This profile is the canonical single source of truth and is what gets shared with prospects.
- **FR-38. Public-facing facility page.** Auto-generated shareable page (link + QR) that Ali Ann can hand to a prospect's family in one motion. Mobile-friendly, no login required, same "low-tech sister" accessibility bar as the rest of the platform.
- **FR-39. Prospect intake form.** Voice-first intake (Ali Ann can capture a prospect on a phone call by hitting record) OR web form for families to self-submit. Captures: prospective resident's name, age, current care setting, diagnoses, mobility, cognitive status, care-level needs, financial qualification, decision-maker contact, urgency, preferred move-in window.
- **FR-40. Fit assessment.** Automated match between prospect needs and facility capability. Flags clear fits, clear non-fits, and edge cases that need a human conversation. Ali Ann sees a ranked inbox of qualified leads.
- **FR-41. Prospect pipeline / CRM.** Kanban-style pipeline with stages: New Lead → Qualified → Tour Scheduled → Tour Completed → Application → Deposit → Move-In Scheduled → Resident. Every stage change is timestamped and attributed (same audit trail discipline as the care log).
- **FR-42. Family decision-maker coordination.** Most placement decisions involve multiple family members who don't live together. The shared-link + role-based access model from §5.2 applies here — adult children can see tour notes, pricing, care plans, and status without installing anything.
- **FR-43. Tour scheduling.** In-app tour booking (virtual or in-person), calendar hold, automated reminders, post-tour follow-up prompts for Ali Ann.
- **FR-44. Move-in handoff into care logging.** The moment a prospect becomes a resident, their OnePoint record transitions seamlessly from the placement pipeline into the care-log system. Their intake notes, diagnoses, and family contacts pre-populate the care record. **No re-entry of data.** This is the core integration that justifies building placement and care logging inside the same product instead of bolting on a separate CRM.
- **FR-45. Referral source tracking.** Where did each lead come from (family referral, discharge planner, website, word of mouth, geriatric care manager, facility marketing, etc.)? Enables Ali Ann to invest in channels that actually produce move-ins.
- **FR-46. Compliance fields.** Placement-specific regulatory fields: physician's report / 602 (CA) or equivalent (CO), TB test, POLST, responsible party, financial attestation. OnePoint tracks which docs are collected and which are outstanding per prospect.
- **FR-47. Occupancy dashboard.** At-a-glance view of current vacancies, upcoming move-ins, move-out risk, and lead funnel health. This is Ali Ann's business-operations view for the Longmont facility.
- **FR-48. Urgency routing.** Hospital discharge placements are time-critical (sometimes 24–72 hours). OnePoint marks urgent leads and surfaces them ahead of general inbox items, with SLA tracking.

---

## 6. Non-Functional Requirements

- **NFR-1.** **Accessibility:** WCAG AA minimum. Must work on low-spec Android, older iPhones, and desktop browsers of any vintage.
- **NFR-2.** **Offline tolerance:** voice capture must survive network loss (record local, sync when available). Caregivers work in homes, cars, rural areas.
- **NFR-3.** **Latency:** voice record → log entry visible to team in <10 seconds under normal network conditions.
- **NFR-4.** **Privacy:** end-to-end encryption of logs at rest; self-host option for teams that want full data sovereignty.
- **NFR-5.** **HIPAA:** compliance required *only* on the medical-records branch of the system; non-medical logs have a lower bar but should meet the same standard by default.
- **NFR-6.** **Reliability:** this is a system of record. Data loss is a P0 bug.
- **NFR-7.** **Minimal-friction auth:** shared link + pick-your-name should be sufficient for the low-tech sister. Heavier auth only where compliance requires it.

---

## 7. User Stories (Prioritized)

### P0 — v0 Must-Haves
1. As Ali Ann, I open OnePoint, tap record, talk about what happened on shift, and hang up — the log is saved, timestamped, and visible to my sisters in under a minute.
2. As the low-tech sister, I click a link in a text message, see today's log in a plain web page, and know who's on duty right now.
3. As any team member, I see a running timeline of everything that's happened with Connie this week.
4. As Ali Ann, I can export every log entry from the last 90 days as a timestamped, attributed document if someone threatens legal action.
5. **As Ali Ann, I can capture a prospective Longmont tenant by voice during a phone call, see their fit score against the facility, share a mobile-friendly facility page with the decision-making family, move them through a tour → move-in pipeline, and have their record automatically become a OnePoint care log the day they move in. (G7 — tenant placement, business-critical.)**
6. **As a prospective resident's family member, I receive a link, view the Longmont facility, book a tour, and message Ali Ann — without installing anything or creating an account.**

### P1 — v0.5
7. As any team member, after I log an unusual symptom, an AI research agent comes back within minutes with cited findings from medical literature relevant to what I just observed.
8. As Ali Ann, I import historical iMessage conversations about Connie so the timeline starts in the past, not today.
9. As the team, we see BP / weight / sleep trends on a dashboard.
10. As Ali Ann, I see an occupancy dashboard for the Longmont facility — current vacancies, upcoming move-ins, lead funnel health — so I can run the facility as a business.
11. As Ali Ann, I tag urgent hospital-discharge placement leads and they rise to the top of my inbox with SLA tracking.

### P2 — v1
12. As the family, we link Connie's actual medical records (with authorization) so the OnePoint timeline includes ER visits and labs.
13. As Ali Ann, I connect Connie's Oura ring (or equivalent) and see biometrics alongside our logs.
14. As the family, we hold a private video check-in inside OnePoint itself.
15. As Ali Ann, I track referral sources for every Longmont lead and know which channels produce actual move-ins.

---

## 8. Open Questions

- **OQ-1.** Which open-source HIPAA-compliant medical records platform do we build on? (Candidates: OpenMRS, Medplum, OpenEMR — see research items.)
- **OQ-2.** What is the legal status of a non-medical companion using AI-assisted research findings in their care decisions? Does OnePoint need disclaimers at the point of display?
- **OQ-3.** Oura (and similar) APIs are consumer-grade; do they provide the data density we need, or do we need to also support clinical-grade devices?
- **OQ-4.** iMessage extraction is macOS-local. What's the equivalent for Android/SMS families?
- **OQ-5.** Does the "low-tech sister" web surface need SMS fallback for alerts, since she may not check a web link proactively?
- **OQ-6.** Pricing model: per-team subscription? Per-care-recipient? Free with self-host paid upgrade?
- **OQ-7.** Multi-tenant vs single-team-per-instance — affects self-host story.

---

## 9. Research Items (for further investigation)

1. **HIPAA-compliant open source medical platforms** — comparative evaluation of OpenMRS, Medplum, OpenEMR, HAPI FHIR. Criteria: HIPAA out of the box, modern stack, active community, license compatible with commercial use, extensible for our log layer.
2. **Non-medical caregiver liability** — state-by-state landscape (priority: CA for Connie, CO for Longmont facility). What records are considered admissible and protective?
3. **Medical research retrieval** — PubMed API, Europe PMC, Semantic Scholar, OpenAlex. Which gives the best combination of journal coverage, citation metadata, and rate limits for a per-log-entry trigger pattern?
4. **Wearables for elderly / dementia / battery-averse users** — Oura (6-day battery), Whoop, Withings ScanWatch, wristband BP cuffs, CGMs, patch biosensors. Integration cost vs data value.
5. **Browser-resident voice + vision agents** — evaluate: realtime transcription APIs, on-device models (Gemma, Whisper.cpp), WebRTC capture flows. Match to offline tolerance NFR-2.
6. **iMessage extraction tooling** — existing libraries, privacy considerations, consent UX pattern.
7. **Competitive landscape (care logging)** — CareZone, Lotsa Helping Hands, CaringBridge, Cariloop, Ianacare, CarePredict. Where does each fall short for *non-medical professional companion teams*?
8. **Shared-link auth patterns for low-tech users** — magic links, passphrase, device-bound tokens. Need the minimum viable auth that still holds up for a legal record.
9. **Reimbursement / insurance angles** — is there any path where non-medical caregiver logs become billable or qualify the family for respite care programs?
10. **Naming & trademark** — clearance search on "OnePoint" in health/caregiver space.
11. **Colorado assisted living regulatory landscape** — CDPHE licensing, Assisted Living Residence (ALR) requirements, admission criteria docs, required pre-admission records, POLST, 602 equivalents, TB testing, physician attestations. What must OnePoint's Longmont placement pipeline capture to stay inside the regulatory fence?
12. **Longmont, CO senior-care market intel** — local competitors, median price per level of care, occupancy rates, typical referral sources (hospitals, discharge planners, geriatric care managers, A Place for Mom, Caring.com, local social workers). What does a qualified lead pipeline actually look like in this market?
13. **Assisted living lead generation channels** — A Place for Mom, Caring.com, local SEO, Google Business Profile, geriatric care manager networks, hospital discharge relationships, Alzheimer's Association chapters, Meals on Wheels networks, elder law attorneys. Which are worth integrating with vs. just tracking?
14. **Competitive landscape (placement CRMs)** — Enquire, Yardi Senior Living Suite, ECP Lead Cloud, Sherpa, Aline (Glennis). Where do they over-serve large chains and under-serve owner-operated small facilities like Ali Ann's?
15. **Referral fee & anti-kickback compliance** — what's legal in CO for senior living referral arrangements (vs. federal anti-kickback rules that apply to SNFs)? Affects how referral source tracking can be monetized.
16. **Facility marketing asset generation** — AI-generated virtual tours, photo enhancement, copywriting for facility pages. Low-effort ways to make the Longmont facility page feel premium without a marketing team.
17. **Hospital discharge workflow** — who are the actual humans (case managers, social workers, discharge planners) who need to receive a OnePoint link to place a patient in 48 hours? What format do they want?

---

## 10. Constraints & Context (from transcripts)

- **Ali Ann's bandwidth** is actively constrained by her own dad's recent move (she moved him herself and cannot lose sight of him). The build cadence must respect this — Ali Ann will be reachable in chunks, not full days, and OnePoint must be usable in the gaps between her dad's needs and Connie's shifts.
- A working spreadsheet already exists between Jero and Ali Ann; it "broke when the gear got off" and was never fully adopted. v0 should revive and mirror this spreadsheet, not replace it.
- A synchronous working session is planned ("Saturday night, 7pm-ish, in person") to lay out the v0 requirements with Ali Ann directly. This PRD should be the input to that session.
- The acute case (Connie's elevation transition + ER visit) is happening *this week*. Time-to-useful matters more than feature completeness.
- The current legal-threat scenario makes defensible logging a *today* problem, not a future compliance checkbox.
- **The Longmont assisted living facility needs a tenant now.** Tenant placement is not future work — it is a co-equal v0 goal alongside care logging. Every week without a move-in is lost revenue for Ali Ann and lost momentum for the platform.

---

## 11. Success Metrics (v0)

- **SM-1.** Ali Ann logs at least one voice entry per shift for 14 consecutive days without prompting.
- **SM-2.** At least 2 of Ali Ann's sisters have viewed the web surface at least once per week for 4 consecutive weeks.
- **SM-3.** The group text thread volume for Connie's care drops by ≥50% (measured before/after migration).
- **SM-4.** An exportable, attributed, timestamped log of the last 30 days can be produced in <60 seconds, on demand.
- **SM-5.** At least one AI research agent finding per week is reviewed and marked useful by a team member.
- **SM-6. (G7 — tenant placement, headline metric)** **At least one qualified tenant moves into the Longmont assisted living facility through OnePoint within 60 days of v0 launch.**
- **SM-7.** At least 5 qualified prospect leads enter the Longmont pipeline in the first 30 days.
- **SM-8.** At least 2 tours are scheduled through the platform in the first 30 days.
- **SM-9.** Median time from "new lead" to "tour scheduled" is under 72 hours.

---

## 12. Appendix — Source Transcript Summary (deduplicated)

Four transcripts analyzed. `AlyAnn.transcript.txt` and `AlyAnn 2.transcript.txt` were byte-equivalent duplicates of the same call and counted once.

- **Call 1 (Ali Ann · logistics):** accessibility for low-tech sisters, spreadsheet revival, in-app voice agent for Connie's time sheets + notes, session scheduling.
- **Call 2 (Ali Ann · basics):** voice-operated daily notes, app + web parity, browser-resident agent with vision, low-tech sister as a hard constraint.
- **Call 3 (AlyAnn · clinical + legal):** Connie's acute medical transition, AI research agent spec, wearables (Oura), iMessage backfill, HIPAA medical records via open-source platform, legal defensibility via logs, active litigation context.

All four calls point at a single coherent product. This PRD is that product.

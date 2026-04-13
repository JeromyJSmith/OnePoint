# 40 — System Architecture

**Status:** v1 · Architecture Output
**Date:** 2026-04-11
**Author:** SYSTEM_ARCHITECT_AGENT
**Inputs:** `OnePoint_PRD.md`, `research/10_skill_landscape.md`, `research/11_oss_landscape.md`

---

## Summary

OnePoint is a docker-compose of seven OSS systems wired together by a thin TypeScript gateway: Medplum is the FHIR system of record for every person, log, and clinical event; Krayin CRM is the placement pipeline that funnels prospects into Medplum on move-in day; LiveKit Agents is the voice+vision capture layer that writes FHIR `Observation` and `Communication` resources via LangGraph agents; Better-Auth provides magic-link login and HTMX server-rendered pages provide the low-tech-sister surface; Europe PMC + OpenAlex back the research agent, Gotenberg emits legal-grade PDF exports, and pgvector+mem0 hold agent memory. Custom engineering is restricted to four small surfaces — the Medplum↔Krayin bridge, the HTMX low-tech pages, the spreadsheet-mirror sync, and a ~50-line SHA-256 hash chain over Medplum AuditEvent — because every other line of code is already OSS we didn't write.

---

## Architectural Principles

1. **OSS first, integration glue second, custom code last.** If an OSS project covers 80% of a feature, we extend it. We never rebuild what Medplum, Krayin, LiveKit, or Better-Auth already ship.
2. **Every data write is also an audit event.** All writes pass through Medplum; Medplum emits FHIR `AuditEvent` + `Provenance` automatically; a hash-chain table makes the sequence tamper-evident. There is no "quiet write" path.
3. **Voice is the primary capture modality.** The UI assumes someone is holding another human with one arm and a phone in the other. Typing is the fallback, not the default.
4. **The low-tech web surface is a first-class requirement, not a compat layer.** The HTMX surface is built first, on its own code path, and is deploy-tested against an old Android browser before anything else ships. React Native comes later and layers on top.
5. **Move-in handoff is a data-flow, not a feature — it's baked into the schema.** A Krayin prospect carries a `medplum_patient_id` stub from the moment fit-assessment passes. Move-in is an event that flips ownership, not a migration job.
6. **Medplum is the eventual source of truth for the person.** Once a prospect becomes a resident, Medplum owns identity, clinical data, contacts, and consent. Krayin retains the sales-pipeline history (stage transitions, tour notes, referral source) but stops being asked about the person.
7. **Self-host by default, cloud when needed.** v0 runs on a single Mac mini / Hetzner box via docker-compose. HIPAA-cloud is an opt-in deployment, not a prerequisite to shipping.
8. **Legal defensibility is day-one, not phase-two.** The hash chain, AuditEvent, and export path must work on the day Ali Ann records her first voice log — because that is the day she may need to produce it.

---

## System Diagram (ASCII)

```
                            ┌─────────────────────────────────────────────────┐
                            │                    DEVICES                     │
                            │                                                 │
   Ali Ann (iPhone)  ──┐    │   Low-tech sister (any browser)                 │
   React Native shell  │    │   Magic link → plain HTML page                  │
                       │    │                                                 │
   Prospect family     │    │   Hospital discharge planner                    │
   (web link, no acct) │    │   (link only, form submit)                      │
                       ▼    │                                                 │
                       ┌────┴─────────────────────────────────────────────────┐
                       │                  EDGE / AUTH                         │
                       │  Better-Auth  (magic link, shared-link, role bind)   │
                       │  Caddy/nginx  (TLS, routing)                         │
                       └────┬─────────────────┬─────────────────┬─────────────┘
                            │                 │                 │
          ┌─────────────────▼───┐  ┌──────────▼────────┐  ┌─────▼──────────────┐
          │  CAPTURE LAYER      │  │  HTMX WEB SURFACE │  │  NATIVE APP API    │
          │  LiveKit Server     │  │  (server-rendered │  │  (thin TS gateway) │
          │  LiveKit Agents     │  │   Fastify + HTMX) │  │  Fastify           │
          │  whisper.cpp (fall- │  │  ← low-tech sister│  │  ← iOS/Android     │
          │   back, offline)    │  │  ← prospect forms │  │                    │
          └──────────┬──────────┘  └──────────┬────────┘  └─────────┬──────────┘
                     │                        │                     │
                     │                        │                     │
                     ▼                        ▼                     ▼
          ┌──────────────────────────────────────────────────────────────────┐
          │                  ONEPOINT GATEWAY (TS / Fastify)                 │
          │   - session + role from Better-Auth                              │
          │   - routes capture → LangGraph  → Medplum                        │
          │   - routes prospect → Krayin    → Medplum (on move-in)           │
          │   - signs every write into the hash chain                        │
          └──────┬─────────────────┬─────────────────────┬──────────────────┘
                 │                 │                     │
                 ▼                 ▼                     ▼
          ┌─────────────┐   ┌──────────────┐      ┌──────────────┐
          │  LangGraph  │   │   Medplum    │      │  Krayin CRM  │
          │  (research  │◄──┤  FHIR Server │◄────►│  (Laravel)   │
          │   agent)    │   │  + Bots      │ webhk│  tenant      │
          │  mem0       │   │  + AuditEv   │      │  pipeline    │
          │  pgvector   │   │  + Provenance│      │              │
          └──────┬──────┘   └──────┬───────┘      └──────┬───────┘
                 │                 │                     │
                 ▼                 ▼                     ▼
          ┌────────────────────────────────────────────────────┐
          │                 PostgreSQL 15                      │
          │   medplum db │ krayin db │ pgvector │ hash_chain   │
          └────────────────────────────────────────────────────┘
                 ▲                 ▲                     ▲
                 │                 │                     │
          ┌──────┴──────┐    ┌─────┴──────┐       ┌──────┴───────┐
          │ Europe PMC  │    │ Gotenberg  │       │  Oura API    │
          │ OpenAlex    │    │ (HTML→PDF  │       │  (biometric  │
          │ (research)  │    │  legal exp)│       │   ingest)    │
          └─────────────┘    └────────────┘       └──────────────┘
```

Every box is a named, real, OSS product. No mystery components.

---

## Component Inventory

| Component | Role | OSS? | Build or Reuse | License | Risk |
|---|---|---|---|---|---|
| Medplum | FHIR system of record, auth plumbing, Bots runtime, AuditEvent, Provenance | Yes | Reuse (self-host Community) | Apache 2.0 | Dev velocity depends on a project we don't control; migration cost is high if we outgrow it |
| Krayin CRM | Placement pipeline (leads → move-in), kanban, custom fields, web forms | Yes | Reuse + extend (custom pipeline stages, custom fields for CO ALR compliance) | MIT | PHP/Laravel stack sits outside our TS monoculture; integration via webhooks only |
| LiveKit Server + Agents | Voice capture, vision, telephony, family video (FR-33) | Yes | Reuse | Apache 2.0 | Server infra burden; partially mitigated by LiveKit Cloud as fallback |
| whisper.cpp | On-device / offline transcription fallback | Yes | Reuse | MIT | None material |
| LangGraph | Research agent orchestration, per-log trigger, durable state | Yes | Reuse | MIT | Learning curve; agent drift mitigated with eval harness |
| mem0 | Per-care-recipient long-term agent memory | Yes | Reuse | Apache 2.0 | None material |
| pgvector | Embeddings store inside the same Postgres as Medplum | Yes | Reuse | PostgreSQL License | None |
| Better-Auth | Magic-link auth, session, role binding | Yes | Reuse | MIT | Newer project, 27.8k stars — watch for breaking changes |
| HTMX + Fastify server-rendered templates | Low-tech sister surface, prospect forms, facility page | Yes | Build thin, on HTMX | BSD-2 | None — this IS the boring path |
| Gotenberg | HTML → PDF legal export | Yes | Reuse (docker container) | MIT | None |
| Europe PMC REST | Medical literature primary | Yes (public API) | Reuse | Open terms | Rate-limit variance; cache aggressively |
| OpenAlex API | Citation graph / topic enrichment | Yes (public API) | Reuse | CC0 | None |
| Twilio (SMS) | Low-tech-sister alert fallback (OQ-5) | No (SaaS) | Reuse via adapter interface | Commercial | Vendor dependency; mitigated by adapter pattern |
| Oura API | Biometric ingest v0 | No (SaaS) | Reuse | Commercial | Consumer-grade SLA; acceptable for v0 |
| **OnePoint Gateway** | Route auth → capture → LangGraph → Medplum → hash chain | **No — custom** | **Build** | proprietary | Smallest surface possible; mostly passthrough |
| **Medplum↔Krayin Bridge** | Event-driven bidirectional sync of prospect ↔ patient | **No — custom** | **Build** | proprietary | Single most load-bearing custom component; see integration section |
| **Hash chain** (~50 LOC) | Tamper-evident sequence over AuditEvent | **No — custom** | **Build tiny** | proprietary | Small, well-scoped |
| **Spreadsheet mirror** | Google Sheets ↔ Medplum bidirectional (FR-34..36) | **No — custom** | **Build small** | proprietary | Conflict handling is the hard part |
| **iMessage backfill** | Local `chat.db` reader + consent UX (FR-20..23) | **No — custom** | **Build small** | proprietary | macOS-only; Android is a v1 problem |
| **Wearable adapters** | Oura v0, patch sensors / BP cuffs later | **No — custom** | **Build per-device** | proprietary | Unbounded surface — strictly Oura-only in v0 |

---

## Data Flow: Voice → Care Log

**Goal:** Ali Ann taps record, talks for 90 seconds, hangs up. Within 10 seconds the sisters see the entry.

```
t=0.0s   Ali Ann opens OnePoint (native app OR HTMX page) and taps "Record".
t=0.2s   Better-Auth session cookie validated → role "caregiver" resolved
         → patient context ("Connie") taken from URL or active-shift record.
t=0.3s   Browser opens WebRTC to LiveKit Server. If network is weak, whisper.cpp
         WASM falls back to local capture; the audio is queued locally and
         synced on reconnect (NFR-2).
t=0.5s   LiveKit Agent starts streaming STT (whisper-large-v3 on server, or
         local whisper.cpp offline). Partial transcripts stream back to UI.
t=60s    Ali Ann stops talking. The agent receives the final transcript.
t=60.1s  LangGraph "capture_parse" node runs over the transcript. It uses the
         `data-context-extractor` pattern to split the stream-of-consciousness
         into (a) time-stamped narrative log entries and (b) timesheet rows
         (FR-3, FR-4).
t=60.5s  Gateway writes to Medplum via the FHIR REST API:
           - 1× Encounter (class=home, period={start..end of recording})
           - N× Observation (one per vital / symptom mention, loinc-coded
             where possible, free-text otherwise)
           - 1× Communication (the full narrative, with the raw audio URL
             attached as a Communication.payload content reference)
           - 1× DocumentReference (the verbatim transcript, immutable)
           - 1× Provenance (author=Ali Ann, agent=LiveKit+LangGraph)
           - 1× AuditEvent (autogenerated by Medplum on every write)
t=60.6s  Gateway computes SHA-256 over (prev_hash || resource_ids || ts ||
         author_id) and appends a row to `hash_chain`. This is what makes
         the sequence tamper-evident without a second database.
t=60.7s  Medplum Bot "on_new_observation" fires → posts a message onto a
         LangGraph queue (research-agent trigger; see research flow).
t=60.8s  Gateway pushes an SSE event to all connected sisters' pages. HTMX
         hx-sse swap re-renders the timeline row for Connie.
t=61s    Sisters see: "Ali Ann · just now · 'walked to bathroom, said back
         hurt, gave 1 Tylenol' · audio ▶". Done.
```

**What the family sees:** one new row in the timeline, attributed, with a playback button and a "what the research agent found" chip that fills in a few minutes later.

---

## Data Flow: Prospect → Move-In → Care Log (THE WEDGE)

**This is the most important data flow in OnePoint. It is the reason Krayin and Medplum live in the same product.**

```
STAGE 1 — LEAD CAPTURE (Krayin owns)
────────────────────────────────────
A. Discharge planner or family clicks the facility link (FR-38) OR
   Ali Ann hits "record" during a phone call with a prospect family
   and speaks the intake (FR-39).

B. HTMX form POST / LiveKit voice-intake agent → Gateway → Krayin REST API.
   Creates a Krayin Lead with custom fields:
     - prospect_name, age, current_setting
     - diagnoses[], mobility, cognition, care_level
     - decision_maker_contact (name, phone, email)
     - urgency ("routine" | "hospital_discharge_48h")
     - preferred_move_in
     - referral_source
     - medplum_patient_id    ← NULL at this stage
   Lead lands in stage "New Lead".

C. LangGraph "fit_assessment" agent runs:
     - pulls facility profile (vacancies, levels of care, specializations)
     - scores prospect against capability matrix
     - writes a fit_score (0..1) and fit_notes back onto the Lead
     - promotes to "Qualified" or flags for human review.

STAGE 2 — SHADOW PATIENT (the critical move)
─────────────────────────────────────────────
D. The first time a Lead reaches stage "Qualified", the Bridge creates
   a Medplum FHIR Patient in state "prospective":
     - Patient.active = false
     - Patient.meta.tag = [{ system: "onepoint", code: "prospective" }]
     - identifier = { system: "krayin-lead", value: <lead_id> }
     - name, birthDate, contact[] (family decision makers)
     - extension[onepoint-fit-score] = fit_score
   The new Patient.id is written back into Krayin as medplum_patient_id.

   Why now, not at move-in: creating the shadow Patient at the Qualified
   stage means fit notes, tour observations, and pre-admission documents
   can ALREADY be attached to the Medplum record as the prospect moves
   through the pipeline. Zero re-entry on move-in day — the record is
   already there, we just flip a flag.

E. As the lead progresses through Krayin stages (Tour Scheduled → Tour
   Completed → Application → Deposit → Move-In Scheduled), each stage
   transition fires a Krayin webhook → Gateway → Medplum:
     - Tour notes → Communication resource (attached to Patient)
     - 602 / POLST / TB / physician's report → DocumentReference
     - Financial attestation → Consent resource
     - CarePlan draft begins to assemble from fit assessment + intake

STAGE 3 — MOVE-IN DAY (Medplum takes ownership)
────────────────────────────────────────────────
F. Krayin stage flips to "Resident".  Webhook fires.
   Bridge runs a single transactional update on Medplum:
     - Patient.active = true
     - Patient.meta.tag = [{ system: "onepoint", code: "resident" }]
     - Encounter created (class=residential, status=in-progress,
       period.start = move-in timestamp)
     - CarePlan.status = active
     - Provenance records the transition with author = Ali Ann
     - AuditEvent records the state change

G. From this point on:
     - Medplum is the source of truth for the person
     - Krayin retains the sales pipeline history (stage transitions, tour
       notes, referral source analytics) but is no longer queried for
       clinical state
     - The patient appears in Ali Ann's care-log timeline automatically,
       alongside Connie
     - All of §"Data Flow: Voice → Care Log" now applies to them

H. Krayin's occupancy dashboard (FR-47) reads from both sides:
     - Vacancies: Krayin (leads in pipeline)
     - Current residents: Medplum (Patient.active && tag=resident)
     - Move-out risk: Medplum (clinical signals from Observations)
   Exactly one query joins the two systems, inside the Gateway.
```

**Why this is the wedge:** a spreadsheet or a standalone CRM would force double-entry on move-in day, which is always chaos. Creating the shadow Medplum Patient at "Qualified" stage means that every tour note, pre-admission document, and family conversation is already in the care record by the time the person walks through the door. Ali Ann's hands stay free.

---

## Integration: Medplum ↔ Krayin

This is the hardest single piece of the architecture. Two systems, two databases, two stacks (TypeScript vs Laravel), two auth models. Here is how we make them coherent.

### Topology

```
Krayin (PHP/Laravel)  ←─ webhook ──►  OnePoint Gateway (TS)  ◄── Bot ─►  Medplum
         │                                      │                         │
         └─ krayin DB (Postgres) ◄──────────────┼──────────► medplum DB (Postgres)
                                                ▼
                                          hash_chain
```

Both apps run in the same docker-compose, both use the same Postgres instance (separate logical databases), and both talk exclusively through the Gateway. Neither is ever allowed to write directly to the other's DB.

### Source-of-truth rules (non-negotiable)

| Field | Owner while prospect | Owner after move-in |
|---|---|---|
| prospect_name, contact, family | Krayin | **Medplum** (Patient.name, Patient.contact) |
| diagnoses, mobility, cognition | Krayin (lead fields) | **Medplum** (Condition resources) |
| care_level, fit_score | Krayin | Krayin (historical); Medplum CarePlan supersedes |
| pipeline stage history | **Krayin (forever)** | **Krayin (forever)** |
| tour notes | Krayin + mirrored to Medplum Communication | **Medplum** (Communication) |
| compliance docs (602/POLST/TB) | Krayin + mirrored to Medplum DocumentReference | **Medplum** (DocumentReference) |
| vacancies, occupancy projections | **Krayin** | **Krayin** |
| voice logs, biometrics, research findings | N/A | **Medplum** |
| referral_source, SLA, channel attribution | **Krayin** | **Krayin** |

### Identity

`krayin.leads.medplum_patient_id` and `Medplum.Patient.identifier[system="krayin-lead"]` are the two halves of the bridge. Either side can resolve the other in one query.

### Consistency

Event-driven, eventually consistent, with a reconciliation job every 15 minutes:
1. Writes go through the Gateway. The Gateway persists to the primary owner first, then fires a change event to the mirror.
2. Krayin webhook → Gateway → Medplum bot invocation (synchronous within the Gateway).
3. Medplum bot → Gateway → Krayin REST API (async, queued).
4. A nightly reconciliation job walks all `resident`-tagged Patients and all Krayin leads with `medplum_patient_id` and diffs the canonical fields. Divergences emit an AuditEvent and a Gateway alert.

### Failure modes

- **Krayin down:** voice capture still works, timeline still works, existing residents unaffected. New prospect intake queues to disk and replays.
- **Medplum down:** voice capture fails gracefully (records to local whisper.cpp and queues). Krayin pipeline still works for already-qualified leads. Move-in transitions are blocked (correctly — we refuse to create a resident we can't write to the system of record).
- **Webhook dropped:** reconciliation job catches it within 15 minutes.
- **Split-brain on a field:** Medplum wins for any person tagged `resident`; Krayin wins for any lead in a non-resident stage. Ownership flip is a single atomic event.

---

## Auth & Access Control

**Stack:** Better-Auth for sessions + magic links. Single shared link per team is the default; a per-person upgrade is available but not required.

### Role model

| Role | How it's assigned | What they can do |
|---|---|---|
| `caregiver_lead` | Invited by founder, verified via Medplum Practitioner | Full R/W on a specific patient + team; can trigger legal export |
| `caregiver_team` | Magic-link join via team invite link | R/W on logs they author; R on whole team timeline |
| `family_lowtech` | Magic link from SMS/email, optionally frictionless device-bound token | Read-only on timeline, write on Communication only (ask questions), no medical records access |
| `family_medical_poa` | Magic link + signed FHIR Consent resource uploaded | Read on Medplum clinical data (labs, ER, linked records) |
| `prospect_family` | Public link, no account; optional form-submit token | Read facility page, submit intake, view their own lead status |
| `discharge_planner` | Public link + optional magic link for follow-up | Submit urgent lead, track its status |

### Low-tech sister flow (this is the whole point of NFR-7)

1. Ali Ann taps "Invite sister" in the app.
2. Gateway generates a magic link with a 90-day rolling token bound to that sister's identity-stub.
3. Sister clicks the link in a text message.
4. Better-Auth sets a cookie; Gateway resolves the stub to a `family_lowtech` role.
5. Sister lands on an HTMX page: today's log, who's on duty, a big record button. No signup, no password, no app install. Ever.
6. On new device, a new magic link is sent to the number/email already on file.

### Medical POA consent (FR-28)

1. Family member uploads the POA document via HTMX form.
2. Gateway stores it as a Medplum `DocumentReference` and creates a `Consent` resource binding that person's identity to `Patient.id` with scope "patient-privacy" and purpose "treatment".
3. Until the `Consent` resource is flipped to `active` by `caregiver_lead` after review, the member's access is unchanged.
4. After activation, the member's magic link unlocks the medical-records view on the timeline.

---

## Research Agent Architecture

**Framework:** LangGraph graph, triggered per Medplum Observation (live) + end-of-day batch.

### Graph structure

```
                ┌─────────────────┐
                │ trigger_on_obs  │  ← Medplum Bot, HTTP POST
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │  load_context   │  ← pull last 30d of Observations,
                │  (mem0)         │     Conditions, Communications for patient;
                └────────┬────────┘     retrieve related prior findings from pgvector
                         │
                ┌────────▼────────┐
                │  symptom_extract│  ← LLM extracts structured symptom set
                │  (LLM)          │     from the new observation + context
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │  literature_search │  ← parallel queries to Europe PMC + OpenAlex
                │  (tool nodes)      │     + PubMed fallback; scope-aware (Parkinson's,
                └────────┬───────────┘     dementia, elevation-BP, UTI, etc.)
                         │
                ┌────────▼────────┐
                │  rank_and_cite  │  ← rerank by relevance to Connie's context,
                │  (LLM + mem0)   │     dedupe, cite
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │ frame_for_team  │  ← "here's what the literature says about
                │  (LLM)          │     what you observed — bring this to
                └────────┬────────┘     Connie's doctor" (FR-14 framing rule)
                         │
                ┌────────▼────────┐
                │ write_to_medplum│  ← creates a Medplum `ClinicalImpression`
                │  (FHIR client)  │     with citations as `evidence[]`
                └────────┬────────┘     + AuditEvent + hash_chain append
                         │
                ┌────────▼────────┐
                │  notify_surface │  ← SSE push to timeline; shows up as a
                │                 │     "research finding" chip under the
                └─────────────────┘     triggering observation
```

### Trigger mechanism

Medplum Bots support pattern: `on create Observation where subject = Patient/<tagged-resident>`. The bot is a ~20-line TS function that POSTs to the LangGraph runner with the resource bundle. Batch mode runs at 22:00 local with a `last N observations + all today's voice logs` payload.

### Memory

mem0 holds three tiers: per-patient (long-term symptom history), per-agent (research strategies that worked/failed for similar cases), per-session (current reasoning chain). pgvector stores embeddings for all three.

### What the family sees

A new row appears under the triggering log entry: "Research agent found 3 relevant findings — tap to read." The tap opens a plain HTML page with summary + cited links to Europe PMC articles. Always framed as "bring this to a licensed professional" per FR-14.

---

## Legal-Grade Audit Trail

**The core claim:** every log entry is immutable, attributed, timestamped, and verifiably sequenced.

### What Medplum gives us for free

- **Provenance resource** on every write: who, what, when, with what agent.
- **AuditEvent resource** on every read/write/update: full audit trail per FHIR standard.
- **Immutable by policy:** Medplum supports `history` on every resource; deletes are soft and logged.
- **HITRUST / SOC2 / HIPAA**: Medplum Community self-host, with disciplined deployment, inherits the compliance posture of the upstream project.

### What we add (the ~50-line hash chain)

```sql
CREATE TABLE hash_chain (
  seq           BIGSERIAL PRIMARY KEY,
  prev_hash     BYTEA NOT NULL,
  resource_ids  TEXT[] NOT NULL,
  author_id     UUID NOT NULL,
  written_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  hash          BYTEA NOT NULL
);
-- hash = sha256(prev_hash || resource_ids || written_at || author_id)
```

The Gateway appends one row per write. Any tamper of a historical Medplum resource breaks the chain because the recomputed hash won't match. Export (below) renders the full chain with a verification page.

### Export pipeline (FR-31, SM-4)

1. `caregiver_lead` requests an export: "last 90 days for Connie".
2. Gateway queries Medplum for all resources where `subject = Patient/Connie` and `meta.lastUpdated >= now() - 90d`.
3. Gateway joins with `hash_chain` and renders a single HTML document: chronological log, attributed, with a verification table at the end.
4. HTML → Gotenberg → signed PDF/A (Gotenberg's PDF/A + watermark profile).
5. Result: one PDF, downloadable in under 60 seconds, that a lawyer can take to court.

### Why it holds up

- **Immutability**: FHIR history + soft-delete.
- **Attribution**: Provenance + AuditEvent + the Better-Auth session ID baked into the author_id.
- **Sequence integrity**: the SHA-256 chain.
- **Reproducibility**: anyone with read access can rebuild the same PDF and compare the hash.
- **Stack pedigree**: "We used Medplum, which is HITRUST / SOC2 / HIPAA certified." is a lot stronger than "we built our own."

---

## Biometric Ingest (Oura first)

**v0 surface: Oura only.** FR-16 lists patch sensors, wristband BP, CGMs; none ship in v0 unless a specific care recipient actually owns one.

### Flow

```
Oura cloud  ──OAuth2──►  Gateway (scheduled pull every 15m)
                              │
                              ▼
                   FHIR Observation resources
                   (category=vital-signs, code=LOINC)
                   subject = Patient/<connected>
                              │
                              ▼
                          Medplum
                              │
                              ▼
                   Timeline merge with voice logs
```

Mapping:
- Heart rate → `Observation LOINC:8867-4`
- HRV → `Observation LOINC:80404-7`
- Sleep duration → `Observation LOINC:93832-4`
- SpO2 → `Observation LOINC:59408-5`
- Skin temp → `Observation LOINC:8310-5`
- Activity → `Observation` custom code under `onepoint.activity`

Every pull is a single Gateway job that de-dupes against `identifier = oura:<reading_id>`. New readings trigger the same research-agent pipeline as a voice log would. A sudden overnight BP/HR deviation next to Connie's elevation transition is exactly the pattern FR-13 wants us to catch.

### v0 constraint

The family already said they don't want an Apple Watch. Oura is the ask. If a family member doesn't wear one, biometric ingest is a no-op and the timeline just runs on voice logs — the architecture degrades gracefully.

---

## Deployment Topology

### v0 Self-host (single node, docker-compose)

```
Host: Mac mini M2 (Jero's home) OR Hetzner CAX31 ARM
OS:   Ubuntu 24.04 LTS (or macOS for local)
CPU:  arm64 throughout
RAM:  16 GB minimum
Disk: 256 GB NVMe (Postgres + audio blobs + PDFs)

docker-compose.yml services:
  postgres           (single Postgres 15, multiple logical DBs)
  medplum-server
  medplum-app        (admin UI, not exposed publicly)
  krayin-app         (Laravel + nginx)
  livekit-server
  livekit-agents
  gateway            (TS / Fastify — our thin custom layer)
  web                (HTMX surface, served by gateway)
  langgraph-runner
  gotenberg
  caddy              (TLS, domain routing)
```

Single `.env` holds all secrets. Single backup job (pgdump + S3 / rsync to offsite). Single upgrade path (`docker compose pull && docker compose up -d`).

### Cloud option (HIPAA-grade, when Ali Ann has a real client)

- **Provider:** AWS us-west-2 under a BAA (the same region Medplum's own managed tier defaults to for HIPAA).
- **Compute:** ECS Fargate for services, RDS Postgres Multi-AZ with encryption at rest, S3 for audio/PDF blobs with object lock.
- **Network:** VPC, private subnets, ALB with WAF in front of Caddy.
- **Secrets:** AWS Secrets Manager.
- **Logs:** CloudWatch, 7-year retention for audit logs.
- **Backup:** RDS snapshots + S3 cross-region replication.

### Cost estimate (1 team / 2 care recipients / 5 users)

**Self-host (Hetzner CAX31 + backup bucket):** ~$18/mo hardware + ~$2/mo backup + Twilio pay-per-SMS (~$5/mo nominal) + Oura PAT (free tier) + LLM spend (~$20/mo at current usage) ≈ **$45/mo.**

**AWS HIPAA self-managed:** ECS + RDS t4g.medium Multi-AZ + S3 + NAT + ALB + WAF ≈ **$380/mo** before LLM spend.

**Medplum Hosted (their managed tier):** Medplum pricing ~$2k/mo at this scale, not recommended for v0 given Jero's constraints.

**v0 recommendation:** self-host on the Mac mini Jero already has, move to Hetzner CAX31 within 2 weeks once he wants it off his machine.

---

## The V0 Cut

**Brutal rule:** if it isn't on this list, it doesn't ship in the first 4 weeks.

### Week 1 — "Record, save, share the link"
- Docker-compose bootstraps: postgres + medplum-server + gateway + web + caddy.
- Better-Auth magic link working for the two critical flows: caregiver login + low-tech-sister link.
- HTMX timeline page, server-rendered, no JS framework. Renders Connie's log.
- LiveKit server + one LiveKit Agent doing STT → gateway → Medplum Observation + Communication.
- `hash_chain` table exists and is appended on every write.
- Covers P0-1, P0-2, P0-3.

### Week 2 — "Export + prospect intake"
- Gotenberg container wired; `GET /export/:patient/:from/:to` returns a PDF with hash verification page.
- Krayin deployed, single pipeline configured for Longmont facility (stages: New Lead → Qualified → Tour → Application → Move-In Scheduled → Resident).
- Facility public page (HTMX) published at a shareable URL with QR.
- Prospect intake form (HTMX) posts to Krayin via Gateway.
- Voice intake variant: Ali Ann taps "new prospect by voice" and LiveKit Agent writes to Krayin.
- Covers P0-4, P0-5 (partially, capture + share), P0-6.

### Week 3 — "Move-in handoff + research agent"
- Bridge: shadow Medplum Patient created at stage=Qualified, flip to active at stage=Resident.
- Fit assessment LangGraph agent running on new leads.
- Research agent LangGraph graph live: triggered by Medplum Bot on new Observation, uses Europe PMC + OpenAlex, writes ClinicalImpression back. mem0 + pgvector deployed.
- Completes P0-5 end-to-end.
- First pass of P1-7 (research findings).

### Week 4 — "Low-tech polish + legal-threat readiness"
- HTMX low-tech surface tested on a real old Android browser. If it fails, it fails the release.
- SMS fallback via Twilio adapter: new log → optional SMS to low-tech sister with a plain link.
- Export tested against a lawyer-facing dry run.
- Oura connection (one caregiver connects a real ring) — only if Connie actually has one; otherwise deferred.
- Occupancy dashboard rendered from Gateway joining Krayin + Medplum.

**What gets cut:** Native app (React Native) — browser-first works on iPhones too. iMessage backfill — v0.5. Spreadsheet mirror — v0.5. Family video (LiveKit already capable, but no one is asking in week 4). CGM/BP/patch adapters.

All P0 user stories from the PRD are covered by end of week 4.

---

## What NOT to Build (forcing function)

1. **Do not build auth.** Better-Auth.
2. **Do not build the CRM.** Krayin. Extend, don't fork.
3. **Do not build FHIR persistence.** Medplum. This is the single biggest don't.
4. **Do not build a transcription engine.** LiveKit Agents + whisper.cpp.
5. **Do not build a PDF renderer.** Gotenberg.
6. **Do not build a vector database.** pgvector.
7. **Do not build an agent memory layer.** mem0.
8. **Do not build an agent orchestration framework.** LangGraph.
9. **Do not build a React SPA for the low-tech surface.** HTMX + server HTML.
10. **Do not build a PubMed crawler.** Europe PMC + OpenAlex.
11. **Do not build an audit DB.** AuditEvent + Provenance + 50-line hash chain.
12. **Do not build an SMS gateway.** Twilio adapter.
13. **Do not build a kanban library.** Krayin ships one.
14. **Do not build a family video product.** LiveKit already running for voice.
15. **Do not build a native app in week 1–4.** The HTMX surface works on every phone including Ali Ann's.
16. **Do not build a second Postgres.** One DB, multiple logical databases.
17. **Do not build a multi-tenant isolation model in v0.** Single team per docker-compose; per-team instances.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Medplum upstream velocity slows or pivots (~2.3k stars is modest) | Low-Med | High | FHIR is a standard; migration to HAPI FHIR is possible though painful. Abstract writes via Gateway so a swap is one component, not the whole app. |
| Medplum self-host has operational gotchas under load | Med | Med | Start on Mac mini, measure before moving to cloud. Follow Medplum docs to the letter. Cap v0 at 3 care recipients. |
| Krayin PHP/Laravel stack creates skill-silo inside a TS project | Med | Med | Isolate Krayin behind the Bridge: Gateway is the only thing that talks to Krayin. Jero never edits Laravel core; only config + custom fields via Krayin's own UI. |
| Krayin upgrade path breaks custom pipeline stages | Med | Med | Pin Krayin at v2.2.0 for v0; reevaluate upgrades quarterly. Custom fields live in Krayin's own config layer, not in forked source. |
| LiveKit server infra burden exceeds Jero's bandwidth | Med | Med | Fall back to LiveKit Cloud (same API) if self-host infra is eating time. Document the fallback in advance. |
| Better-Auth is young (27.8k stars but ~2 years old) | Low | Med | Auth flows are isolated in the Gateway. A swap to Auth.js is realistic if Better-Auth stalls. |
| Ali Ann's dad needs dominate the schedule and v0 slips | **High** | High | Architecture specifically designed to degrade gracefully: week 1 output is independently useful even if weeks 2–4 slip. |
| Legal threat escalates before export path is live | Med | **Critical** | Ship week 1 with hash chain already in place, even if UI is bare. The defensibility story is the first thing that has to work. |
| HIPAA posture is claimed but not audited for OnePoint itself | High | Med | Be explicit: "self-hosted on Medplum, inherits Medplum's controls, not independently audited." Don't overclaim in marketing. |
| Low-tech sister tries it once on a weird browser, hates it, blocks adoption | Med | High | Test on a real old phone before any family touches it. Accept that HTMX is the floor, not a "modern light" framework. |
| Research agent hallucinates a clinical conclusion and a family acts on it | Low | **Critical** | FR-14 framing is enforced at the frame_for_team node: every finding ends with "bring this to a licensed professional." No treatment recommendations, only literature summary with citations. |
| Krayin↔Medplum reconciliation job silently fails | Med | Med | Reconciliation emits an AuditEvent on any divergence; Gateway surfaces a red dot in the admin header if there are unresolved divergences. |
| Twilio cost balloons with alert volume | Low | Low | Per-team rate limit; opt-in SMS; default delivery is email + SSE. |
| Medplum Bot runner is not hardened enough for per-log-entry triggers | Med | Med | Decouple: Bot posts to a Gateway HTTP endpoint that enqueues a LangGraph job; the Bot itself does no real work. |
| Oura API changes / rate-limits out | Low | Low | Oura adapter is isolated; biometric ingest degrades to "no data" gracefully. |

---

## Open Architectural Decisions

These need Jero + Ali Ann input before implementation, not architect judgment.

1. **Does the single shared magic link go to Ali Ann's whole team, or does each sister get her own?** Single link is simpler for the low-tech sister but loses per-user attribution. Recommendation: per-person magic link with "remember this device" cookie so she only sees the link prompt once. Needs confirmation from Ali Ann.
2. **Where does the v0 Postgres physically live?** Options: Jero's Mac mini (free, home internet, risk of home outage), Hetzner CAX31 ($18/mo, Germany region — HIPAA implications if ever used for real PHI), or AWS us-west-2 ($380/mo, BAA-ready). Recommendation: Mac mini for week 1 so Jero can iterate fast, Hetzner by week 3, AWS only when a paying client needs HIPAA.
3. **Does v0 serve Ali Ann's dad AND Connie on day one, or does Connie come first?** The architecture supports both from day one (FR-26 per-person filter). The question is whether Jero doubles the testing surface in week 1. Recommendation: Connie first, Dad by end of week 2 — but this is Ali Ann's call.
4. **Does the "spreadsheet mirror" onboarding ship in v0 or v0.5?** FR-34–36 call it out as the on-ramp, but it's custom work and the v0 cut defers it to v0.5. Jero needs to decide if killing it delays Ali Ann's adoption. Recommendation: v0 ships without it; the HTMX surface is the on-ramp.
5. **Does Ali Ann want Krayin's PHP admin UI visible to her, or only through OnePoint's own wrapper?** Exposing Krayin directly is faster in week 2 but violates the "single surface" promise. Recommendation: hide Krayin entirely; thin wrapper pages in HTMX for the 5 CRM actions she actually uses (new lead, change stage, add note, schedule tour, move-in).
6. **Who runs the hash-chain verification at export time — the Gateway, or an external CLI?** Gateway is easier for Ali Ann; external CLI is more defensible ("we ran the verifier, the court can too"). Recommendation: both. The Gateway renders the PDF, and a separate `onepoint-verify` CLI is published open-source so any third party can re-verify.
7. **What is the fit-assessment agent's refusal policy when a prospect is a clinical mismatch for the facility?** "Decline with note" is simplest, but family feelings are in play. Recommendation: never auto-decline; always surface to Ali Ann with a recommendation + rationale. Needs her buy-in.
8. **Consent capture for family video in LiveKit.** Do we require a FHIR Consent resource before a video call can be recorded, or is the session consent sufficient? Recommendation: session consent + no recording by default in v0. Recording is a v1 decision with legal review.

---

*End of architecture. The next document should be the implementation plan — turning this into a week-by-week task list with concrete ownership for every custom surface named above.*

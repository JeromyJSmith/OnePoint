# 31 — AI-Native Advantage Design

**Status:** v1 · AI_ADVANTAGE_AGENT output
**Date:** 2026-04-11
**Stack assumption:** LiveKit Agents + whisper.cpp, LangGraph + mem0 + pgvector, Medplum FHIR, Europe PMC + OpenAlex, Claude (Haiku 4.5 / Sonnet 4.6 / Opus 4.6), Krayin CRM bridge.

---

## Executive Summary

OnePoint's AI thesis is not "AI helps caregivers." It is that **every voice capture instantly becomes five coordinated artifacts** — a timeline entry, a timesheet row, a FHIR Observation, a cited literature query, and a family-digest seed — inside a FHIR-compliant record with an immutable hash chain. Legacy CRMs (Aline, Yardi, ECP) and caregiver apps (CaringBridge, Lotsa) cannot retrofit this because their data models were built as forms, not as journals, and their AI surface is a single post-hoc summary bolted onto a sales funnel. The ten features below compose a single loop: a 90-second voice blob triggers structuring, literature retrieval, trend detection, and family synthesis — all grounded in the same FHIR record that produces the legal export. The moat is the loop, not any single feature: each capture enriches the per-patient memory graph (mem0 + pgvector), which makes the next capture cheaper, better-grounded, and harder to replicate. We stay under the $50/month/care-recipient target by routing 95% of calls to Claude Haiku 4.5 and caching aggressively at the (symptom-hash, patient-context) level.

---

## Defensibility Theory

A legacy competitor copying any single feature on this list is not the threat. The threat is that **the whole loop compounds** in ways that break the copycat's incentives:

1. **Schema asymmetry.** OnePoint logs are born FHIR-structured via LLM extraction at capture time. Every competitor's care log is a `notes` text column bolted next to a billing row. Retrofitting a text column into FHIR Observations is a multi-year migration inside a live compliance surface — Yardi's own eMAR takes 11 minutes per resident because its schema fights it. OnePoint's schema compounds from day one because every Observation auto-indexes into pgvector AND feeds mem0 AND triggers LangGraph.

2. **Capture-surface lock-in via Ali Ann's voice.** The voice-first capture pattern (FR-1..FR-5) is not an input method — it's a data moat. Each caregiver develops a personal voice style that the extraction prompt gets better at parsing over time via per-user few-shot examples stored in mem0. Five days of recordings turns a generic extractor into "Ali Ann's extractor." Aline can't ship this because their captured population is licensed nurses typing into forms; there's no voice ground truth to train against.

3. **Literature grounding requires the log to be structured first.** The research agent (AI-03) only works if the log is already parsed into symptoms + entities + temporal markers. Every competitor's notes field is unstructured, so their only option is to feed the whole text to a generic summarizer — which is exactly what Aline's marketing "system of recommendation powered by AI" collapses to. OnePoint can run topic-scoped PubMed queries because its schema tells it what to query on.

4. **Move-in handoff is a data join, not a product feature.** AI-08 turns prospect intake into the opening care log via a pointer inside the same FHIR Patient resource. ECP (the only competitor that does any form of handoff) runs CRM → EHR as a cross-module export. OnePoint doesn't export — there's one record. Zero re-entry because there was never a second system. Competitors would have to merge their CRM and EHR databases, which is a board-level architectural decision they are not going to make for a single owner-operator market.

5. **Incumbent inertia.** Aline's 100+ partner integrations mean every new feature crosses three product teams and a compliance queue. Yardi's eMAR has documented 11-minute-per-resident load times because nobody owns latency. OnePoint ships the entire stack self-hosted in a single Docker Compose. Velocity asymmetry is the most under-appreciated moat in enterprise software — incumbents literally cannot move this fast.

6. **Trust posture compounds.** A Place for Mom's $6M TCPA settlement and Senate investigation (per `20_competitor_matrix.md`) left the market with visible scar tissue. OnePoint's "we do not sell your information, we place one person at one facility" posture is impossible for a referral-fee business to adopt without tearing up its revenue model. AI features like the weekly digest (AI-06) and trend detection (AI-07) only work if families trust the capture posture — which means incumbents can't adopt them without rebuilding trust first.

7. **Per-patient memory graph.** mem0 builds a persistent, cross-session memory of the care recipient (their baseline gait, their typical afternoon confusion, their medications). Every new log is contextualized against this graph. Six months in, the graph is the product. A competitor building this feature from scratch starts with zero history per patient; OnePoint starts with whatever the team has captured that week.

The compound effect: a competitor who clones feature AI-01 still can't run AI-03 (no schema), AI-07 (no memory graph), or AI-08 (no unified record). Cloning the full loop means rebuilding their stack.

---

## Feature Designs

### AI-01: Voice-Blob-to-Structured-Care-Log

- **User trigger:** Caregiver opens OnePoint (web or native app), taps the record button, speaks freely for 15–300 seconds, taps stop (or hits end-of-turn silence). Also triggered by LiveKit phone-in for FR-5 hands-free scenarios.
- **System behavior:**
  1. LiveKit Agents session captures WebRTC audio; streams to server.
  2. whisper.cpp (Metal on Apple Silicon; small.en or medium model) transcribes locally. Offline path: WASM whisper.cpp in the browser for NFR-2.
  3. Raw transcript hits the LangGraph `extract_care_log` node. The node passes transcript + mem0 per-patient context (last 10 entries, known meds, known conditions) to Claude Haiku 4.5.
  4. Haiku returns a JSON object: `timeline_entry`, `timesheet_row`, `symptoms[]`, `entities[]`, `medications_mentioned[]`, `vitals_mentioned[]`, `confidence_score`, `needs_human_review: bool`.
  5. The result is written as a FHIR `Observation` (clinical obs), `Communication` (narrative), and a custom `Timesheet` resource inside Medplum. Provenance is stamped with caregiver ID, device ID, UTC timestamp, and inserted into the SHA-256 hash chain.
  6. mem0 is updated with the new memories.
  7. A Medplum Bot webhook fires off downstream triggers: AI-03 (research), AI-07 (trend detection).
- **Tech approach:** LiveKit Agents (WebRTC + audio pipeline) → whisper.cpp (local STT) → LangGraph node → Claude Haiku 4.5 via Anthropic API with structured output (tool-use JSON schema) → Medplum FHIR client → mem0 update → pgvector embedding.
- **Model choice + rationale:** **Claude Haiku 4.5** ($1/MTok input, $5/MTok output). Fastest-responding frontier-class model for sub-second structured extraction. Escalates to Sonnet 4.6 only on `confidence_score < 0.7`.
- **Data in:** `{audio_blob: bytes, caregiver_id: uuid, patient_id: uuid, device_id: string, captured_at: iso8601, mem0_context: object}`
- **Data out:**
  ```json
  {
    "timeline_entry": { "text": "...", "start": iso8601, "end": iso8601, "topic_tags": ["gait", "meds"] },
    "timesheet_row": { "caregiver_id": uuid, "start": iso8601, "end": iso8601, "duration_min": int, "task_codes": [] },
    "symptoms": [ { "concept": "confusion", "severity": "mild", "snomed_code": "40917007", "onset": "evening" } ],
    "entities": [ { "type": "medication", "name": "sinemet", "rxnorm": "197531", "dose_mentioned": null } ],
    "vitals_mentioned": [ { "type": "systolic_bp", "value": 142 } ],
    "confidence_score": 0.92,
    "needs_human_review": false
  }
  ```
- **Latency target:** <8 s from stop-recording to visible timeline entry on the web surface. <12 s under NFR-3.
- **Cost target:** ~$0.003 per 90-second log (transcript ~200 tokens in, ~500 tokens out on Haiku). **~$0.45/care-recipient/month** at 5 logs/day × 30 days.
- **Failure mode:**
  - Transcription fails: raw audio is still persisted to Medplum as a Media resource with a "transcription pending" flag. The timeline shows a playable audio card; the team sees exactly what was said.
  - LLM extraction fails or low-confidence: entry lands as unstructured text + `needs_human_review: true`, queued for next-day batch reprocessing with Sonnet 4.6.
  - Offline: whisper.cpp WASM in browser produces a local transcript; log is queued in IndexedDB; syncs to server on reconnect. This is NFR-2, not a graceful degradation — this is a first-class path.
- **Defensibility:** Competitors' care logs are text blobs. OnePoint's care logs are FHIR-grounded, SNOMED-coded, RxNorm-resolved — which makes every downstream feature cheap. ECP captures none of this from voice; CaringBridge captures none of this at all.
- **Maps to FR:** FR-1, FR-3, FR-4, FR-5, FR-25, FR-30, NFR-2, NFR-3, NFR-6.
- **Competitive contrast:** Sherpa CRM has call recording + transcription for sales calls only (`20_competitor_matrix.md` §10), no care-log path. CaringBridge users report "speech-to-text consistently aborting" (`21_review_intelligence.md` cluster #1). Yardi's eMAR takes 11 min/resident because it's form-based (cluster #3). None produce a structured care log from free-form speech; OnePoint is the only entry in the matrix where this column says ✓.

---

### AI-02: Legal-Grade Audit Export

- **User trigger:** Ali Ann taps "Export audit package" in the dashboard, picks a date range and a care recipient, selects output format (PDF / signed PDF / zip-with-hashes).
- **System behavior:**
  1. API queries Medplum FHIR for all resources tied to the patient in the range: Observations, Communications, Timesheets, Provenances, AuditEvents, linked Media (audio blobs), linked DiagnosticReports.
  2. Each resource is rendered into a chronological, attributed timeline via a Gotenberg HTML template.
  3. The SHA-256 hash chain is walked: every (prev_hash, resource_id, author_id, timestamp) is verified, and a verification page is appended showing "Chain intact: yes/no, last verified block = N."
  4. Attribution page lists every contributor with their role, active time range, and number of entries.
  5. Gotenberg converts the HTML into PDF/A (archival format, required for legal evidence).
  6. Optional: Claude Sonnet 4.6 pass generates a 1-page "executive narrative" summary at the front ("This record covers 2026-01-01 through 2026-03-31, 142 entries by 4 caregivers, 3 clinical events flagged, 0 hash chain violations"), with every claim hyperlinked to a specific timeline entry by ID.
  7. The export itself is registered as a new FHIR `DocumentReference` resource — so the act of exporting is inside the audit trail.
- **Tech approach:** Medplum FHIR query → custom TS renderer → Gotenberg (HTML→PDF/A) → SHA-256 chain verifier → Claude Sonnet 4.6 for narrative page → upload as FHIR DocumentReference.
- **Model choice + rationale:** **Claude Sonnet 4.6** ($3/MTok input, $15/MTok output) for the narrative-page generation only. Sonnet because the narrative is read by an attorney or insurer — it must be accurate, cited, and defensible. Haiku's error rate is too high for legal output. Most of the export pipeline is deterministic and runs with no model at all.
- **Data in:** `{patient_id: uuid, start: date, end: date, format: "pdf" | "pdf_a" | "zip"}`
- **Data out:** PDF/A file; ZIP containing the PDF/A + all source FHIR resources in NDJSON + Merkle-style hash-chain verifier script + README with verification instructions. Every page footer has a hash fingerprint linking back to the chain.
- **Latency target:** <60 s for 30 days of logs (SM-4). <180 s for 12 months.
- **Cost target:** ~$0.08 per export (1-page Sonnet narrative ~1k tokens in, 500 out) + Gotenberg compute (~$0.002). **~$0.32/care-recipient/month** if exported weekly.
- **Failure mode:**
  - Hash chain break: export still succeeds, but the verification page shows the broken block and the cover letter is replaced with a red-banner warning. The audit trail of the break is itself auditable.
  - FHIR resource missing: marked as "resource reference present but body missing" with a recovery note.
  - Gotenberg crash: falls back to Pandoc (GPL CLI, per `11_oss_landscape.md` §G).
- **Defensibility:** Hash-chained FHIR audit + PDF/A + narrative is a *legal product*, not a report. ECP has an audit log but it's inside their enterprise silo — you cannot hand it to your attorney as a zip. Aline's reporting takes "a time suck to fix" (cluster #4, `21_review_intelligence.md`). Yardi has "no emergency backup system other than emailing to users" (Capterra review).
- **Maps to FR:** FR-30, FR-31, FR-32, SM-4.
- **Competitive contrast:** Per `20_competitor_matrix.md`, only enterprise CRMs produce any export at all, and none produce an attributed, hash-chained, subpoena-ready output. This is the single feature that converts an active-litigation caregiver from a CaringBridge user into a OnePoint user in one demo.

---

### AI-03: Medical Research Agent (Cited, Per-Log)

- **User trigger:** A new FHIR `Observation` lands in Medplum (from AI-01 or from a manual entry). A Medplum Bot fires the `research_agent` webhook. Also triggered batch nightly at 02:00 local time for the previous day's entries.
- **System behavior:**
  1. LangGraph graph `medical_research_v1` receives `{observation_id, patient_id}`.
  2. **Planner node (Sonnet 4.6):** reads the observation + patient history from mem0 + known diagnoses from Medplum Patient/Condition resources; outputs a structured research query plan: `[{query_type: "symptom+comorbidity", terms: ["orthostatic hypotension", "parkinsonism", "elevation change"], databases: ["europepmc", "openalex"]}, ...]`.
  3. **Retrieval nodes (no LLM — just tool calls):** fire off parallel calls to Europe PMC REST (primary, 33M pubs) and OpenAlex (240M works, citation enrichment). Results cached per `sha256(query_terms + patient_context_hash)` in pgvector + Postgres for 30 days. Cache hit rate target: 60%+ after 2 weeks of use.
  4. **Reader node (Haiku 4.5):** takes top 8 abstracts, reads each against the triggering observation, emits a structured finding per paper: `{pmid, title, authors, year, journal, relevance_score, finding_type: "supports"|"contradicts"|"context", one_sentence_takeaway, direct_quote, warning: bool}`.
  5. **Synthesizer node (Sonnet 4.6):** merges findings into a cited "here's what the literature says" note. Every claim is hyperlinked to a specific paper by PMID. Framed per FR-14 — informational, not diagnostic.
  6. Result lands as a FHIR `DiagnosticReport` resource tied to the original Observation. Appears on the timeline as a research card next to the log entry.
- **Tech approach:** LangGraph (durable state, human-in-loop ready) → Europe PMC REST + OpenAlex API → Claude Haiku 4.5 (reader) + Sonnet 4.6 (planner + synthesizer) → pgvector cache → Medplum Bot → FHIR DiagnosticReport.
- **Model choice + rationale:**
  - Planner = Sonnet 4.6: query planning requires medical reasoning; cheap because called once per trigger.
  - Reader = Haiku 4.5: high-volume abstract reading, needs speed and low cost.
  - Synthesizer = Sonnet 4.6: final user-facing output, must be accurate and well-cited.
- **Data in:** `{observation_id: uuid, patient_id: uuid, trigger: "realtime" | "nightly_batch"}`
- **Data out:** FHIR DiagnosticReport:
  ```json
  {
    "resourceType": "DiagnosticReport",
    "status": "final",
    "code": { "coding": [{ "system": "local", "code": "literature_review" }] },
    "subject": "Patient/{id}",
    "basedOn": ["Observation/{id}"],
    "conclusion": "3 papers support, 1 contradicts, 2 warnings surfaced...",
    "presentedForm": [{ "contentType": "text/markdown", "data": "<cited markdown>" }],
    "extension": [
      { "url": "findings", "value": [{ "pmid": "...", "relevance": 0.89, "type": "warning", ... }] }
    ]
  }
  ```
- **Latency target:** <90 s realtime path; nightly batch is untimed.
- **Cost target:** ~$0.04 per trigger (planner 1k/500 Sonnet ~$0.011 + reader 8×2k/500 Haiku ~$0.036 — wait, recompute: 8 abstracts × 2k input + 500 out Haiku = 16k in × $1/MTok = $0.016 + 8 × 500 × $5/MTok = $0.020, reader = $0.036 — no: 4k/2k total Haiku = $0.014 — call it $0.04 per trigger worst case before cache). **With 60% cache hit rate: ~$6/care-recipient/month** at 5 logs/day.
- **Failure mode:**
  - Europe PMC rate-limit: OpenAlex as fallback; then PubMed E-utilities as last resort.
  - No relevant papers: DiagnosticReport still generated with `status: "final"`, conclusion = "No directly relevant literature found for this query"; no fabricated citations. Halted-early is a legitimate outcome.
  - Hallucinated citation: synthesizer output is validated against retrieved PMIDs — any citation not in the retrieval set is stripped. This is a hard post-check.
- **Defensibility:** Requires structured logs (AI-01) + mem0 per-patient context + literature APIs wired in. No competitor in the matrix does this. "AI" claims at Aline/Sherpa/ECP are all unverified marketing (§Competitor Matrix Research Notes).
- **Maps to FR:** FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, SM-5.
- **Competitive contrast:** Literally nobody does this. The closest is CareZone's old pill-bottle OCR, which isn't research. Aline's "system of recommendation powered by AI" is unverified and operates on sales leads, not medical observations (`20_competitor_matrix.md` §11).

---

### AI-04: Placement Fit Scoring

- **User trigger:** A new `Prospect` record lands in Krayin CRM (from AI-05 voice intake or the web form FR-39). Webhook fires to the `placement_fit` LangGraph node.
- **System behavior:**
  1. Load the Longmont facility profile (FR-37): level-of-care, specializations (memory care, Parkinson's, post-acute), vacancy, pricing tiers, regulatory fit (CO ALR requirements).
  2. Load the prospect's extracted intake: diagnoses, mobility, cognitive status, financial qualification, urgency, family decision-maker count.
  3. **Fit node (Sonnet 4.6):** runs a structured fit assessment against a scoring rubric prompt. Outputs `{fit_score: 0-100, fit_class: "strong" | "edge" | "miss", reasoning: [...], red_flags: [...], unknowns_to_ask: [...], recommended_next_action: string}`.
  4. The assessment writes back to the Krayin Prospect record as structured fields. A color band (green/yellow/red) appears on Ali Ann's kanban inbox.
  5. For "edge" and "miss" cases, the agent drafts a compassionate suggested response Ali Ann can send (e.g., "Here are 3 facilities in Longmont that handle your mother's care level better than we can").
- **Tech approach:** Krayin CRM webhook → LangGraph → Claude Sonnet 4.6 → write back to Krayin via API.
- **Model choice + rationale:** **Sonnet 4.6.** Fit scoring touches regulated fields (CO ALR compliance) and affects a high-stakes business decision. Haiku is too risky here; Sonnet's error rate on structured-JSON output is well-suited. Not Opus — Opus is reserved for hard escalation cases (AI-07).
- **Data in:**
  ```json
  {
    "prospect_id": uuid,
    "facility_profile": { ... },
    "intake": { "diagnoses": [...], "mobility_level": "requires_assist", "cognitive_status": "moderate_dementia", "financial_qualified": true, "urgency": "48h", "decision_makers": 3 }
  }
  ```
- **Data out:**
  ```json
  {
    "fit_score": 78,
    "fit_class": "strong",
    "reasoning": ["Facility specializes in dementia care", "Ambulatory-with-assist is within scope", "24-hour discharge urgency matches hospital-discharge path"],
    "red_flags": [],
    "unknowns_to_ask": ["Does POLST exist?", "Medicaid eligibility confirmed?"],
    "recommended_next_action": "Schedule tour within 24 hours; send CO-602 equivalent for physician completion"
  }
  ```
- **Latency target:** <30 s from intake submission to fit score visible in Krayin kanban.
- **Cost target:** ~$0.05 per prospect (2k in, 800 out Sonnet). At 5 prospects/week, **~$1/month**.
- **Failure mode:** LLM unavailable or low-confidence: prospect enters kanban as "manual review" (yellow band, no score). Ali Ann sees them all; none are silently dropped.
- **Defensibility:** Requires Krayin + CO ALR schema + prompt tuned to owner-operator context. Enterprise CRMs (Aline, Yardi) don't do this because their prospects get scored by marketing teams for chain-wide optimization, not one-facility fit. Roobrik does pre-qualification but is top-of-funnel only (`20_competitor_matrix.md` §13).
- **Maps to FR:** FR-37, FR-39, FR-40, FR-46, FR-48, G7.
- **Competitive contrast:** Aline "AI recommendation" is unverified marketing; Sherpa's "Prospect Opportunity Score" mechanism is undocumented (`20_competitor_matrix.md` §§10–11). OnePoint ships a transparent, cited scoring rubric a single operator can read, verify, and override.

---

### AI-05: Voice-First Prospect Intake

- **User trigger:** Ali Ann is on a phone call with a prospect's family member. She taps "Capture prospect" in the OnePoint app (or dials the dedicated LiveKit SIP number if she's on a landline). The call continues; OnePoint listens in the background.
- **System behavior:**
  1. LiveKit Agents captures the call audio (with consent banner + recording disclosure — FR-22 consent pattern). Dual-channel if possible.
  2. whisper.cpp transcribes (local). Diarization labels "Ali Ann" vs "family caller."
  3. At call end, a LangGraph `prospect_intake_extract` node runs. Uses Claude Sonnet 4.6 to extract the FR-39 intake fields: prospect's name, age, current care setting, diagnoses, mobility, cognitive status, care-level needs, financial qualification, decision-maker contact, urgency, preferred move-in window, referral source.
  4. Missing fields are flagged as "unknown — follow up." The agent drafts a follow-up email (via Gmail MCP) listing exactly what's missing, pre-filled for Ali Ann to send with one click.
  5. A Krayin Prospect record is created. AI-04 immediately fires against it.
  6. The raw audio + transcript are stored as FHIR Media + Communication resources tied to the Prospect, hash-chained alongside care logs (same audit discipline as FR-30, applied to the placement pipeline).
- **Tech approach:** LiveKit Agents (SIP or WebRTC) → whisper.cpp (local STT + diarization) → LangGraph → Claude Sonnet 4.6 → Krayin API + Gmail MCP (for drafted follow-up).
- **Model choice + rationale:** **Sonnet 4.6** for extraction because conversations are noisy and multi-party; Haiku struggles with diarization-aware extraction. One-shot per call, so the cost is acceptable.
- **Data in:** `{call_audio: blob, duration_min: int, caller_phone: string, call_direction: "inbound"|"outbound"}`
- **Data out:** Krayin Prospect record + FHIR Media + draft email. Schema:
  ```json
  {
    "name": "Margaret Thompson",
    "age": 84,
    "diagnoses": ["early-stage Alzheimer's", "post-hip-replacement"],
    "mobility": "walker_assist",
    "care_level": "assisted",
    "urgency": "hospital_discharge_72h",
    "decision_maker": { "name": "Sarah Thompson", "relationship": "daughter", "phone": "..." },
    "referral_source": "hospital_discharge_planner_longmont_general",
    "unknown_fields": ["financial_qualification", "POLST_on_file"],
    "follow_up_draft": "<email body>"
  }
  ```
- **Latency target:** <2 min after call end for intake record + fit score + drafted email to be ready.
- **Cost target:** ~$0.08 per call (5k tokens in + 1k out Sonnet). At 20 calls/month, **~$1.60/month**.
- **Failure mode:** Call too noisy for diarization: transcript still produced, fields less complete, intake record created with higher `unknown_fields` count. Ali Ann sees the call card and can replay audio inline.
- **Defensibility:** No competitor captures prospects by voice for a single-facility owner-operator. Sherpa records sales calls but for sales coaching, not intake extraction (`20_competitor_matrix.md` §10). Zero competitors turn the call into a structured prospect + drafted follow-up email + CO-compliance flags.
- **Maps to FR:** FR-1, FR-39, FR-42, FR-45, FR-48.
- **Competitive contrast:** Unique in matrix. Beats A Place for Mom's pattern of "bombarding families with dozens of unvetted sales calls" (cluster #8, `21_review_intelligence.md`) because OnePoint's intake is one call, owned by the facility operator, never resold.

---

### AI-06: Family Weekly Digest Synthesis

- **User trigger:** Cron job fires every Sunday at 18:00 local time per care recipient. Can also be triggered ad-hoc by "Generate digest now" button.
- **System behavior:**
  1. LangGraph `weekly_digest` loads the past 7 days of FHIR resources for the care recipient: Observations, Communications, Media, DiagnosticReports (AI-03 outputs), wearable data.
  2. mem0 loads per-family recipient preferences: "Aunt Karen wants clinical summary," "Flip-phone sister wants the feel-good version."
  3. Claude Sonnet 4.6 runs the `weekly_digest_v1` prompt. Outputs:
     - **Headline:** "Mom had a good week, with one concern." (or "difficult week with improvements on Friday," etc.)
     - **Top 3 moments:** each a 1-2 sentence vignette citing the underlying log entry by ID.
     - **One concern flag:** if trend detection (AI-07) fired, surface it here in plain language.
     - **Numbers that matter:** meds taken vs missed, hours of sleep, BP range, total caregiver hours.
     - **Links:** each claim hyperlinked to the specific log entry in the OnePoint web surface.
  4. Digest is delivered via three channels per family member preference: email (Gmail MCP), SMS (Twilio behind adapter, per `11_oss_landscape.md`), or shareable web link (magic-linked per FR-7).
  5. A link at the bottom: "Reply to this digest." Replies route back into OnePoint as Communication resources, so the family's "I have a question about Friday" is captured on the timeline.
- **Tech approach:** Cron → LangGraph → Medplum query → Claude Sonnet 4.6 → Gmail MCP / Twilio adapter / HTMX share-link surface.
- **Model choice + rationale:** **Sonnet 4.6.** Digest writing requires tone calibration (Aunt Karen's clinical voice vs the flip-phone sister's feel-good voice), which Haiku handles less reliably. One-shot per family member per week; cost is tolerable.
- **Data in:** `{patient_id: uuid, week_start: date, week_end: date, recipient_id: uuid, recipient_preferences: {tone: "clinical"|"warm"|"brief", channels: [...]}}`
- **Data out:**
  ```json
  {
    "headline": "Mom had a steady week with one concern flagged Wednesday.",
    "moments": [
      { "text": "Walked to the kitchen unassisted Tuesday morning — first time in a week.", "log_entry_id": "obs-123" }
    ],
    "concern": { "text": "Blood pressure trended low in the evenings; research agent flagged elevation-related instability.", "diagnostic_report_id": "dr-456" },
    "numbers": { "meds_taken_pct": 96, "sleep_hours_avg": 6.8, "bp_range_sys": [102, 148], "caregiver_hours": 42 },
    "delivery": { "email_sent": true, "sms_sent": false, "web_link": "https://..." }
  }
  ```
- **Latency target:** <60 s per digest. Batched in parallel across all family recipients.
- **Cost target:** ~$0.06 per digest (8k tokens in — a week of logs + 1k out Sonnet). At 4 family members per care recipient × 4 digests/month = **~$1/month/care-recipient**.
- **Failure mode:** No activity that week: digest still produced with "quiet week, no concerns." Tone stays consistent so the family doesn't get a broken-looking email.
- **Defensibility:** Only possible because the underlying logs are structured (AI-01) and contextualized via mem0 + AI-07 trend detection. Competitors' caregiver apps either have no digest or produce a dumb activity log. The family never reads those.
- **Maps to FR:** FR-3 (structured), FR-25 (timeline feed), FR-33 (family communication), SM-2, SM-3.
- **Competitive contrast:** CaringBridge is the closest analog — family members subscribe to a patient page — but updates are manually authored by the family (`20_competitor_matrix.md` §2). OnePoint writes the update automatically, grounded in clinical data, with every claim traceable. CaringBridge also has "buggy and freezes up randomly" issues (cluster #1), so even the manual path is broken.

---

### AI-07: Trend Detection Across Logs + Biometrics

- **User trigger:** Nightly batch at 03:00 local time per care recipient. Also triggered on any new wearable data ingest (Oura sync) OR a new log entry that matches one of 20 pre-defined "watch patterns" (confusion, gait, falls, BP mention, refusal to eat).
- **System behavior:**
  1. LangGraph `trend_detector_v1` loads: last 30 days of FHIR Observations, last 30 days of Oura data (or other wearables), mem0 per-patient baseline.
  2. **Statistical node (no LLM):** runs rolling-window analyses over the numeric observations — z-score drift for BP, sleep, HRV, activity; frequency deltas for symptom mentions (e.g., "confusion" mentioned 3× this week vs 0× baseline).
  3. **Pattern detector node (Haiku 4.5):** takes the statistical drifts + the corresponding log entries and asks whether the drift is clinically interesting. Prompt: "Is this drift a compound signal? Specifically flag: BP + hydration + elevation, sleep + confusion, gait + falls risk."
  4. If compound signal detected, **escalation node (Opus 4.6):** runs one deep-read pass — reads the full 30-day context + any prior research agent findings + mem0 baseline, produces a detailed "possible pattern" finding with a confidence score and a recommendation framed per FR-14 (informational, bring to your doctor).
  5. Result lands as a FHIR `ClinicalImpression` resource. If high-confidence AND high-severity, a push notification fires to Ali Ann and the designated family medical POA.
  6. The finding is logged into mem0 so the next research agent (AI-03) query is primed with it.
- **Tech approach:** LangGraph → pgvector (for historical log similarity search) → NumPy/statsmodels for drift → Claude Haiku 4.5 for pattern detection → Claude Opus 4.6 (only on compound hits) → Medplum ClinicalImpression.
- **Model choice + rationale:**
  - Pattern detector = Haiku 4.5: fast, high-volume, most runs are no-op.
  - Escalation = **Claude Opus 4.6** ($15/MTok input, $75/MTok output). Opus only when the stats + Haiku signal say "this is real." This is where OnePoint earns the trust of a family — getting this one right matters more than cost. Budget: ~5% of nights will trigger Opus escalation.
- **Data in:** `{patient_id: uuid, as_of: date, windows: [7, 14, 30]}`
- **Data out:**
  ```json
  {
    "resourceType": "ClinicalImpression",
    "status": "completed",
    "summary": "BP trending low in evenings over 10 days; correlates with elevation re-entry and weaker gait reports; pattern matches literature finding in DiagnosticReport dr-456.",
    "finding": [
      { "itemCodeableConcept": {"text": "orthostatic drift"}, "basis": "Oura + log entries obs-101..obs-142" }
    ],
    "prognosis": "Recommend: bring to next clinical visit; consider hydration and orthostatic BP check protocol.",
    "confidence": 0.81,
    "alerted_to": ["caregiver-ali", "family-poa-james"]
  }
  ```
- **Latency target:** <10 min for nightly batch per patient. Compound-hit escalation <3 min.
- **Cost target:** Nightly Haiku scan: ~$0.01/night. Opus escalation (5% of nights): ~$0.30/hit. **~$0.75/care-recipient/month.**
- **Failure mode:** False positive: finding is marked with confidence; Ali Ann can mark "not useful" which trains mem0 (per-patient rejection memory). False negative is the real risk — mitigated by the pre-defined watch-pattern trigger list (which fires regardless of drift).
- **Defensibility:** Requires structured logs + biometrics in the same FHIR store + per-patient memory + literature grounding. The entire stack is the feature. No caregiver app has wearables; no CRM has biometrics; ECP has no research layer. OnePoint is the only combined stack in the matrix.
- **Maps to FR:** FR-13 (warning patterns), FR-16, FR-18, FR-19, FR-24, FR-25, SM-5.
- **Competitive contrast:** CarePredict is the only adjacent vendor doing wrist-based drift detection, and it doesn't read logs. OnePoint's compound signal (log text + biometric drift + literature corroboration) is not done by anyone in the matrix.

---

### AI-08: Move-In Handoff Intelligence

- **User trigger:** A Krayin Prospect moves to stage = `Move-In Scheduled` or `Resident`. Webhook fires to the `move_in_handoff` LangGraph node.
- **System behavior:**
  1. Load the full Prospect record: intake (AI-05 output), fit assessment (AI-04), all prospect-phase Communications (tour notes, family exchanges), collected compliance docs (602-equivalent, TB, POLST).
  2. **Transformer node (Sonnet 4.6):** converts the Prospect into a pre-populated FHIR Patient + Condition + CarePlan + RelatedPerson + Practitioner (for Ali Ann's team) resource set. Every field is annotated with provenance ("this came from the intake call on 2026-03-14").
  3. **Gap analysis node:** identifies which fields are still missing for a full care record (e.g., "current medications list not on file — this is day-1 questions for family"). Produces a day-1 checklist for Ali Ann.
  4. **Day-1 care-plan draft node (Sonnet 4.6):** drafts an opening care plan — baseline care schedule, shift expectations, known risks (from AI-04 red flags), first-week observation targets. The plan is a starting point, not locked.
  5. The FHIR Patient is created in Medplum. The Prospect record in Krayin is linked by `patient_fhir_id`. The care log timeline now starts *from the intake call*, not from move-in day — the family sees the full arc including the tour notes.
  6. mem0 is seeded with the prospect-phase memories so AI-01 (voice extraction on day 1) already knows the patient baseline.
- **Tech approach:** Krayin webhook → LangGraph → Claude Sonnet 4.6 → Medplum FHIR Patient/Condition/CarePlan/RelatedPerson/Practitioner → mem0 seed.
- **Model choice + rationale:** **Sonnet 4.6**. One-shot per move-in; must be thorough and accurate; Sonnet's structured-output reliability is the right tradeoff. Opus is overkill for a transform task.
- **Data in:** `{prospect_id: uuid, move_in_date: date}`
- **Data out:** FHIR Patient bundle + Day-1 checklist + Day-1 draft care plan + mem0 seed confirmation. Sample checklist:
  ```json
  {
    "day_1_checklist": [
      { "task": "Confirm current medications", "source_gap": "not captured in intake", "priority": "high" },
      { "task": "Collect POLST original", "source_gap": "copy only in Prospect record", "priority": "high" }
    ],
    "care_plan_draft": { ... },
    "patient_fhir_id": "Patient/xyz",
    "timeline_seed_entries": 14
  }
  ```
- **Latency target:** <60 s from stage transition to fully populated FHIR Patient + checklist visible.
- **Cost target:** ~$0.10 per move-in (5k in, 2k out Sonnet). At ~1 move-in/month, **~$0.10/month** amortized.
- **Failure mode:** Missing prospect data: handoff still runs, `day_1_checklist` is longer. No re-entry, ever — the Patient resource exists, the team fills gaps day-of.
- **Defensibility:** ECP is the only competitor that claims this (`20_competitor_matrix.md` §12), but ECP is CRM→EHR inside an enterprise licensed-facility stack. OnePoint does it with a *family-accessible* record that includes the prospect-phase voice captures. ECP cannot mimic this without abandoning its licensed-facility sales motion.
- **Maps to FR:** FR-44, FR-41, FR-42, FR-37.
- **Competitive contrast:** ECP's handoff is real but invisible to families. Aline's is a within-product data pass. OnePoint's handoff *spans the family-facing surface*, which neither can touch without rebuilding their trust story.

---

### AI-09: iMessage Backfill Intelligence

- **User trigger:** Ali Ann taps "Import historical care messages" in onboarding. Selects which contacts to import (per-contact consent per FR-22). Points to her local `chat.db`.
- **System behavior:**
  1. Local SQLite reader pulls selected conversations' messages. Never uploads raw `chat.db`.
  2. Per-message pass with Claude Haiku 4.5: "Is this message about care for Connie? If yes, extract the same schema as AI-01."
  3. Care-relevant messages are backfilled as FHIR Observation / Communication resources with their original iMessage timestamps preserved, provenance marked as `source: imessage_backfill`, participant marked as the original sender.
  4. After extraction, a Sonnet 4.6 pass walks the backfilled timeline and produces a "historical summary" — what the team was tracking, what got dropped, key events before OnePoint existed. This summary seeds mem0 so AI-03 and AI-07 have pre-OnePoint context.
  5. The un-imported (non-care) messages are never written anywhere — they don't exist inside OnePoint.
- **Tech approach:** Local SQLite reader (custom, ~200 LOC, per `11_oss_landscape.md`) → Claude Haiku 4.5 for per-message filter/extract → Claude Sonnet 4.6 for historical summary → Medplum backfill with historical timestamps → mem0 seed.
- **Model choice + rationale:** **Haiku 4.5** for the per-message filter — this is a high-volume, simple-classification task. **Sonnet 4.6** only for the one-shot historical summary pass.
- **Data in:** `{chat_db_path: string, contact_phones: [string], patient_id: uuid, date_range: {start, end}}`
- **Data out:** Count of imported Observations + FHIR resources with preserved timestamps + historical summary + mem0 seed.
- **Latency target:** 2 minutes per 1,000 messages (local STT not involved; Haiku is fast).
- **Cost target:** One-time at onboarding. ~$0.50 per 1,000 messages (1,000 × 100-token input, 50-token output Haiku). A typical backfill of 5,000 messages = **~$2.50 one-time**.
- **Failure mode:** Mis-classification: message marked non-care that is actually care. Mitigated by a review mode — Ali Ann can batch-review imported vs excluded messages, reclassify, and reprocess. No message is ever imported without being visible.
- **Defensibility:** No competitor does this — PRD §5.5 is the only place in any caregiver product that imports historical text conversations with per-person consent. Exists only because OnePoint has the voice-blob extraction stack already built; iMessage is just another upstream source.
- **Maps to FR:** FR-20, FR-21, FR-22, FR-23, FR-25.
- **Competitive contrast:** Unique in matrix. The legal-litigation use case (Ali Ann's current threat per PRD §10) turns this into table stakes — texts are evidence.

---

### AI-10: Vision-Verified Observations (the "show me this" agent)

- **User trigger:** Caregiver is in voice capture mode and says something like "Let me show you this" OR toggles the vision camera explicitly OR the extraction detects an ambiguous entity that could be resolved visually ("she took the blue one").
- **System behavior:**
  1. LiveKit Agents opens a vision channel. Caregiver shows the camera a pill bottle, BP cuff display, wound, rash, physical environment.
  2. A single frame is captured (or a 2s burst).
  3. **Vision node (Sonnet 4.6 with vision, or Haiku 4.5 with vision):** extracts what's visible. For pills: brand/generic name, imprint, dose, quantity remaining. For BP cuff: systolic/diastolic/pulse. For environment: hazards, bed setup, mobility aids present. For wound/rash: size, color, location (no diagnosis — description only).
  4. The extracted observation is merged with the concurrent voice transcript into a single FHIR Observation. The image is stored as a FHIR Media resource linked to the Observation (with automatic face-blurring for any incidental humans).
  5. For medication verification: cross-reference against the patient's known medication list in Medplum — flag mismatches immediately. ("You said Sinemet but the bottle I see says Mirapex.")
- **Tech approach:** LiveKit Agents (vision channel) → frame capture → Claude Sonnet 4.6 vision (or Haiku for high-volume pill checks) → FHIR Observation + Media → med reconciliation against Medplum.
- **Model choice + rationale:**
  - Pill/BP cuff/simple extraction = **Haiku 4.5 with vision** ($1/MTok input, $5/MTok out — vision token cost included).
  - Wound/environment/complex = **Sonnet 4.6 with vision** ($3/MTok input, $15/MTok output).
- **Data in:** `{frame: bytes, concurrent_transcript: string, patient_id: uuid, vision_intent: "pill"|"vitals"|"wound"|"environment"}`
- **Data out:** FHIR Observation with `component` fields for visible-value entries + FHIR Media resource.
- **Latency target:** <6 s from frame capture to confirmation on screen.
- **Cost target:** ~$0.005 per vision frame (1 image ~= 1k tokens + 500 out Haiku). At ~3 vision events/week, **~$0.06/month**.
- **Failure mode:** Ambiguous image (blurry, partial): result marks low-confidence and asks for a retake in-session. Never silently guesses.
- **Defensibility:** Needs the voice + vision + FHIR stack in one session. CircleOf has video calls but no vision extraction; no caregiver or CRM product in the matrix has a vision-reasoning capture path. CaringBridge's "app fails when it comes to adding photos" (cluster #14, `21_review_intelligence.md`) is the competitive floor — most of the market can't even attach a picture, let alone read one.
- **Maps to FR:** FR-2, FR-25, FR-30.
- **Competitive contrast:** Unique in matrix. Addresses PRD FR-2 directly and closes the medication-verification gap that none of the enterprise eMARs solve (per cluster #2, GPS-betrayal is the closest analog — and that's a punitive feature, not an empowering one).

---

## Compound Effects

The ten features compose three higher-order capabilities that no competitor can ship without running the full loop:

**1. Predictive Care.** AI-01 structures the log. AI-03 grounds it in literature. AI-07 detects drift across logs + biometrics. Together they enable a sequence the matrix has never shipped: *"Here is what she did today. Here is what the literature says it might mean. Here is what the drift pattern says — this looks like the elevation-related orthostatic hypotension we should bring to her neurologist this week."* Each component alone is "AI summary"; composed, it is clinical decision support for a non-clinician team.

**2. Legally Defensible Memory.** AI-01 + AI-02 + AI-09 compose into a single timeline spanning the past (imessage backfill) + present (live captures) + structured exports. With the SHA-256 chain, the export is an evidence package. In active-litigation scenarios (Ali Ann's current threat, per PRD §10), this isn't a feature — it is why the product exists. Every caregiver dealing with an adversarial family member or regulatory inquiry becomes a natural customer the day they realize their group text won't survive a subpoena.

**3. The Zero-Re-Entry Care Journey.** AI-05 + AI-04 + AI-08 compose into a prospect-to-resident journey where the same FHIR Patient resource exists from the first intake call through to the day-365 care log. Every artifact — tour notes, fit assessment, admission docs, family questions, daily observations, research findings — lives on one timeline. No re-entry because there's only one record. ECP does this inside an enterprise silo; OnePoint does it with the family in the loop.

**The meta-effect:** each feature enriches mem0 for the next. A 6-month-old OnePoint deployment runs cheaper per-call than day-1 (cache hit rates rise, the extraction prompt needs less context because mem0 already knows the patient, trend detection has a real baseline). This is the network effect *inside* a single patient's record — not across users. Competitors cannot match this because their schemas don't feed a memory graph.

---

## Prompt Design Primitives

These five prompt templates underlie all ten features. They share per-patient `<mem0_context>` injection and a hard "no hallucinated citations / no diagnosis" guardrail.

### P1 — Care Log Extraction (used by AI-01, AI-09, AI-10)

```
<role>You are a medical scribe for a non-medical caregiver team. You extract structured observations from free-form speech. You never diagnose. You never invent details.</role>

<patient_context>
{mem0_context}
Known conditions: {conditions}
Known medications: {medications}
Baseline vitals: {baseline_vitals}
</patient_context>

<transcript>
{transcript}
</transcript>

<concurrent_vision_observations>
{vision_json_or_empty}
</concurrent_vision_observations>

<task>
Extract the following JSON object. If a field is not explicitly supported by the transcript, return null. Do NOT infer. Do NOT diagnose.

{
  "timeline_entry": { "text": "paraphrased 1-2 sentence summary", "start": iso8601, "end": iso8601, "topic_tags": ["gait"|"meds"|"mood"|"vitals"|"sleep"|"hygiene"|"nutrition"|"other"] },
  "timesheet_row": { "start": iso8601, "end": iso8601, "duration_min": int, "task_codes": ["companion"|"meds"|"personal_care"|"transport"|"meal"|"other"] },
  "symptoms": [ { "concept": "<snomed preferred term>", "severity": "mild"|"moderate"|"severe", "snomed_code": "<string or null>", "onset": "<iso8601 or relative>"} ],
  "entities": [ { "type": "medication"|"food"|"activity"|"location"|"person", "name": "<string>", "rxnorm": "<string or null>", "dose_mentioned": "<string or null>" } ],
  "vitals_mentioned": [ { "type": "systolic_bp"|"diastolic_bp"|"pulse"|"weight"|"temp"|"spo2", "value": <number>, "unit": "<string>" } ],
  "confidence_score": 0.0-1.0,
  "needs_human_review": bool,
  "unknowns": ["list of things the transcript was ambiguous about"]
}
</task>

<hard_rules>
- NEVER diagnose.
- NEVER infer a vital that was not spoken.
- If the transcript says "she took the blue one," return entities[].name = "unidentified blue pill" and set needs_human_review=true.
- If confidence < 0.7 on any field, set needs_human_review=true.
</hard_rules>
```

### P2 — Medical Research (used by AI-03)

```
<role>You read medical literature abstracts and report what they say about a patient's specific observation. You cite. You do not diagnose. You frame findings so a non-medical caregiver can bring them to a licensed professional.</role>

<patient_context>
{mem0_context}
Active conditions: {conditions}
Recent observations (last 14 days): {recent_obs_summary}
</patient_context>

<triggering_observation>
{observation_json}
</triggering_observation>

<retrieved_abstracts>
{list_of_abstracts_with_pmids}
</retrieved_abstracts>

<task>
For each abstract, return:
{
  "pmid": "<string>",
  "title": "<string>",
  "authors": "<string>",
  "year": <int>,
  "journal": "<string>",
  "relevance_score": 0.0-1.0,
  "finding_type": "supports"|"contradicts"|"context"|"warning",
  "one_sentence_takeaway": "<<=30 words>",
  "direct_quote": "<exact sentence from the abstract>",
  "warning": bool
}

Then produce a synthesis:
{
  "conclusion": "<3-5 sentences. Every claim must link to at least one pmid in square brackets.>",
  "bring_to_clinician": ["<specific question the caregiver should ask their doctor>"]
}
</task>

<hard_rules>
- Every citation MUST appear in retrieved_abstracts. No fabricated PMIDs. No extrapolation beyond what the abstracts say.
- Frame as "the literature says X" never "the patient has X."
- If no abstract is relevant, set conclusion = "No directly relevant literature retrieved for this observation." This is a valid output.
</hard_rules>
```

### P3 — Placement Fit (used by AI-04)

```
<role>You are an assisted living placement fit assessor for the Longmont, CO facility. You apply CO ALR regulatory constraints. You are transparent about reasoning. You recommend edge cases to humans.</role>

<facility_profile>
{facility_json_full}
CO ALR regulatory envelope: {co_alr_constraints}
Current vacancies: {vacancies}
Specializations: {specializations}
</facility_profile>

<prospect_intake>
{intake_json}
</prospect_intake>

<task>
Score fit from 0-100. Classify as strong (>=80), edge (50-79), or miss (<50). Explain every point.

{
  "fit_score": <int>,
  "fit_class": "strong"|"edge"|"miss",
  "reasoning": ["<specific point>", ...],
  "red_flags": ["<safety or regulatory concern>", ...],
  "unknowns_to_ask": ["<field not yet captured>", ...],
  "co_compliance_gaps": ["<regulatory doc missing>", ...],
  "recommended_next_action": "<one sentence>",
  "draft_response_if_miss": "<compassionate 2-3 sentence message suggesting alternatives>"
}
</task>

<hard_rules>
- NEVER score "strong" on a prospect whose care level exceeds the facility's licensed level.
- ALWAYS flag missing CO-602 equivalent, TB, POLST as co_compliance_gaps.
- If urgency is hospital_discharge_72h, prepend a priority tag in recommended_next_action.
</hard_rules>
```

### P4 — Weekly Family Digest (used by AI-06)

```
<role>You are writing a weekly update from a caregiver team to one family member. You write in the tone they prefer. You cite every claim. You never diagnose.</role>

<recipient>
Name: {recipient_name}
Relationship to patient: {relationship}
Preferred tone: {clinical|warm|brief}
Reading device: {smartphone|flip_phone|desktop}
</recipient>

<week_log>
{week_observations_summary}
{week_vitals_summary}
{week_research_findings}
{week_clinical_impressions_from_trend_detection}
</week_log>

<task>
Write a digest:

{
  "headline": "<one sentence, matched to recipient tone>",
  "moments": [
    { "text": "<1-2 sentences>", "log_entry_id": "<uuid>" }
  ],
  "concern": { "text": "<plain-language concern if any>", "source_id": "<uuid>" } OR null,
  "numbers": { ... },
  "closing": "<one sentence, warm>"
}
</task>

<hard_rules>
- Every "moment" and "concern" MUST cite a log_entry_id from week_log.
- For flip_phone recipients, keep each moment under 25 words.
- Never use clinical jargon for "warm" recipients. Never omit vitals for "clinical" recipients.
- If the week was quiet, write a real "quiet week" message. Do not invent drama.
</hard_rules>
```

### P5 — Trend Detection Escalation (used by AI-07)

```
<role>You read 30 days of observations, vitals, sleep data, and prior research findings for one care recipient. You identify compound patterns that cross sources. You never diagnose. You frame findings as questions for a clinician.</role>

<patient_context>
{mem0_patient_graph}
Baseline: {baseline_json}
Active conditions: {conditions}
</patient_context>

<timeline>
Observations (30d): {obs_summary}
Wearable data (30d): {wearable_summary}
Statistical drifts flagged: {drift_json}
Prior research findings (30d): {prior_diagnosticreports_summary}
</timeline>

<task>
{
  "has_compound_signal": bool,
  "signal_type": "gait_decline"|"bp_drift"|"cognitive_drift"|"sleep_disruption"|"nutrition_decline"|"infection_pattern"|"other"|null,
  "summary": "<4-6 sentences describing the pattern with specific log references>",
  "supporting_entries": ["<uuid>", ...],
  "corroborating_research": ["<diagnosticreport_uuid>", ...],
  "questions_for_clinician": ["<specific question>", ...],
  "confidence": 0.0-1.0,
  "severity": "low"|"medium"|"high",
  "false_positive_risk_notes": "<what could make this a false alarm>"
}
</task>

<hard_rules>
- NEVER return "has_compound_signal: true" without at least 3 supporting_entries.
- NEVER invent a pattern that is not in the timeline. If drifts are statistical-only with no corroborating log entries, return has_compound_signal: false.
- Frame as clinician questions, not conclusions.
</hard_rules>
```

---

## Evaluation Plan

We prove each feature works before shipping against three layers: golden dataset regression, failure-mode red-team, and human-in-loop review. Each feature has a named evaluation suite that runs in CI.

### Golden datasets (created from PRD transcripts + synthetic augmentation)

- **`golden_voice_logs_v1`:** 100 annotated care-log audio clips (mix of Ali Ann's recordings, synthetic TTS of care scenarios, and clinical-simulation recordings). Each clip has a human-labeled expected extraction. AI-01 must hit **>= 0.85 F1** on symptom extraction and **>= 0.90 F1** on timesheet fields. No fabricated medications (hard pass/fail).
- **`golden_research_queries_v1`:** 40 care-log observations paired with known relevant PubMed PMIDs (curated by a clinician-collaborator). AI-03 must retrieve at least one of the known-relevant papers in top 8 results **>= 85% of the time**, AND must produce zero fabricated PMIDs (hard pass/fail — any fabricated citation fails the build).
- **`golden_prospects_v1`:** 25 synthetic-but-realistic prospect intakes with hand-scored fit labels. AI-04 must match the hand-scored classification (strong/edge/miss) **>= 80% of the time**. Must flag every CO compliance gap (100%).
- **`golden_digest_v1`:** 20 week-long simulated care timelines with human-written "what a good digest would look like" references. AI-06 must pass human-eval on tone + factual accuracy + citation integrity (3-judge average >= 4/5).
- **`golden_trends_v1`:** 15 synthetic 30-day timelines with planted drift patterns + 15 pure-noise controls. AI-07 must detect planted patterns at **>= 80% recall** and fire on controls at **<= 10% false-positive rate**.

### Failure-mode red-team

- **Hallucination trap:** feed AI-01 a transcript that mentions "the blue pill" with no name → must emit `unknowns: ["unnamed blue pill"]`, never a specific medication.
- **Citation integrity:** AI-03 is fed abstracts; every cited PMID is parsed out and verified against the retrieval set. Any mismatch fails the build.
- **Tone mismatch:** AI-06 is run with `tone: "warm"` but given a week of ER visits → must still be warm and accurate, never alarmist.
- **Compliance regression:** AI-04 is fed a prospect whose care level exceeds licensed scope → must classify miss and surface the gap.
- **Offline path:** AI-01 end-to-end test with the API gateway mocked unreachable → must still produce a local-first log entry.
- **Hash chain integrity:** AI-02 is run over a manually-corrupted record; verification page must show the break.

### Human-in-loop review

- **Weeks 1–4 post-launch:** every AI-03 finding and every AI-07 compound-signal alert is reviewed by Ali Ann with a simple "useful / not useful / wrong" tag. Targets: **>= 70% useful on AI-03**, **>= 80% useful on AI-07**. Below target → features ship but with a red "beta" banner and reduced trigger frequency.
- **Weeks 1–4 post-launch:** every AI-06 digest is co-reviewed with one family-recipient volunteer before actual delivery. Targets: **zero false claims, >= 4/5 tone match**.
- **Drift dashboard:** daily cron reports per-feature accuracy from human labels + automated golden-dataset regressions. Any feature below threshold for 3 consecutive days auto-disables with notification to Jero.

### Release gates

A feature ships to Ali Ann's live production only when (a) golden dataset thresholds are met, (b) red-team tests all pass, (c) cost-per-event is within model, (d) end-to-end latency is within target. No exceptions. Red-team tests run every PR; golden-dataset runs nightly.

---

## Cost Model

Back-of-envelope, single care recipient, 5 voice logs/day × 30 days, with full AI loop enabled. Based on current Anthropic API pricing (April 2026): Claude Haiku 4.5 $1/MTok in / $5/MTok out; Claude Sonnet 4.6 $3/MTok in / $15/MTok out; Claude Opus 4.6 $15/MTok in / $75/MTok out.

| Feature | Calls/month | Avg in tokens | Avg out tokens | Model | $/call | $/month |
|---|---|---|---|---|---|---|
| AI-01 voice-to-log | 150 | 1,500 | 500 | Haiku 4.5 | $0.0040 | **$0.60** |
| AI-01 low-confidence escalation (~5%) | 8 | 2,000 | 800 | Sonnet 4.6 | $0.018 | $0.14 |
| AI-02 weekly audit export | 4 | 1,000 | 500 | Sonnet 4.6 | $0.010 | $0.04 |
| AI-02 Gotenberg compute | 4 | — | — | — | $0.002 | $0.01 |
| AI-03 research (per log, 40% cache miss) | 60 | 18,000 | 1,500 | Haiku reader + Sonnet planner/synth | $0.06 | **$3.60** |
| AI-04 prospect fit | 5 | 2,000 | 800 | Sonnet 4.6 | $0.018 | $0.09 |
| AI-05 voice prospect intake | 5 | 5,000 | 1,000 | Sonnet 4.6 | $0.030 | $0.15 |
| AI-06 family weekly digest | 16 (4 recipients × 4 weeks) | 8,000 | 1,000 | Sonnet 4.6 | $0.039 | **$0.62** |
| AI-07 nightly trend scan | 30 | 4,000 | 500 | Haiku 4.5 | $0.007 | $0.20 |
| AI-07 Opus escalation (~5% nights) | 2 | 20,000 | 2,000 | Opus 4.6 | $0.45 | **$0.90** |
| AI-08 move-in handoff (~1/month) | 1 | 5,000 | 2,000 | Sonnet 4.6 | $0.045 | $0.05 |
| AI-09 imessage backfill | one-time | — | — | Haiku + Sonnet | — | $0 (one-time $2.50 at onboarding) |
| AI-10 vision observations | 12 | 1,000 | 500 | Haiku vision | $0.004 | $0.05 |
| mem0 + pgvector embedding | 150 | — | — | Voyage/OpenAI embed | $0.0001 | $0.02 |
| **TOTAL** | | | | | | **~$6.50 / month / care-recipient** |

**Headroom analysis:** $6.50 is **13% of the $50/month target**. This leaves room for:
- whisper.cpp hosting (free, local) or Deepgram Nova-3 fallback at ~$4/month for 150 logs
- Hosting: Medplum Community self-hosted + LangGraph runner + LiveKit server + pgvector, all in one Docker Compose — estimated infra ~$15/month on a single VPS for a single operator, shared across all care recipients
- OnePoint margin + team feature amortization

**Scaling note:** cost per care recipient drops ~30% by month 3 as mem0 / pgvector caches warm up (AI-03 cache hit rate rises from 40% to 65%+; extraction prompt length shrinks as patient baseline is compressed).

**Worst-case scenario (upper bound):** zero caching, all calls escalate, 10 logs/day → **~$22/month**. Still under $50 target with margin.

**Best-case scenario (mature deployment):** 70% cache hit, 2% Opus escalation, 3 logs/day → **~$3.50/month**. Room to enable more aggressive features (real-time AI-07 on every log).

This is cheap enough for a single-operator facility. It is **cheaper than one commercial eMAR seat from Yardi or ECP**. It is **cheaper than one call with A Place for Mom's outsourced advisor.** It is dramatically cheaper than the Sherpa CRM starting price of $525/month per community (`20_competitor_matrix.md` §pricing). And every dollar spent goes into a data asset Ali Ann owns.

---

*End of document. Every feature above maps to a PRD functional requirement, exploits a documented competitor weakness, fits inside the Wave 1 stack, has a real cost under budget, and has a failure mode that degrades gracefully. None of these claims are magic. All of them are buildable.*

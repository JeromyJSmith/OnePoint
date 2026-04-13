# META AGENT — Next Steps

**Date:** 2026-04-11
**Purpose:** Concrete, sequenced actions from research to execution.

---

## TODAY (pre-Saturday)

### ✅ Already Done
- PRD locked (`OnePoint_PRD.md` v0.1)
- 9 research documents produced and cross-validated
- QA report issued
- Stack decision made (Medplum + Krayin + LiveKit + LangGraph + Better-Auth + HTMX + Gotenberg)

### 🛑 Blocking before Saturday (5 min)
- [ ] **Verify Medplum compliance page live.** Open https://www.medplum.com/docs/compliance → screenshot → paste verbatim compliance claim into `11_oss_landscape.md` §A.

### 📄 Read before Saturday
- [ ] `50_onepoint_strategy.md` — the 15-minute elevator
- [ ] `30_gap_analysis.md` §Two Segment Opportunities
- [ ] `40_system_architecture.md` §The V0 Cut (week 1–4)
- [ ] `50_onepoint_strategy.md` §Critical Open Questions (these ARE the Saturday agenda)

---

## SATURDAY NIGHT — Working Session with Ali Ann

**Goal:** answer the 7 Critical Open Questions from `50_onepoint_strategy.md`. Nothing else.

**Setup (before she arrives):**
- [ ] Print or screen-share `30_gap_analysis.md §Segment Opportunity: The Orphaned Small Operator`
- [ ] Have the existing shared spreadsheet open (the "broken gear" one from Call 1) — this is v0's on-ramp
- [ ] Have `50_onepoint_strategy.md §Week-by-Week` visible so the plan is real, not abstract

**Questions to answer in session (bring to consensus):**
1. Which care recipient is buyer zero for the care-log side? Connie (acute, this week)? Ali Ann's dad (parallel)? Both?
2. What's the Longmont facility's exact name, address, license type, current vacancy count, price tier? (This data becomes FR-37 the next day.)
3. Which sister specifically needs the low-tech web surface? Name + device + comfort level. (This person becomes FR-7's user-zero.)
4. Is Ali Ann willing to self-host v0 (laptop/docker-compose) or does she want cloud from day one?
5. Who is the medical power of attorney for Connie? (FR-28 requires explicit authorization before records ingest.)
6. What's the litigation threat's timeline? (Determines whether FR-30/31/32 ships week 1 or week 4.)
7. What's the realistic cadence Ali Ann can meet with Jero over the next 4 weeks? (Determines the v0 cut.)

**Leave the session with:**
- [ ] A signed-off v0 scope (what ships week 1, 2, 4)
- [ ] The Longmont facility profile data
- [ ] Explicit consent for iMessage extraction from whoever is on the team
- [ ] A calendar of the next 4 working sessions

---

## WEEK 1 — First Usable Slice

**Goal:** Ali Ann logs one voice note per shift and her sisters can read it via a web link.

- [ ] **Day 1:** Provision Medplum self-host on docker-compose (reference: https://www.medplum.com/docs/self-hosting/install-on-ubuntu)
- [ ] **Day 1:** Stand up Better-Auth magic-link web surface (HTMX-rendered, no SPA)
- [ ] **Day 2:** Wire local-stt-mcp (whisper.cpp) → Medplum FHIR Observation POST
- [ ] **Day 2:** Build the "hit record" page (single HTML page, one button)
- [ ] **Day 3:** Seed Connie as a Medplum `Patient` resource + `CarePlan`
- [ ] **Day 3:** Build the read-only timeline view for the low-tech sister link
- [ ] **Day 4:** Ship week-1 v0 to Ali Ann; she logs her first real shift
- [ ] **Day 5:** Debrief; fix whatever broke; mark SM-1 day 1 of 14.

**Revisit these specific research items during week 1:**
- [ ] R2: verify CDC NCHS segment-size source
- [ ] R3: clean AI-03 cost paragraph

---

## WEEK 2 — Research Agent + Legal Export

- [ ] Wire LangGraph research agent: log entry → Europe PMC query → cited finding back to timeline
- [ ] Ship `31_ai_advantage.md §AI-02` — legal-grade export via Gotenberg with SHA-256 hash chain
- [ ] First real litigation-ready export run (even if unused, it exists)
- [ ] Start tracking SM-3 (group text volume drop)

---

## WEEK 3 — Krayin Stand-Up + Shadow Patient Pattern

- [ ] Provision Krayin on same docker-compose
- [ ] Build the Gateway service (thin TS/Fastify) that bridges Krayin events → Medplum
- [ ] Ship the shadow-Patient pattern: Krayin "Qualified" lead → Medplum Patient (prospective state)
- [ ] Ship the Longmont facility profile page (FR-37, FR-38) — shareable link, QR, mobile-first
- [ ] **Deliverable:** Ali Ann can capture a prospect by voice and share a facility page same day.

---

## WEEK 4 — Move-In Handoff + First Tenant Target

- [ ] Ship the atomic move-in transaction (shadow Patient → active resident, CarePlan activated)
- [ ] All P0 user stories from PRD now shippable
- [ ] First prospect in the Longmont pipeline (target: SM-7 = 5 leads in 30 days)
- [ ] First audit export reviewed by an attorney for legal defensibility

---

## MONTH 2 — Biometrics + Dashboard + Trend Detection

- [ ] Oura Ring integration (FR-16, AI-07)
- [ ] Dashboard with BP/weight/sleep trends (FR-24)
- [ ] Trend detection agent (AI-07)
- [ ] Family weekly digest synthesis (AI-06)
- [ ] SM-2 check: 2 sisters viewing web surface weekly × 4 weeks
- [ ] First tour scheduled through OnePoint for Longmont (target: SM-8)

---

## MONTH 3 — Close the Loop

- [ ] **SM-6 checkpoint (HEADLINE METRIC):** at least one qualified tenant moves into the Longmont facility through OnePoint pipeline.
- [ ] If YES → double down on placement pipeline, start second facility outreach
- [ ] If NO → execute the decision tree in `50_onepoint_strategy.md §Decision Tree`
- [ ] iMessage backfill shipped (FR-20–22, AI-09)
- [ ] HIPAA records link path live for at least one family (FR-27, FR-28)

---

## ONGOING — Do Not Drop These

1. **Ali Ann's dad remains her constraint.** Never schedule a session that forces her to choose between her dad and OnePoint. The tool must fit around her, not the other way around.
2. **Connie is the acute case.** Every week without a usable voice log is a week Connie's care is happening on group text. Speed > polish.
3. **The litigation threat is today.** FR-30/31/32 is not optional and not a future milestone.
4. **Longmont placement is revenue.** Every week without a move-in is lost revenue for Ali Ann. Treat it as a first-class metric, not a side bet.

---

## Research Still Outstanding

Items the META AGENT did not fully close and should be picked up before any pricing/GTM decisions:

1. **Real buyer pricing test** — one conversation with a single-operator assisted living owner outside of Ali Ann's network. Replaces the $50/care-recipient assumption.
2. **Legal review of the research-agent output** — is "cited peer-reviewed literature" presented to a non-medical caregiver a liability exposure? Retain a healthcare attorney for a 1-hour consult.
3. **CO ALR regulatory field set (FR-46)** — direct consult with Colorado CDPHE or a licensed ALR administrator to confirm the required document set for admission.
4. **TCPA compliance for placement outreach** — the anti-APFM positioning is only credible if OnePoint's own outreach is TCPA-clean.
5. **Thin competitive surfaces** — Ianacare, Cariloop, CircleOf, Roobrik need interview-based research because their public review surfaces are inadequate.

---

## When to Re-Run the META AGENT

Trigger a fresh META AGENT orchestration when:
- A real buyer conversation invalidates a core assumption
- A competitor ships a voice-first capture or family-to-facility bridge
- The regulatory environment shifts (new HIPAA guidance, CO ALR rule change)
- SM-6 fails at month 3 (this is a pivot trigger)
- Founder bandwidth changes materially (Ali Ann's dad stabilizes → more hours; Connie declines → fewer hours)

---

## Final Word

The single most important property of this body of work is that **OnePoint is buildable by a solo founder in constrained bandwidth because 95% of the stack already exists**. The META AGENT's job was to prove that. It did. What remains is execution, not discovery.

# META AGENT — Execution Log

**Project:** OnePoint platform intelligence pipeline
**Date:** 2026-04-11
**Orchestrator:** META AGENT (Claude Opus 4.6)
**Directive:** Find existing leverage before building anything. Minimize custom engineering.

---

## Agent Team Deployed

| # | Agent | Scope | Wave | Output | Status |
|---|-------|-------|------|--------|--------|
| 1 | SKILL_DISCOVERY_AGENT | Local skills + MCP servers + skills.sh + GitHub | 1 | `10_skill_landscape.md` | ✅ |
| 2 | OSS_RESEARCH_AGENT | Medical, CRM, AI, voice, auth, research, export OSS | 1 | `11_oss_landscape.md` | ✅ |
| 3 | COMPETITOR_AGENT | 16 competitors across care + placement segments | 1 | `20_competitor_matrix.md` | ✅ |
| 4 | REVIEW_INTELLIGENCE_AGENT | G2/Capterra/Reddit/forums/app stores | 1 | `21_review_intelligence.md` | ✅ |
| 5 | GAP_ANALYSIS_AGENT | Fuse PRD + competitors + reviews → named gaps | 2 | `30_gap_analysis.md` | ✅ |
| 6 | AI_ADVANTAGE_AGENT | AI-native feature design w/ real cost model | 2 | `31_ai_advantage.md` | ✅ |
| 7 | SYSTEM_ARCHITECT_AGENT | Full architecture incl. Medplum↔Krayin bridge | 2 | `40_system_architecture.md` | ✅ |
| 8 | SYNTHESIS_AGENT | Single strategy document, traceable to upstream | 3 | `50_onepoint_strategy.md` | ✅ |
| 9 | QA_AGENT | Audit all 9 docs for fluff, contradictions, hallucinations | 4 | `99_qa_report.md` | ✅ |

---

## Wave Sequencing

```
Wave 1 (parallel, 4 agents, independent)
├── Skill Discovery ────┐
├── OSS Research ───────┤
├── Competitor Matrix ──┤
└── Review Intelligence ┘
            ↓
Wave 2 (parallel, 3 agents, require Wave 1)
├── Gap Analysis ───────┐  (needs competitors + reviews)
├── AI Advantage ───────┤  (needs competitors + reviews + skills + OSS)
└── System Architecture ┘  (needs skills + OSS)
            ↓
Wave 3 (sequential, requires Waves 1+2)
└── Synthesis
            ↓
Wave 4 (sequential, audit)
└── QA
            ↓
META (final deliverables)
```

Total agent count: **9**. Parallelism exploited in Waves 1 and 2 (7 of 9 agents ran concurrent with at least one peer).

---

## Critical Findings by Phase

### Phase 1 — Skill Discovery
- User already has ~240 local skills in `~/.agents/skills/` including direct hits on voice-ai-integration, rag-agent-builder, prospect, legal-risk-assessment, compliance-tracking, meeting-record-system.
- Top 3 external MCP picks identified with install commands: `local-stt-mcp`, `pubmed-search-mcp`, `fhir-mcp-server`.
- 55 entries in full catalog, every one with a real URL + FR mapping.

### Phase 2 — OSS Research
- **Stack decision finalized:** Medplum + Krayin + LiveKit Agents + whisper.cpp + LangGraph + mem0 + pgvector + Better-Auth + HTMX + Gotenberg + Europe PMC + OpenAlex.
- **Key rejection:** Twenty, EspoCRM, SuiteCRM, Plane all AGPL — rejected as SaaS landmines. Krayin (MIT) is the only viable modern kanban CRM.
- **Lucia flagged as deprecated** (Mar 2025); Better-Auth replaces.

### Phase 3 — Competitor Matrix
- **Market bifurcation confirmed:** care coordination vs. placement CRM, almost no overlap.
- **Consolidation event:** Aline = Enquire + Glennis + Sherpa (2023).
- **Bridge gap finding:** ECP is the only competitor that credibly spans placement → care log, but its bridge is *operator-to-operator* (licensed facility staff), not *family-to-facility* (Ali Ann's segment).
- **A Place for Mom vulnerable:** $6M TCPA settlement + Senate Aging Committee probe.

### Phase 4 — Review Intelligence
- **15 complaint clusters** built from ~150–200 real reviews across 10+ sources.
- **Top complaints:** data loss, click-burden (Yardi eMAR = 11min/resident), clock-in/GPS betrayal (unpaid wages), trust failure (APFM lead reselling), low-tech family exclusion (answered with "just use WhatsApp").
- **Latent demand signal:** every complaint cluster maps to a OnePoint FR. The rage is the validation.

### Phase 5 — Gap Analysis
- **5 named gaps** with severity, evidence, defensibility, FR mapping:
  1. Voice-first capture (5/5) — click-burden kill
  2. Low-tech family inclusion (5/5) — flip-phone sister surface
  3. Legal-grade audit for non-medical companion (5/5) — Ali Ann's litigation
  4. Per-log-entry medical research agent (4/5) — category-defining
  5. Single-facility owner-operator placement bridge (5/5) — family-to-facility wedge
- **Anti-goals** declared: no enterprise chains, no EMR replacement, no diagnostic agent, no lead marketplace, no EVV/Medicaid, no SPA drift.
- **Segment sizing:** ~30,600 Residential Care Communities per CDC NCHS (flagged by QA for verification); $30M–$85M ARR floor for OnePoint's target segment.

### Phase 6 — AI Advantage
- **10 features** designed with model/trigger/schema/cost/latency/failure-mode.
- **Total cost: ~$6.50/month/care-recipient** (13% of $50 budget target).
- **Model mix:** Haiku 4.5 for high-volume reading, Sonnet 4.6 for structuring, Opus 4.6 only for escalations (~5% of calls).
- **Three compound moats:** Predictive Care, Legally Defensible Memory, Zero Re-Entry Care Journey.
- Evaluation plan with 5 golden datasets and explicit release gates.

### Phase 7 — System Architecture
- **Single docker-compose** shipable v0. AWS us-west-2 + BAA cloud option.
- **Cost:** ~$45/mo self-host, ~$380/mo cloud (before AI spend).
- **Medplum ↔ Krayin integration:** shadow-Patient pattern — a Krayin "Qualified" lead instantly creates a Medplum Patient in `prospective` state; every pipeline event attaches to that Patient; on move-in day a single atomic transaction flips state to `resident`. **Zero re-entry by architectural design, not integration glue.**
- **Week-by-week v0 cut** covering all P0 user stories through week 4.
- **17-item "do not build" list** enforcing the reuse-first philosophy.
- **15-row risk register** including honest Medplum and Krayin-specific risks.

### Phase 8 — Synthesis
- **Pitch script:** 148 words, sayable.
- **Three moats:** The Compound Loop, Trust Posture as Legal Commitment, Velocity Asymmetry.
- **Decision tree:** kill/pivot/double-down criteria at 30/60/90 days — concrete and uncomfortable.
- **7 Critical Open Questions** for Saturday's in-person session with Ali Ann.

### Phase 9 — QA
- **Verdict: PASS WITH MINOR REVISIONS.**
- Zero hallucinated URLs in 15-URL spot-check.
- Zero contradictions between strategy.md and architecture.md.
- **1 blocking revision for Saturday:** verify Medplum compliance page live (5 minutes).
- **2 non-blocking revisions:** CDC NCHS segment-size source verification, AI-03 cost-paragraph cleanup.

---

## Files Produced

```
/Users/ojeromyo/Desktop/OnePoint/research/
├── 10_skill_landscape.md       Skill Discovery
├── 11_oss_landscape.md         OSS Research
├── 20_competitor_matrix.md     Competitor Analysis
├── 21_review_intelligence.md   Review Intelligence
├── 30_gap_analysis.md          Gap Analysis
├── 31_ai_advantage.md          AI Advantage Design
├── 40_system_architecture.md   System Architecture
├── 50_onepoint_strategy.md     Strategy Synthesis
├── 99_qa_report.md             QA Audit
├── execution_log.md            ← this file
├── quality_report.md           META quality report
└── next_steps.md               Concrete execution list
```

---

## Orchestration Notes

- **Parallelism ratio:** 7 of 9 agents ran concurrent with at least one peer (78%).
- **Context discipline:** each agent received a self-contained briefing with required reading paths. No cross-agent chatter.
- **Output discipline:** every agent produced exactly one primary output file to the expected path.
- **No cascading failures:** Wave 2 agents received complete Wave 1 outputs; Wave 3 synthesis had the full corpus.
- **Tool economics:** total tool-use count across agents ~216; duration ~45 minutes wall-clock; parallelism cut sequential time from ~4 hours to ~25 minutes in the critical waves.

---

## What the META AGENT Did Right
1. **Skill discovery first** — exposed the 240 local skills before any custom-build reasoning began.
2. **Forced the stack decision in Phase 2** — no "consider X or Y" menus; Wave 2 agents inherited concrete components.
3. **Wave 2 parallelism** — Gap Analysis, AI Advantage, and System Architecture ran concurrent because their upstream dependencies overlapped but didn't block.
4. **QA as a gate, not a formality** — the QA report found a live blocking issue (Medplum compliance page verification) that would have embarrassed the Saturday session.

## What the META AGENT Would Do Differently
1. **Run a Phase 4a** — specifically interview Ali Ann for the gaps Review Intelligence couldn't reach (Ianacare, Cariloop, CircleOf, Roobrik had thin public review surfaces).
2. **Commission a pricing-sensitivity test** earlier — the $50/care-recipient AI budget is a founder assumption; one real buyer conversation would replace it with truth.
3. **Spawn a dedicated LEGAL_AGENT** — the CO ALR regulatory field set (FR-46), TCPA compliance for the placement side, and HIPAA BAA posture each deserve focused attention that neither OSS Research nor Architecture fully covered.

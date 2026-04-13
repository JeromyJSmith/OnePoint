# 10 — Skill Landscape for OnePoint

*Compiled: 2026-04-11. Sources: local `~/.agents/skills/` library (~240 skills), GitHub MCP server search, awesome-mcp lists, lobehub, mcpservers.org, pulsemcp.com.*

## Summary

OnePoint's functional requirements are **unusually well-served** by existing skills and MCP servers. The user already has a ~240-skill local library at `/Users/ojeromyo/.agents/skills/` that covers PRD-critical surfaces: voice AI, RAG, multi-agent research, document generation, dashboards, compliance tracking, and CRM/prospect pipelines — all installable via the `library` skill that's already active in this session. Externally, a mature ecosystem of MCP servers covers every integration the PRD calls out: PubMed / Europe PMC / OpenAlex for FR-10–15, FHIR/Medplum for FR-27, Oura Ring for FR-16, iMessage (`chat.db`) for FR-20, and local Whisper (MLX/Apple Silicon) for FR-1. The only gaps with no off-the-shelf fit are the **Longmont placement pipeline's regulatory fields** (FR-46), the **spreadsheet-mirror onboarding pattern** (FR-34–36), and the **low-tech-sister shared-link surface** (FR-7, NFR-7) — all three require custom OnePoint work. Everything else should be wired, not rebuilt.

## Top 3 Recommended Skills (USE THESE)

### 1. `local-stt-mcp` — Local Whisper.cpp transcription on Apple Silicon
- **Source:** https://github.com/SmartLittleApps/local-stt-mcp
- **Install:** `claude mcp add local-stt --command "npx local-stt-mcp"` (verify exact command at repo README; Apple Silicon optimised, fully on-device)
- **Why it's top pick:** OnePoint is voice-first (FR-1, FR-4, FR-5) AND needs offline tolerance (NFR-2) AND touches PHI (NFR-4, NFR-5). On-device Whisper is the only combination that satisfies all three without shipping audio to a third party. The user is on an Apple Silicon Mac — this is the native path.
- **Unlocks:** FR-1 (hit-record-and-talk), FR-3 (stream-of-consciousness parsing once text is extracted), FR-5 (hands-free capture), NFR-2 (offline), NFR-4 (privacy), NFR-5 (HIPAA posture).
- **Integration difficulty:** 2/5

### 2. `pubmed-search-mcp` — Multi-source biomedical literature MCP (40 tools)
- **Source:** https://github.com/u9401066/pubmed-search-mcp
- **Install:** `claude mcp add pubmed-search --command "uv run pubmed-search-mcp"` (Python/uv, per repo)
- **Why it's top pick:** Single server that unifies PubMed + Europe PMC + OpenAlex + CORE and exposes 40 tools including citation networks and PICO analysis. OnePoint's research agent (FR-10–15) needs exactly this coverage because Connie's case crosses Parkinson's, dementia staging, UTI differential, and elevation/BP — none of which resolves from a single database. Also addresses Research Item #3 in the PRD directly.
- **Unlocks:** FR-10, FR-11, FR-12 (cited), FR-13 (warning-pattern surfacing), FR-14 (literature framing), FR-15 (scope examples).
- **Integration difficulty:** 2/5

### 3. `fhir-mcp-server` (Momentum) — FHIR/Medplum natural-language clinical data
- **Source:** https://github.com/the-momentum/fhir-mcp-server
- **Install:** `claude mcp add fhir --command "uv run fhir-mcp-server" --env "MEDPLUM_URL=...,MEDPLUM_CLIENT_ID=..."`
- **Why it's top pick:** Directly answers PRD Open Question OQ-1 (which HIPAA-compliant medical records platform). Supports Medplum out of the box with OAuth2, full CRUD on FHIR resources, LOINC codes, and semantic document ingest. This collapses FR-27 (HIPAA link), FR-28 (authorization flow), and the records side of FR-25 (timeline merge) into a single integration instead of three.
- **Unlocks:** FR-27, FR-28, FR-25 (clinical events on timeline), plus resolves OQ-1.
- **Integration difficulty:** 3/5 (OAuth2 + Medplum tenant setup)

## Top 5 Shortlist

| # | Skill | Source | One-liner | OnePoint relevance |
|---|-------|--------|-----------|--------------------|
| 1 | `local-stt-mcp` | github.com/SmartLittleApps/local-stt-mcp | Local whisper.cpp STT, Apple Silicon | 5/5 (FR-1, NFR-2, NFR-5) |
| 2 | `pubmed-search-mcp` | github.com/u9401066/pubmed-search-mcp | PubMed+EuropePMC+OpenAlex, 40 tools | 5/5 (FR-10–15) |
| 3 | `fhir-mcp-server` | github.com/the-momentum/fhir-mcp-server | FHIR/Medplum natural-language bridge | 5/5 (FR-27, FR-28, OQ-1) |
| 4 | `imessage-query-fastmcp` | github.com/hannesrudolph/imessage-query-fastmcp-mcp-server | Safe read-only `chat.db` query with phone validation | 5/5 (FR-20, FR-21, FR-22) |
| 5 | `oura-ring-mcp` (mitchhankins01) | github.com/mitchhankins01/oura-ring-mcp | Oura Ring v2 API with human-readable insights | 5/5 (FR-16, FR-17, FR-19) |

## Full Catalog

Local skills live at `/Users/ojeromyo/.agents/skills/<name>/SKILL.md`; install via `/library install <name>`. External MCPs install via `claude mcp add` per each repo's README.

| Skill | Source | What it does | Integration difficulty | OnePoint relevance | Notes |
|---|---|---|---|---|---|
| `voice-ai-integration` | local: ~/.agents/skills/voice-ai-integration | STT + TTS provider patterns (Google, Whisper, etc.), voice-first app scaffolding | 2/5 | 5/5 (FR-1, FR-2) | Pairs with local-stt-mcp; provides the application-layer pattern |
| `funasr-transcribe` | local: ~/.agents/skills/funasr-transcribe | Local FunASR → timestamped markdown with diarization, supports mp4/mov/mp3/wav/m4a | 2/5 | 4/5 (FR-4, FR-20 audio) | Good for batch transcription of recorded call audio / backfill |
| `local-stt-mcp` | https://github.com/SmartLittleApps/local-stt-mcp | Local whisper.cpp MCP, Apple Silicon-optimised | 2/5 | 5/5 (FR-1, NFR-2, NFR-5) | Top pick #1 |
| `mlx-whisper-mcp` | https://github.com/kachiO/mlx-whisper-mcp | MLX-accelerated Whisper MCP for Apple Silicon | 2/5 | 4/5 (FR-1) | Alternative to local-stt-mcp |
| `listen-claude-code` | https://github.com/gmoqa/listen-claude-code | Voice input for Claude Code via local Whisper | 1/5 | 3/5 (dev ergonomics only) | Speeds up Jero's own build, not end-user |
| `pubmed-search-mcp` | https://github.com/u9401066/pubmed-search-mcp | 40-tool biomedical MCP: PubMed, Europe PMC, OpenAlex, CORE | 2/5 | 5/5 (FR-10–15) | Top pick #2 |
| `paper-search-mcp` | https://github.com/openags/paper-search-mcp | Arxiv + PubMed + bioRxiv + Europe PMC unified search/download | 2/5 | 4/5 (FR-10, FR-11) | Broader coverage, fewer medical-specific tools |
| `Scientific-Papers-MCP` | https://github.com/benedict2310/Scientific-Papers-MCP | Arxiv + OpenAlex real-time paper access | 2/5 | 3/5 (FR-11) | Thinner than pubmed-search-mcp |
| `pubmed-mcp-server` (cyanheads) | https://github.com/cyanheads/pubmed-mcp-server | NCBI E-utilities MCP: search, full text, citations, MeSH | 2/5 | 4/5 (FR-11, FR-12) | Solid PubMed-only fallback |
| `chat-with-arxiv` | local: ~/.agents/skills/chat-with-arxiv | Build research chat agents over papers | 2/5 | 3/5 (FR-13, FR-14) | Pattern layer above the retrieval MCPs |
| `deep-research-agent` | local: ~/.agents/skills/deep-research-agent | Multi-source research planning, source evaluation, report generation | 2/5 | 5/5 (FR-10–14) | Use as the orchestrator over pubmed-search-mcp |
| `research-management` | local: ~/.agents/skills/research-management | Manages ongoing research workflows | 2/5 | 3/5 (FR-10) | Useful for the per-log-entry trigger pattern |
| `rag-agent-builder` | local: ~/.agents/skills/rag-agent-builder | Vector DB + embeddings + retrieval strategies (hybrid, reranking, agentic) | 3/5 | 5/5 (FR-11, FR-25) | Use to ground research answers in Connie's own log history |
| `document-chat-interface` | local: ~/.agents/skills/document-chat-interface | Natural-language Q&A over PDFs, repos, emails | 2/5 | 4/5 (FR-31, FR-32) | Lets team query their own exported logs |
| `fhir-mcp-server` | https://github.com/the-momentum/fhir-mcp-server | FHIR/Medplum bridge, OAuth2, LOINC, CRUD | 3/5 | 5/5 (FR-27, FR-28, OQ-1) | Top pick #3 |
| `mcp-fhir` (flexpa) | https://github.com/flexpa/mcp-fhir | Alternative FHIR MCP implementation | 3/5 | 4/5 (FR-27) | Good fallback if Momentum server doesn't fit |
| `imessage-query-fastmcp` | https://github.com/hannesrudolph/imessage-query-fastmcp-mcp-server | FastMCP iMessage `chat.db` query, phone validation, attachments | 2/5 | 5/5 (FR-20, FR-21, FR-22) | Exactly the shape PRD §5.5 asks for |
| `imessage-mcp` (wyattjoh) | https://github.com/wyattjoh/imessage-mcp | Read-only `chat.db` MCP, search/browse conversations | 2/5 | 5/5 (FR-20) | Alternative; simpler surface |
| `jons-mcp-imessage` | https://github.com/jonmmease/jons-mcp-imessage | iMessage MCP with hybrid search + contact enrichment | 2/5 | 4/5 (FR-20, FR-21) | Contact enrichment helps the per-person consent UX (FR-22) |
| `oura-ring-mcp` | https://github.com/mitchhankins01/oura-ring-mcp | Oura v2 API MCP with readable insights | 2/5 | 5/5 (FR-16, FR-17, FR-19) | Human-readable output simplifies timeline merge |
| `oura-mcp-server` (hemantkamalakar) | https://github.com/hemantkamalakar/oura-mcp-server | Oura MCP for Claude Desktop | 2/5 | 4/5 (FR-16) | Alternative |
| `open-wearables` | https://github.com/the-momentum/open-wearables | Unified API over Garmin + Oura + Fitbit | 3/5 | 5/5 (FR-16, FR-18, OQ-3) | Best if OnePoint needs to support more than Oura |
| `prospect` | local: ~/.agents/skills/prospect | Apollo.io-backed ICP → ranked, enriched lead list | 1/5 | 4/5 (FR-39, FR-40, FR-45) | Re-aim at senior-living prospect intake instead of B2B |
| `enrich-lead` | local: ~/.agents/skills/enrich-lead | Apollo.io contact enrichment for any identifier | 1/5 | 4/5 (FR-39, FR-42) | Enrich decision-maker family contacts from a name |
| `apollo-io-mcp-server` (lkm1developer) | https://github.com/lkm1developer/apollo-io-mcp-server | Apollo.io MCP, 27 tools: leads, sequences, CRM | 2/5 | 4/5 (FR-41, FR-45) | Backs the `prospect` + `enrich-lead` skills directly |
| `apollo-io-mcp` (Chainscore) | https://github.com/Chainscore/apollo-io-mcp | 27-tool Apollo.io MCP, pipeline management | 2/5 | 4/5 (FR-41) | Alternative |
| `gitscrum-core/mcp-server` | https://github.com/gitscrum-core/mcp-server | Kanban + CRM + tasks + sprints + client CRM + invoicing via MCP | 3/5 | 5/5 (FR-41, FR-43, FR-44) | Closest thing to the FR-41 Kanban pipeline out of the box |
| `task-management` | local: ~/.agents/skills/task-management | Shared TASKS.md task tracking | 1/5 | 3/5 (shift handoffs) | Lightweight fallback for FR-8 / FR-9 |
| `task-manager` | local: ~/.agents/skills/task-manager | GitHub Issues-backed agent task manager | 2/5 | 2/5 | Useful for Jero's build, not for end users |
| `meeting-record-system` | local: ~/.agents/skills/meeting-record-system | Meeting notes + action items, Notion integration | 2/5 | 4/5 (FR-4, FR-33) | Direct match for shift-handoff pattern |
| `meeting-briefing-anthropic` | local: ~/.agents/skills/meeting-briefing-anthropic | Structured legal-relevant meeting briefings | 2/5 | 3/5 (FR-33) | Pattern for tour prep and family calls |
| `collaborative-document-creation` | local: ~/.agents/skills/collaborative-document-creation | Merge multi-author docs, version management | 2/5 | 4/5 (FR-30, FR-34–36) | Useful for the spreadsheet-mirror onboarding |
| `spreadsheet-processor` | local: ~/.agents/skills/spreadsheet-processor | Excel processing with formulas and formatting | 2/5 | 5/5 (FR-34, FR-35, FR-36) | Direct enabler of the spreadsheet-mirror onramp |
| `xlsx-processing-anthropic` | local: ~/.agents/skills/xlsx-processing-anthropic | Anthropic's reference XLSX skill | 2/5 | 4/5 (FR-34, FR-35) | Alternative spreadsheet surface |
| `interactive-dashboard-builder` | local: ~/.agents/skills/interactive-dashboard-builder | Self-contained HTML/Chart.js dashboards with filters | 2/5 | 5/5 (FR-24, FR-25, FR-47) | Ships the occupancy dashboard AND the low-tech-sister web surface |
| `pdf-processing-anthropic` | local: ~/.agents/skills/pdf-processing-anthropic | PDF read/write/OCR/form fill/extract | 1/5 | 5/5 (FR-31, FR-46) | Legal export + 602/POLST handling |
| `docx-processing-anthropic` | local: ~/.agents/skills/docx-processing-anthropic | Word doc create/read/edit | 1/5 | 4/5 (FR-31, FR-38) | Facility page export, attorney-ready logs |
| `audit-support` | local: ~/.agents/skills/audit-support | SOX-style control testing, sample selection, documentation | 2/5 | 4/5 (FR-30, FR-32, FR-46) | Repurpose the attribution/sample pattern for care-log defensibility |
| `compliance-tracking` | local: ~/.agents/skills/compliance-tracking | Track compliance requirements, audit prep | 2/5 | 5/5 (FR-46, NFR-5) | Direct fit for tracking which placement docs are collected |
| `compliance-anthropic` | local: ~/.agents/skills/compliance-anthropic | GDPR/CCPA, DPAs, data subject requests | 2/5 | 3/5 (NFR-4, NFR-5) | Background for self-host data-sovereignty story |
| `legal-risk-assessment-anthropic` | local: ~/.agents/skills/legal-risk-assessment-anthropic | Severity × likelihood risk framework | 2/5 | 4/5 (FR-32) | Frame for "this log matters, this one doesn't" triage in litigation |
| `legal-document-analyzer` | local: ~/.agents/skills/legal-document-analyzer | Analyze and extract from legal docs | 2/5 | 3/5 (FR-31) | Processes inbound waiver / POA docs |
| `legal-proposal-generator` | local: ~/.agents/skills/legal-proposal-generator | Generate structured legal service documents | 2/5 | 3/5 (FR-31, FR-38) | Usable for facility page + admission packet generation |
| `contract-review-anthropic` | local: ~/.agents/skills/contract-review-anthropic | Clause-by-clause contract review | 2/5 | 2/5 | Low — residency agreements only |
| `multi-agent-orchestration` | local: ~/.agents/skills/multi-agent-orchestration | CrewAI/AutoGen/LangGraph/Swarm orchestration patterns | 3/5 | 5/5 (FR-10, FR-13) | Backbone pattern for the per-log research agent |
| `distributed-task-execution` | local: ~/.agents/skills/distributed-task-execution | Parallel task execution across agents | 3/5 | 3/5 (FR-10 batch) | End-of-day batch research trigger |
| `user-research-synthesis` | local: ~/.agents/skills/user-research-synthesis | Synthesize qualitative research into themes/personas | 2/5 | 3/5 (SM-5) | Use to extract patterns from shift logs over time |
| `data-visualization` | local: ~/.agents/skills/data-visualization | Data viz patterns | 2/5 | 4/5 (FR-24) | Pairs with interactive-dashboard-builder |
| `financial-document-management` | local: ~/.agents/skills/financial-document-management | Invoice organizer / financial doc categorization | 2/5 | 3/5 (FR-46, FR-47) | Financial attestation tracking |
| `knowledge-management` | local: ~/.agents/skills/knowledge-management | Knowledge base organization | 2/5 | 3/5 (FR-25) | Patient history store |
| `data-context-extractor` | local: ~/.agents/skills/data-context-extractor | Extract structured data from raw text | 2/5 | 5/5 (FR-3, FR-4) | Stream-of-consciousness → timesheet row + log entry separation |
| `data-validation` | local: ~/.agents/skills/data-validation | Input validation patterns | 2/5 | 3/5 (NFR-6) | Guards the log-of-record |
| `whisper-mcp` (jwulff) | https://github.com/jwulff/whisper-mcp | Local whisper.cpp MCP (lightweight) | 2/5 | 3/5 (FR-1) | Lighter alternative |
| `Fast-Whisper-MCP-Server` | https://github.com/BigUncle/Fast-Whisper-MCP-Server | Faster-whisper high-perf MCP | 2/5 | 3/5 (FR-1) | Batch-transcription path |
| `audio-transcription-mcp` (pmerwin) | https://github.com/pmerwin/audio-transcription-mcp | Real-time Whisper transcription MCP | 2/5 | 3/5 (FR-1, NFR-3) | Real-time path if local-stt isn't enough |
| claude.ai Notion MCP (session) | already loaded | Create/query Notion pages for structured notes | 1/5 | 3/5 (FR-34, FR-35) | Spreadsheet-mirror backbone if Ali Ann's team prefers Notion |
| claude.ai Gmail MCP (session) | already loaded | Read/draft Gmail messages | 1/5 | 4/5 (FR-42, FR-45) | Family decision-maker coordination over email |
| claude.ai Google Calendar MCP (session) | already loaded | Calendar management | 1/5 | 4/5 (FR-43) | Tour scheduling + shift handoffs |
| claude.ai Linear MCP (session) | already loaded | Project/issue management | 1/5 | 3/5 (FR-41 backlog) | Internal OnePoint build tracking (not end-user) |
| claude.ai Slack MCP (session) | already loaded | Slack channels/threads/canvases | 1/5 | 2/5 | Weak fit — team is on group text, not Slack |
| claude.ai Vercel MCP (session) | already loaded | Deploy + logs | 1/5 | 4/5 (FR-7) | Deploy the low-tech-sister web surface |
| `infranodus` MCP (session) | already loaded | Knowledge-graph text analysis and RAG augmentation | 3/5 | 4/5 (FR-11, FR-13, SM-5) | Surface non-obvious symptom clusters across weeks of logs |
| `omega-memory` MCP (session) | already loaded | Persistent cross-conversation memory | 2/5 | 4/5 (FR-25) | Long-term patient memory across agent sessions |
| `pencil` MCP (session) | already loaded | Design editor for `.pen` files | 2/5 | 3/5 (FR-38) | Facility-page design source of truth |

**Total catalog entries: 55.**

## Gaps — no skill exists for these

1. **Colorado ALR regulatory field set (FR-46).** No MCP or skill carries the 602-equivalent, TB, POLST, physician attestation, and responsible-party form definitions for Colorado assisted living. This is custom schema + validation work. Ties to PRD Research Item #11.
2. **Spreadsheet-mirror onboarding pattern (FR-34–36).** No skill implements "read Google Sheet, create OnePoint mirror, stream changes both directions, never force migration." `spreadsheet-processor` handles the read/write primitives but the bidirectional-mirror-with-eventual-migration pattern is OnePoint-specific.
3. **Low-tech-sister web surface (FR-7, NFR-1, NFR-7).** No skill builds a WCAG-AA, zero-install, magic-link-auth, works-on-a-flip-phone-browser surface. Must be hand-built. Closest primitives: `interactive-dashboard-builder` (HTML shell) + a custom magic-link token route.
4. **Magic-link auth for care-logging (NFR-7).** No MCP exists. Magic-link libraries (passport-magic-login, SuperTokens) exist at the app layer but require custom integration. There's also the explicit caveat that magic links are ill-suited to automated agents — OnePoint must build the human-facing variant itself.
5. **HIPAA-compliant transcription pipeline posture.** Local Whisper via `local-stt-mcp` gives us the *posture* (on-device, no network), but there is no off-the-shelf skill that ships the BAA, audit logs, and access-review paperwork. That is operational, not code.
6. **iMessage consent UX (FR-22).** The iMessage MCPs give DB access but none ship the per-person consent capture flow the PRD mandates. Custom work.
7. **Longmont occupancy dashboard wired to the actual facility (FR-47).** `interactive-dashboard-builder` gives the shell; facility-specific data model is custom.
8. **SMS fallback for alerts (OQ-5).** No skill in the catalog addresses SMS delivery to the low-tech sister. Needs Twilio-class integration (not an MCP concern yet — or build a custom MCP wrapper over Twilio).
9. **Consumer-grade wearable unification beyond Oura/Garmin/Fitbit.** `open-wearables` covers three devices. Patch biosensors, wristband BP cuffs, and CGMs (all called out in FR-16, FR-18) have no existing MCP.

## Install / wire-up commands

**Prerequisite (session-level):** the `library` skill is already active in this session. Local skills install via `/library install <name>`. MCP servers install via `claude mcp add`.

```bash
# ─── Top 3 MCP servers ─────────────────────────────────────────────

# 1. Local Whisper STT (Apple Silicon) — FR-1, NFR-2, NFR-5
git clone https://github.com/SmartLittleApps/local-stt-mcp ~/repos/local-stt-mcp
cd ~/repos/local-stt-mcp && uv sync
claude mcp add local-stt --scope user -- uv --directory ~/repos/local-stt-mcp run local-stt-mcp

# 2. Multi-source biomedical literature — FR-10–15
git clone https://github.com/u9401066/pubmed-search-mcp ~/repos/pubmed-search-mcp
cd ~/repos/pubmed-search-mcp && uv sync
claude mcp add pubmed-search --scope user \
  --env "NCBI_API_KEY=$NCBI_API_KEY" \
  -- uv --directory ~/repos/pubmed-search-mcp run pubmed-search-mcp

# 3. FHIR / Medplum bridge — FR-27, FR-28, OQ-1
git clone https://github.com/the-momentum/fhir-mcp-server ~/repos/fhir-mcp-server
cd ~/repos/fhir-mcp-server && uv sync
claude mcp add fhir --scope user \
  --env "FHIR_BASE_URL=https://api.medplum.com/fhir/R4" \
  --env "FHIR_CLIENT_ID=$MEDPLUM_CLIENT_ID" \
  --env "FHIR_CLIENT_SECRET=$MEDPLUM_CLIENT_SECRET" \
  -- uv --directory ~/repos/fhir-mcp-server run fhir-mcp-server

# ─── Shortlist extras ──────────────────────────────────────────────

# iMessage backfill — FR-20–22
git clone https://github.com/hannesrudolph/imessage-query-fastmcp-mcp-server ~/repos/imessage-mcp
cd ~/repos/imessage-mcp && uv sync
claude mcp add imessage --scope user -- uv --directory ~/repos/imessage-mcp run imessage-query-fastmcp

# Oura Ring — FR-16, FR-17, FR-19
git clone https://github.com/mitchhankins01/oura-ring-mcp ~/repos/oura-ring-mcp
cd ~/repos/oura-ring-mcp && uv sync
claude mcp add oura --scope user --env "OURA_PAT=$OURA_PAT" \
  -- uv --directory ~/repos/oura-ring-mcp run oura-ring-mcp

# ─── Local skills (install via library) ────────────────────────────
/library install voice-ai-integration
/library install deep-research-agent
/library install rag-agent-builder
/library install multi-agent-orchestration
/library install interactive-dashboard-builder
/library install spreadsheet-processor
/library install pdf-processing-anthropic
/library install docx-processing-anthropic
/library install data-context-extractor
/library install compliance-tracking
/library install audit-support
/library install legal-risk-assessment-anthropic
/library install meeting-record-system
/library install document-chat-interface
/library install prospect
/library install enrich-lead

# Verify everything is wired
claude mcp list
/library list
```

**Post-install sanity checks:**

1. `local-stt` — transcribe a 30s voice memo → confirms FR-1 offline path.
2. `pubmed-search` — query "Parkinson's dementia elevation blood pressure" → confirms FR-10 returns citations.
3. `fhir` — OAuth2 handshake against a Medplum sandbox tenant → confirms FR-27 auth flow.
4. `imessage` — read-only query for one consenting contact → confirms FR-20 path and FR-22 consent boundary.
5. `oura` — pull last 24h readiness → confirms FR-16 data ingress.

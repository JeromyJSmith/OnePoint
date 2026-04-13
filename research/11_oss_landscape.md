# 11 — OSS Landscape for OnePoint

**Status:** v1 · Research Output
**Date:** 2026-04-11
**Author:** OSS_RESEARCH_AGENT
**Philosophy:** DO NOT BUILD FROM SCRATCH. This document picks the stack. Every line is a decision, not a menu.

---

## Executive Summary — The 5 Picks That Define OnePoint

1. **Medplum (Apache 2.0)** is the care-log and medical-records backbone. It is the only modern, TypeScript-native, FHIR-compliant, HIPAA/SOC2/HITRUST-certified open-source platform that ships a complete developer stack (auth, repository, bots, React components). It closes FR-27, FR-28, FR-29, FR-30, FR-31, FR-32 in one decision. Self-hosted Community tier is free.
2. **Krayin CRM (MIT)** is the tenant-placement pipeline. MIT license is non-negotiable for commercial SaaS, and Krayin is the only modern, MIT-licensed kanban CRM still actively developed (v2.2.0, March 2026). Every other viable CRM (Twenty, EspoCRM, SuiteCRM, Plane) is AGPL. We extend Krayin to close FR-41 through FR-48.
3. **LiveKit Agents (Apache 2.0)** is the voice-first capture layer. It is the only OSS framework that ships realtime STT + LLM + TTS + telephony + vision in one package, which is exactly the shape of FR-1 through FR-5 and FR-2 (vision). whisper.cpp (MIT) is the on-device transcription fallback for offline NFR-2.
4. **Better-Auth (MIT)** is authentication. Magic-link first-class, framework-agnostic, TypeScript, 27.8k stars, active. This is the only pick that actually satisfies NFR-7 ("shared link + pick-your-name") while still producing a defensible audit trail. Lucia is deprecated. Authelia is SSO, wrong shape.
5. **HTMX (BSD-2) + server-rendered pages** is the low-tech surface. FR-7 is a hard constraint: "if it doesn't work on a skeptical relative's old phone, it fails the requirement." Any React/Next.js SPA fails this test on day one. HTMX + server-rendered HTML is the entire UX for the low-tech sister; the native app (FR-6) layers on top.

---

## Stack Recommendation — This Is The Stack

| Layer | Pick | License | Why |
|---|---|---|---|
| Medical records / care log / audit trail | **Medplum** | Apache 2.0 | FHIR-native, HITRUST/SOC2/HIPAA, TypeScript, self-hostable, Apache (no AGPL trap) |
| Tenant placement CRM | **Krayin CRM** (extended) | MIT | Only actively maintained MIT kanban CRM; Laravel/Vue; custom pipeline stages trivial |
| Voice + vision capture | **LiveKit Agents** | Apache 2.0 | Realtime STT+LLM+TTS+WebRTC+vision+telephony in one framework |
| Offline / on-device transcription | **whisper.cpp** | MIT | Apple-Silicon-native, runs in WebAssembly, satisfies NFR-2 offline tolerance |
| Agent orchestration | **LangGraph** | MIT | Durable, stateful, human-in-the-loop, production-proven |
| Agent memory | **mem0** | Apache 2.0 | Simple API, production-ready, 52.7k stars. Letta is heavier than we need |
| Vector store | **pgvector** | PostgreSQL License | One database for everything. Medplum already runs Postgres. Qdrant is overkill for v0 |
| Auth | **Better-Auth** | MIT | Magic link, TypeScript, framework-agnostic, active |
| Low-tech web surface | **HTMX** + server-rendered HTML | BSD-2 | FR-7 hard constraint: works on any device, any vintage |
| Medical research retrieval | **Europe PMC REST** (primary) + **OpenAlex API** (enrichment) | Public APIs | Open license, no key required, commercial-friendly; NCBI/PubMed keeps rate limits too tight for per-log-entry triggering |
| PDF / export | **Gotenberg** | MIT | Dockerized API, HTML→PDF, merge/sign/PDF-A — exactly FR-31 legal export |
| Audit log integrity | **Medplum's built-in provenance + FHIR AuditEvent** | Apache 2.0 | Already in Medplum; no second system needed. Add SHA-256 chain for tamper-evidence |

**Database:** PostgreSQL 15+ (required by Medplum, used by Krayin via bridge, and by pgvector).
**Runtime:** Node.js / TypeScript (Medplum, Better-Auth, LiveKit Agents JS SDK, LangGraph JS).
**Deploy target:** Docker Compose for v0, Kubernetes later. Self-hostable end-to-end (NFR-4).

---

## Per-Category Analysis

### A. Care Logging / Medical Records (HIPAA-compliant)

| Project | License | What it solves | What it doesn't | Integration path | Verdict |
|---|---|---|---|---|---|
| **Medplum** (github.com/medplum/medplum, 2.3k stars, last release v5.1.7 Apr 2026) | Apache 2.0 | FHIR repo, auth, bots, React components, SOC2+HITRUST+HIPAA compliance program, self-host Community free | Not a clinical UI out of box — you build on top | Deploy self-hosted; model care logs as FHIR `Observation` + `Communication`; use Bots for research-agent triggers | **USE (core)** |
| HAPI FHIR (hapifhir/hapi-fhir, 2.3k stars, active) | Apache 2.0 | Java FHIR server toolkit | No auth, no UI, no bots, no app framework — library not platform | Would need to build everything Medplum already gives us | IGNORE |
| OpenMRS (openmrs/openmrs-core, 1.8k stars, active) | MPL 2.0 | Mature EMR for resource-constrained settings | Java/Maven stack, global-health-NGO focus, heavy, no FHIR-first design | Wrong shape for a voice-first log layer | IGNORE |
| OpenEMR (openemr/openemr, 5.1k stars, active) | GPL-3.0 | Full EHR + practice mgmt + billing | PHP monolith, ONC-cert focused, GPL-3 infects modifications | Wrong stack, wrong license for SaaS | IGNORE |
| LibreHealth | MPL 2.0 | OpenEMR fork | Lower activity than OpenEMR, same stack problems | — | IGNORE |

**HIPAA verification:** Medplum publicly advertises HITRUST, SOC2 Type II, ONC, HIPAA, and CFR Part 11 on `medplum.com/docs/compliance`. Citation: Medplum compliance docs. This is the only candidate with documented, audited HIPAA-grade controls as an OSS project. OpenMRS and OpenEMR make no HIPAA claims — they are "HIPAA-capable if you configure them right," which is not the same thing.

**Maps to:** FR-27, FR-28, FR-29, FR-30, FR-31, FR-32, NFR-4, NFR-5, NFR-6.

---

### B. CRM / Pipeline / Kanban

| Project | License | What it solves | What it doesn't | Integration path | Verdict |
|---|---|---|---|---|---|
| **Krayin CRM** (krayin/laravel-crm, 22.1k stars, v2.2.0 Mar 2026) | **MIT** | Leads, pipeline, kanban, email, custom fields, web forms | PHP/Laravel stack (separate from Medplum's TS stack); UI dated | Deploy as sidecar service; bridge to Medplum via webhooks on stage transitions; custom pipeline stages map to FR-41 | **USE (extend)** |
| Twenty CRM (twentyhq/twenty, 43.8k stars, v1.21.0 Apr 2026) | **AGPL-3.0** + Enterprise commercial | Modern TS/React CRM, kanban, clean UX | AGPL-3.0 is a landmine for commercial SaaS: network-use triggers copyleft | — | **IGNORE** (AGPL) |
| EspoCRM (EspoCRM/espocrm, 2.9k stars, v9.3.4 Mar 2026) | **AGPLv3** | Mature PHP CRM | Same AGPL problem | — | IGNORE (AGPL) |
| SuiteCRM (salesagility/SuiteCRM, 5.4k stars, last commit Jan 2025) | **AGPLv3** | Enterprise CRM | AGPL + stale (>12 months no major commits on v7) | — | IGNORE (AGPL + stale) |
| Plane (makeplane/plane, 47.6k stars, very active) | **AGPL-3.0** | Beautiful issue tracker / kanban | AGPL + it's a PM tool, not a CRM — no lead/contact model | — | IGNORE (AGPL + wrong shape) |
| Focalboard | MIT | Kanban boards | Mattermost abandoned it — stale. No CRM model | — | IGNORE (stale) |
| Kanboard | MIT / AGPL | Minimalist kanban | PHP, no CRM, no contact model | — | IGNORE |
| Crust CRM | Apache 2.0 | Low-code CRM | Low activity, complex Corteza platform dependency | — | IGNORE |

**AGPL flag:** Twenty, EspoCRM, SuiteCRM, Plane are all AGPL-3.0. For a commercial SaaS that modifies the CRM (which OnePoint will), AGPL forces you to release your modifications to every user who touches the network-exposed service. Krayin's MIT license is the only reason it wins this category despite a less modern stack.

**Maps to:** FR-37 through FR-48, G7, SM-6, SM-7, SM-8, SM-9.

---

### C. AI / Agents / Memory

| Project | License | What it solves | What it doesn't | Integration path | Verdict |
|---|---|---|---|---|---|
| **LangGraph** (langchain-ai/langgraph, 29k stars, v1.1.7a1 Apr 2026) | MIT | Durable stateful agents, human-in-loop, persistence | Some learning curve | Research-agent (FR-10..FR-15) as a LangGraph graph triggered by Medplum Bots on new Observation | **USE** |
| **mem0** (mem0ai/mem0, 52.7k stars, active) | Apache 2.0 | Multi-level agent memory (user/session/agent) | — | Persist per-care-recipient memory; recall prior logs for research agent | **USE** |
| **pgvector** (pgvector/pgvector, 20.7k stars, v0.8.2, active) | PostgreSQL License (permissive) | Vector search inside Postgres | Less specialized than Qdrant for billions of vectors | One database for everything; we are not at Qdrant scale for years | **USE** |
| LlamaIndex | MIT | RAG-focused toolkit | Overlaps LangGraph; we don't need two orchestrators | Could use as retrieval helper, but LangGraph is enough | IGNORE (duplication) |
| AutoGen | MIT | Multi-agent conversations | Research-framework feel, less production-hardened than LangGraph | — | IGNORE |
| CrewAI | MIT | Role-based agent orchestration | Lighter than LangGraph; less durable execution | — | IGNORE |
| DSPy | MIT | Prompt optimization | Complementary, not a substitute | Can layer later if prompts drift | IGNORE v0 |
| Qdrant | Apache 2.0 | High-scale vector DB | Operational burden of a second DB | Reconsider at 10M+ vectors | IGNORE v0 |
| Weaviate | BSD-3 | Vector DB + hybrid | Same overkill | — | IGNORE v0 |
| Chroma | Apache 2.0 | Dev-friendly vector DB | Not production-proven at OnePoint's compliance bar | — | IGNORE |
| Letta / MemGPT | Apache 2.0 | Stateful agents with tiered memory | Heavier than mem0; overlaps LangGraph+mem0 | — | IGNORE (duplication) |
| Zep | Apache 2.0 | Agent memory + chat history | Separate service; mem0 covers it | — | IGNORE |

**Maps to:** FR-10 through FR-15, FR-19, NFR-3.

---

### D. Voice / Transcription

| Project | License | What it solves | What it doesn't | Integration path | Verdict |
|---|---|---|---|---|---|
| **LiveKit Agents** (livekit/agents, ~10k stars, active) | Apache 2.0 | Realtime voice agent framework: STT+LLM+TTS+WebRTC+telephony+vision+MCP | Needs LiveKit server infra (also OSS) | Browser-resident agent (FR-1), vision (FR-2), ambient capture (FR-5), phone-in intake for prospects (FR-39) | **USE (core)** |
| **whisper.cpp** (ggerganov/whisper.cpp, 48.5k stars, v1.8.1 active) | MIT | On-device Whisper inference, Apple Silicon Metal, WASM | Not realtime-streaming friendly on its own | Offline fallback (NFR-2); WASM build for in-browser transcription when network is out | **USE (fallback)** |
| faster-whisper (SYSTRAN/faster-whisper, 22.1k stars, active) | MIT | 4x faster Python Whisper via CTranslate2 | Python-only; server-side | Batch transcription for backfill (FR-20) or server fallback | **USE (backend batch)** |
| Vosk | Apache 2.0 | Lightweight offline ASR | Accuracy behind Whisper | — | IGNORE |
| Moonshine | MIT | Small on-device ASR | Newer, less proven; whisper.cpp already covers device-side | — | IGNORE |
| Parakeet (NVIDIA NeMo) | Apache 2.0 | Very accurate but GPU-hungry | Infra overhead for marginal gain over Whisper large-v3 | — | IGNORE |
| Whisper-streaming | MIT | Streaming on top of Whisper | LiveKit Agents already handles streaming STT | — | IGNORE (duplication) |

**Maps to:** FR-1, FR-2, FR-3, FR-4, FR-5, FR-39, NFR-2, NFR-3.

---

### E. Family UX / Auth / Low-Tech

| Project | License | What it solves | What it doesn't | Integration path | Verdict |
|---|---|---|---|---|---|
| **Better-Auth** (better-auth/better-auth, 27.8k stars, very active) | MIT | Magic link, 2FA, multi-tenant, framework-agnostic TS | Newer than Auth.js, but more features and actively growing | Single magic-link flow for FR-8 shared-login + NFR-7 | **USE** |
| **HTMX** (bigskysoftware/htmx, 47.8k stars, active) | BSD-2 | Server-rendered interactivity, 14KB, works on any browser | No SPA routing (good — that's the point) | Entire low-tech sister surface: FR-7, NFR-1 | **USE** |
| Hotwire (Turbo+Stimulus) | MIT | Similar to HTMX, Rails-centric | We're TS/Node, not Rails | — | IGNORE |
| Auth.js (NextAuth) | ISC | Auth for Next.js apps | We don't want a SPA framework gating the low-tech surface | — | IGNORE |
| Lucia | MIT + 0BSD | Auth learning resource | **Deprecated March 2025**; now a tutorial, not a library | — | IGNORE (deprecated) |
| Authelia | Apache 2.0 | SSO portal for reverse proxies | Wrong shape: org-level SSO, not app-level user auth | — | IGNORE (wrong shape) |
| Clerk OSS alternatives | — | — | Clerk itself is not OSS; Better-Auth is the OSS alt | — | — |

**SMS fallback:** Twilio is the only production path (addresses OQ-5). No OSS Twilio replacement is mature enough. Use Twilio SDK directly, wrap in an interface so a future OSS swap is one adapter. SignalWire is a Twilio-compatible alternative but not OSS.

**Maps to:** FR-7, FR-8, FR-33, NFR-1, NFR-7, OQ-5.

---

### F. Medical Research Retrieval

| API | License / Terms | What it solves | What it doesn't | Verdict |
|---|---|---|---|---|
| **Europe PMC REST** (europepmc.org/RestfulWebService) | Free public API, commercial use allowed, no key required for most endpoints | 33M publications, 10.2M full-text, 6.5M open-access, citations, text-mined entities | Rate limits exist but are unpublished — polite usage is fine | **USE (primary)** |
| **OpenAlex API** (api.openalex.org) | CC0 public domain data, free API, 100k calls/day with polite pool | 240M+ works, rich citation graph, author disambiguation, topic classification | Not full-text | **USE (enrichment)** |
| PubMed E-utilities (NCBI) | Free, rate limit 3 req/s without key / 10 with key | Gold-standard PubMed index | **3 req/s is too slow for per-log-entry triggering at any scale** — use only as secondary lookup | EXTEND (secondary) |
| Semantic Scholar API | Free, 100 req/5min unauth / 1 req/s auth, commercial use permitted | Good citation graph, TLDR summaries | Rate limits tight for per-log-entry triggering | IGNORE v0 (Europe PMC covers it) |

**Strategy:** Europe PMC is primary. OpenAlex enriches with citation counts and topic tags. PubMed E-utilities is a fallback for when Europe PMC misses. Cache aggressively per (symptom-set, patient-context) hash.

**Maps to:** FR-11, FR-12, FR-13.

---

### G. Document / Export / Legal Audit Trail

| Project | License | What it solves | What it doesn't | Verdict |
|---|---|---|---|---|
| **Gotenberg** (gotenberg/gotenberg, 11.8k stars, v8.30.1 Apr 2026) | MIT | Dockerized PDF API: HTML→PDF, merge, flatten, PDF/A, watermark, encrypt | Service, not a library — fine for us | **USE** |
| Pandoc | GPL-2+ | Universal document converter | GPL-2 is fine when used as a CLI tool we call; but Gotenberg is better-shaped for HTML→PDF at the legal-export path | USE (backup) |
| WeasyPrint | BSD-3 | Python HTML→PDF | Still active at the main org (the Docker-wrapper repo we checked was archived but WeasyPrint itself is fine) | IGNORE (Gotenberg is one-stop) |
| Typst | Apache 2.0 | Modern LaTeX alternative | Wrong shape: we're not typesetting, we're exporting web views | IGNORE |
| Carbone | LGPL / Commercial | Template-to-PDF | Commercial-dependency model | IGNORE |
| **FHIR AuditEvent** (inside Medplum) | Apache 2.0 | Immutable event log inside FHIR store | Already there — use it | **USE** |
| **SHA-256 hash chain** (custom, ~50 lines) | — | Tamper-evident append-only log on top of AuditEvent | — | **BUILD (tiny)** |
| sigstore / Rekor | Apache 2.0 | Transparency log for signed artifacts | Overkill for per-log-entry signing at v0 volume; revisit at scale | IGNORE v0 |
| Trillian | Apache 2.0 | Google's transparency log | Operational burden | IGNORE v0 |

**Legal defensibility (FR-30, FR-31, FR-32) plan:**
1. Every log entry lands in Medplum as a FHIR resource with Provenance + AuditEvent (immutable, attributed, timestamped).
2. A thin SHA-256 hash chain runs over `(prev_hash, resource_id, timestamp, author_id)` to produce a tamper-evident ledger (~50 lines of code).
3. Export via Gotenberg renders a signed PDF of the chronological log with hash-chain verification page appended.

**Maps to:** FR-30, FR-31, FR-32, G5.

---

## What NOT to Build

1. **Do not build your own CRM.** Use Krayin, extend the pipeline model. (FR-37..FR-48)
2. **Do not build your own EMR / FHIR server.** Use Medplum. This is the single biggest "don't" in the document. (FR-27..FR-29)
3. **Do not build your own auth.** Use Better-Auth with magic-link. Do not roll JWT flows. (FR-8, NFR-7)
4. **Do not build your own voice agent framework.** Use LiveKit Agents. Do not glue Whisper + GPT + TTS yourself. (FR-1..FR-5)
5. **Do not build your own vector DB or agent memory layer.** pgvector + mem0. (FR-19)
6. **Do not build your own PDF export pipeline.** Gotenberg in a container. (FR-31)
7. **Do not build a React SPA for the low-tech sister surface.** Server-rendered HTMX. (FR-7)
8. **Do not build your own PubMed crawler.** Europe PMC + OpenAlex cover 33M+ papers. (FR-11)
9. **Do not build your own audit-log database.** FHIR AuditEvent inside Medplum is already immutable. Add a hash chain, stop. (FR-30)
10. **Do not build an SMS gateway.** Twilio, behind an adapter interface. (OQ-5)
11. **Do not build your own kanban board library.** Krayin has one. The Longmont pipeline is a Krayin pipeline. (FR-41)
12. **Do not build a generic family chat / video.** Use LiveKit for video (same infra as the voice agent). (FR-33)

---

## Build-vs-Buy Decisions — Every FR Area

| FR Area | Decision | OSS Leveraged |
|---|---|---|
| FR-1..FR-5 Voice capture | **REUSE** LiveKit Agents + whisper.cpp fallback | LiveKit Agents, whisper.cpp |
| FR-6 Native app | **BUILD (thin)** — React Native shell calling the same TS backend | (React Native, OSS) |
| FR-7 Low-tech web surface | **BUILD (thin)** — server-rendered HTMX pages, no SPA | HTMX |
| FR-8 Shared login | **REUSE** Better-Auth magic-link | Better-Auth |
| FR-9 Dashboard | **BUILD** on Medplum React components | Medplum React |
| FR-10..FR-15 Research agent | **REUSE + CONFIGURE** LangGraph graph + mem0 + Europe PMC/OpenAlex tools | LangGraph, mem0, Europe PMC, OpenAlex |
| FR-16..FR-19 Wearables | **CUSTOM (required)** — per-device adapters; Oura has an API, no OSS shortcut exists that covers all devices. Accept this is custom | — |
| FR-20..FR-23 iMessage backfill | **CUSTOM (small)** — SQLite reader against `chat.db`. No mature OSS package that handles consent UX; ~200 lines of Python + UI | (sqlite3) |
| FR-24..FR-26 Visualization / timeline | **EXTEND** Medplum React components; add mem0-powered semantic search | Medplum React, pgvector |
| FR-27..FR-29 Medical records + HIPAA | **REUSE** Medplum (the central decision) | Medplum |
| FR-30..FR-32 Legal defensibility | **REUSE + 50 LINES** Medplum AuditEvent + SHA-256 chain + Gotenberg export | Medplum, Gotenberg |
| FR-33 Family video | **REUSE** LiveKit (same infra as voice agent — free win) | LiveKit |
| FR-34..FR-36 Spreadsheet on-ramp | **CUSTOM (small)** — Google Sheets API sync bridge; ~1 day of work | (Google Sheets API) |
| FR-37..FR-48 Tenant placement pipeline | **EXTEND** Krayin CRM — custom pipeline stages, fit-assessment agent, Medplum move-in handoff | Krayin |

**Total custom-build surface:** wearable adapters, iMessage reader, sheet sync, thin native/web shells, glue code. Everything else is configuration and extension on top of the stack above.

---

## Licensing Watchlist (commercial SaaS safety)

| License | OnePoint stance |
|---|---|
| Apache 2.0, MIT, BSD, ISC, MPL-2.0 | **Safe** — all core picks fall here |
| AGPL-3.0 | **Blocked** — network-use copyleft. Twenty, EspoCRM, SuiteCRM, Plane all fall here |
| GPL-3.0 | **Use as separate process only** — OpenEMR, Pandoc (we call it as CLI) |
| SSPL | **Blocked** — not currently in our stack, but watch for Mongo etc. |
| LGPL | **Safe if linked dynamically** — not currently needed |

---

## Freshness Audit (flagging stale candidates, >12mo since last commit)

- **SuiteCRM:** last meaningful commit Jan 2025. **STALE** (>12mo). Already rejected on AGPL anyway.
- **Focalboard:** Mattermost dropped it. **STALE/ABANDONED**. Rejected.
- **Lucia:** **DEPRECATED** March 2025 by maintainer. Rejected.
- **WeasyPrint Docker wrapper (Kozea/weasyprint):** archived 2023. Upstream WeasyPrint itself is fine, but we're using Gotenberg anyway.
- Everything else in the stack had activity in the last 30 days as of 2026-04-11.

---

## Final Note — The Shape of the v0 Build

A single Docker Compose file boots:
- `postgres` (Medplum + Krayin + pgvector)
- `medplum-server` (FHIR + auth + bots)
- `krayin-app` (tenant pipeline, bridged to Medplum via webhook on stage=Resident)
- `livekit-server` + `livekit-agents` (voice + vision + video)
- `langgraph-runner` (research agents, triggered by Medplum Bot on new Observation)
- `gotenberg` (PDF export)
- `web` (HTMX + server-rendered TS; the low-tech surface)
- `api` (thin TS/Node.js gateway with Better-Auth)

That is the entire platform. Every box is OSS. Every license is commercial-SaaS-safe. Zero from-scratch systems of record. This is what respects Ali Ann's and Jero's bandwidth constraint.

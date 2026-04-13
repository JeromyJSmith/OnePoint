---
title: "OnePoint MVP Execution Plan"
project: "OnePoint"
owner: "Jero + Ali Ann"
status: "active"
version: "v0"
last_updated: "2026-04-13"
source_docs:
  - "OnePoint_PRD_MVP.md"
  - "OnePoint_MVP_2Week_Checklist.md"
objective: "Ship a usable MVP for voice-first caregiver logging with shared timeline, on-duty handoff, and legal-grade export."
success_criteria:
  - "Voice log capture under 30 seconds"
  - "Shared timeline adopted by team"
  - "Export works for 30-day legal/history review"
---

# OnePoint Plan

## What We Are Doing
We are building the narrow MVP first: a simple, reliable care-log system that replaces scattered text threads with one shared source of truth.  
This plan intentionally excludes advanced features (HIPAA integrations, wearables, automated medical research, CRM) until core usage is stable.

## Plan
1. Build the core data model and web-first foundation.
2. Deliver voice capture into timeline entries.
3. Add on-duty and handoff workflow.
4. Add export for legal/risk documentation.
5. Backfill historical spreadsheet data.
6. Validate with real usage and ship.

## Task List (YAML)

```yaml
tasks:
  - id: T01
    name: "Initialize MVP foundation"
    status: "pending"
    priority: "P0"
    outcome: "Working project scaffold with persistent storage and migrations."
    deliverables:
      - "Project scaffold committed locally"
      - "Database schema initialized"
      - "Basic seed data loaded"

  - id: T02
    name: "Implement core data model"
    status: "pending"
    priority: "P0"
    depends_on: ["T01"]
    entities:
      - "CareRecipient"
      - "TeamMember"
      - "LogEntry"
      - "ShiftStatus"
    outcome: "Data model supports multi-recipient logging and handoff."

  - id: T03
    name: "Build voice capture pipeline"
    status: "pending"
    priority: "P0"
    depends_on: ["T02"]
    outcome: "Tap -> record -> transcribe -> save as log entry."
    acceptance:
      - "Entry stores author + timestamp + recipient + source"
      - "Flow completes in under 30 seconds target"

  - id: T04
    name: "Build shared timeline UI"
    status: "pending"
    priority: "P0"
    depends_on: ["T03"]
    outcome: "Chronological timeline visible to all users."
    features:
      - "Recipient filter"
      - "Date filter"
      - "Mobile-first layout"

  - id: T05
    name: "Implement on-duty and handoff"
    status: "pending"
    priority: "P0"
    depends_on: ["T04"]
    outcome: "Current on-duty person and latest handoff are always visible."

  - id: T06
    name: "Implement simple link-based access"
    status: "pending"
    priority: "P0"
    depends_on: ["T04"]
    outcome: "Low-tech users can access without app install."
    note: "Keep auth friction minimal for MVP while preserving basic access control."

  - id: T07
    name: "Implement export"
    status: "pending"
    priority: "P0"
    depends_on: ["T05"]
    outcome: "Chronological date-range export for legal/history review."
    format: "CSV or Markdown (v0)"

  - id: T08
    name: "Build spreadsheet backfill import"
    status: "pending"
    priority: "P0"
    depends_on: ["T02"]
    outcome: "One-time import of existing tracking data into timeline."

  - id: T09
    name: "Reliability and error handling pass"
    status: "pending"
    priority: "P1"
    depends_on: ["T03", "T04", "T05", "T07"]
    outcome: "Core flows handle failures gracefully without data loss."

  - id: T10
    name: "MVP validation and release readiness"
    status: "pending"
    priority: "P0"
    depends_on: ["T06", "T07", "T08", "T09"]
    outcome: "All MVP acceptance criteria validated with real usage."
    release_gate:
      - "Voice logging works end-to-end"
      - "Timeline stable on mobile and desktop"
      - "Export passes 30-day test"
      - "Low-tech user can access unassisted"
```

## Out of Scope For This Plan
- HIPAA medical record integrations
- AI medical journal research agent
- Wearables and biometrics
- Built-in video chat
- Assisted living placement CRM

## Planning Checklist
- [ ] Scope is constrained to MVP only (no hidden P1/P2 features).
- [ ] Every P0 task has a clear outcome and dependency path.
- [ ] Acceptance criteria are defined for core flows.
- [ ] Low-tech access is treated as a release requirement.
- [ ] Export and data integrity requirements are included.
- [ ] Backfill path exists for legacy spreadsheet data.
- [ ] Release gate is explicit and testable.

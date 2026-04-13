# OnePoint MVP — 2 Week Checklist

Use this as the execution board for v0.

## Week 1 — Build Core Flow

### Day 1: Project Setup + Data Skeleton
- [ ] Confirm stack and create project scaffold.
- [ ] Create core entities: `CareRecipient`, `TeamMember`, `LogEntry`, `ShiftStatus`.
- [ ] Add persistence layer and migrations.
- [ ] Seed with one sample recipient and two sample members.

### Day 2: Voice Capture Pipeline
- [ ] Add record button UI (mobile-first).
- [ ] Implement audio upload/save flow.
- [ ] Implement speech-to-text integration.
- [ ] Save transcript as `LogEntry` with timestamp and author.
- [ ] Validate end-to-end voice -> timeline entry.

### Day 3: Timeline UI
- [ ] Build timeline feed view.
- [ ] Show author, time, recipient, and entry text.
- [ ] Add recipient and date filters.
- [ ] Add empty/loading/error states.

### Day 4: On-Duty + Handoff
- [ ] Add "set on-duty" action.
- [ ] Add handoff note field.
- [ ] Show current on-duty and latest handoff at top of timeline.
- [ ] Ensure updates propagate to all users.

### Day 5: Basic Access + Sharing
- [ ] Implement simple link-based access model for MVP.
- [ ] Ensure low-friction entry (no app install required).
- [ ] Validate flow on older phone/browser.
- [ ] Smoke test with at least two user personas.

## Week 2 — Hardening + Export + Import

### Day 6: Export
- [ ] Build export endpoint by date range.
- [ ] Include ordered timeline with author + timestamps.
- [ ] Support one practical format (CSV or Markdown first).
- [ ] Verify export readability for legal/history usage.

### Day 7: Spreadsheet Backfill
- [ ] Define import mapping from current spreadsheet columns.
- [ ] Build one-time import tool.
- [ ] Preserve original timestamps where available.
- [ ] Validate imported records render correctly in timeline.

### Day 8: Reliability + UX polish
- [ ] Improve form validation and error handling.
- [ ] Add retry behavior for voice transcription failures.
- [ ] Add confirmations for destructive actions.
- [ ] Tighten mobile layout and readability.

### Day 9: QA + Edge Cases
- [ ] Test low-connectivity behavior.
- [ ] Test long voice notes and malformed transcripts.
- [ ] Test multi-recipient switching.
- [ ] Test concurrent updates (two users logging around same time).

### Day 10: MVP Readiness Review
- [ ] Run final acceptance checklist from `OnePoint_PRD_MVP.md`.
- [ ] Fix P0 defects only (defer non-critical enhancements).
- [ ] Prepare short user walkthrough.
- [ ] Capture v0.1 backlog (P1 items only).

## Daily Definition of Done
- [ ] Feature works on mobile browser and desktop browser.
- [ ] Data is timestamped and attributed.
- [ ] No regressions in core flow (voice log, timeline, on-duty, export).
- [ ] Notes updated in project doc before end of day.

## Launch Gate (Must Pass)
- [ ] Voice log can be created in under 30 seconds.
- [ ] Timeline is accurate and shared.
- [ ] Export works for last 30 days.
- [ ] At least one low-tech user can access via link unassisted.

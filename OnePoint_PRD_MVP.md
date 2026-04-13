# OnePoint — MVP PRD

**Status:** Active Build Scope (v0)  
**Last Updated:** 2026-04-13  
**Audience:** Product + Build

## 1) Product Definition
OnePoint is a voice-first, shared care-log app for family and non-medical caregiver teams.  
It replaces scattered group texts with one reliable timeline that works for both tech-savvy and low-tech users.

## 2) Problem
Care teams are coordinating with texts, memory, and ad hoc notes. This causes:
- missed handoffs,
- unclear accountability,
- inconsistent history,
- legal risk when records are needed.

## 3) MVP Outcome
Any caregiver can capture an update in under 30 seconds, and the whole team can view a clean, timestamped timeline immediately.

## 4) Target Users
- **Primary:** lead caregiver/coordinator.
- **Secondary:** family or companion caregivers rotating shifts.
- **Critical edge user:** low-tech relative who only wants a simple web link.

## 5) In Scope (P0)
1. **Voice capture -> log entry**
   - Tap record, speak naturally, save.
   - Auto-transcribed text entry with author + timestamp.
2. **Shared timeline**
   - Reverse-chronological care notes.
   - Filter by care recipient and date.
3. **On-duty + handoff**
   - Set who is currently on duty.
   - Store latest handoff summary.
4. **Web-first access**
   - Mobile web app works on older/low-spec devices.
   - Link-based access so no app install is required for v0.
5. **Export for legal/risk needs**
   - Export date range as chronological record.
   - Each item includes who logged it and when.
6. **Spreadsheet backfill**
   - One-time import from existing spreadsheet to seed history.

## 6) Out of Scope (P1/P2+)
- HIPAA medical records integrations.
- Automated medical journal research agent.
- Wearables integrations.
- Built-in video chat.
- Assisted-living placement CRM.
- Complex role matrix and enterprise auth.

## 7) Functional Requirements
- **FR-1:** User can create a voice note and see saved text log in same session.
- **FR-2:** Every log entry stores `recipient`, `author`, `timestamp`, `content`, `source`.
- **FR-3:** Timeline updates are visible to all authorized users quickly.
- **FR-4:** Team can set and view current on-duty person.
- **FR-5:** Export includes full ordered log over selected range.
- **FR-6:** System supports at least two care recipients.

## 8) Non-Functional Requirements
- **NFR-1:** Fast capture flow (target under 30 seconds).
- **NFR-2:** No data loss.
- **NFR-3:** Mobile web usable on older devices.
- **NFR-4:** Basic privacy protections and secure storage.

## 9) Minimal Data Model
- **CareRecipient**: id, name, status
- **TeamMember**: id, display_name, contact
- **LogEntry**: id, recipient_id, member_id, timestamp, text, source
- **ShiftStatus**: recipient_id, on_duty_member_id, handoff_note, updated_at

## 10) Success Metrics (first 30 days)
- 80%+ daily updates captured in OnePoint instead of group text.
- Average log entry time under 30 seconds.
- At least 3 weekly active users.
- 30-day export generated in under 1 minute without manual edits.

## 11) Acceptance Criteria (MVP complete when...)
- Voice log capture works end-to-end.
- Shared timeline is stable and readable on phone + desktop browsers.
- On-duty state and handoff note are visible to all users.
- Export is usable for legal/history review.
- Existing spreadsheet data can be imported once.

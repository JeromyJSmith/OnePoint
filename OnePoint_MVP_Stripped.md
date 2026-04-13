# OnePoint MVP (Stripped)

## What This App Is
OnePoint is a simple, shared caregiver log for families and non-medical caregivers.
It replaces scattered group texts with one timeline everyone can use, including low-tech family members.

## Core Problem To Solve
- Care updates are currently spread across texts, memory, and ad hoc notes.
- Shift handoffs are inconsistent.
- Legal/risk exposure is high without clean timestamps and attribution.
- Some family members will not install or learn complex apps.

## Primary Users
- Lead caregiver / coordinator (power user, logs often, needs exports).
- Family members on shift (need fast logging and handoff clarity).
- Low-tech family members (must work via simple web link).

## MVP Goal (v0)
In under 30 seconds, any caregiver can log what happened, and everyone sees the same updated timeline.

## Must-Have Features (P0)
1. Voice-first shift logging:
   - Tap record, speak naturally, save.
   - Auto-transcribe into a single timeline entry with timestamp and author.
2. Shared timeline:
   - Chronological feed of all care notes.
   - Basic filters: by person receiving care, by date.
3. On-duty handoff:
   - Mark who is currently on duty.
   - Show latest handoff note at top.
4. Cross-device access:
   - Mobile-friendly web app first.
   - Link-based access for low-tech relatives (no app install required).
5. Legal-grade export:
   - Export date range as chronological log (PDF/CSV/Markdown acceptable for v0).
   - Every entry includes created-at time and who logged it.
6. Spreadsheet bridge (temporary):
   - Import existing spreadsheet data once for backfill.
   - Do not block launch on perfect sync.

## Should-Have Soon After MVP (P1)
- Pull old iMessage/text history into timeline (with consent).
- Basic dashboard metrics (note volume, symptom trend tags, coverage gaps).
- Simple reminders/checklists for end-of-shift notes.

## Explicitly Not MVP (Later)
- Full HIPAA medical record integration.
- Automated medical journal research agent.
- Wearables integrations.
- Built-in video chat.
- Assisted-living placement CRM pipeline.
- Any broad "all-in-one healthcare platform" scope.

## MVP Data Model (Minimal)
- CareRecipient: name, notes.
- TeamMember: name, contact, role.
- LogEntry: recipient_id, member_id, timestamp, text, source(voice/manual/import).
- ShiftStatus: recipient_id, on_duty_member_id, updated_at, handoff_note.

## Non-Negotiable Product Rules
- Fast capture beats perfect structure.
- Low-tech compatibility is a release blocker.
- No data loss. Ever.
- Every action is timestamped and attributable.

## Success Criteria (First 30 Days)
- 80%+ of daily updates logged in OnePoint instead of group text.
- At least 3 active family/caregiver users each week.
- One-click export works for last 30 days without manual cleanup.
- Average log creation time under 30 seconds.

## Build Order (Practical)
1. Web app shell + auth-light shared access.
2. Voice capture -> transcript -> log entry.
3. Timeline + on-duty status.
4. Export.
5. Spreadsheet import.

If these five steps work, MVP is real. Everything else is phase 2.

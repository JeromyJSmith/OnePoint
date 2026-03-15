# OnePoint! Caregiving Colorado — Development Plan

## Phase 1: Core Platform + AI Foundation (Weeks 1-5)

### Week 1: Patient Dashboard + Navigation

**Goal**: Caregivers and family admins can see and navigate to their patients.

- Patient list page (`apps/web/src/app/dashboard/patients/page.tsx`)
  - Role-aware: FAMILY_ADMIN sees owned patients, CAREGIVER sees assigned patients
  - Card layout with patient name, conditions, last vitals summary
- Patient detail page (`apps/web/src/app/dashboard/patients/[id]/page.tsx`)
  - Tabbed layout: Overview / Vitals / Meds / Notes
  - Overview tab: profile card (conditions, contacts, weight, gait belt status)
- Sidebar navigation component
  - Role-based menu items (admins see admin panel, caregivers see "Today" view)
  - Collapsible on mobile
- Wire up to existing API endpoints: `patients.list`, `patients.get`
- Use oRPC client from `apps/web/src/utils/orpc.ts` with TanStack Query

### Week 2: Vitals + Medications UI

**Goal**: Caregivers can log vitals and medication intake, family admins can review.

- BP readings list with color-coded status
  - HIGH (red), LOW (yellow), NORMAL (green) — utils already in `packages/utils/src/bp.ts`
- Quick-log vital form (modal or slide-over)
  - Type selector (blood_pressure, heart_rate, temperature, weight, blood_sugar)
  - Dynamic value fields based on type
- Vitals trend chart (recharts or similar)
  - Systolic/diastolic over time with threshold lines
- Medication list with schedule display
  - Active/inactive toggle, grouped by time of day
- Medication intake logging form
  - Status: given / refused / skipped / late
  - Notes field, auto-timestamps
- Missed dose alerts (highlight overdue medications)
- Wire up: `vitals.list`, `vitals.create`, `medications.list`, `medications.logIntake`, `medications.logs`

### Week 3: Notes + AI Handoff Briefing

**Goal**: Shift notes flow naturally, AI generates handoff summaries.

- Observation/incident log page
  - Type filtering: incident / shift_note / checklist
  - Incident subtypes: fall, behavioral, medical_emergency, medication_error, skin_integrity, elopement, dietary, other
- Quick-add shift note form
  - Rich text or simple textarea with auto-save
- Incident report form (structured, all 8 subtypes)
- Install Vercel AI SDK: `bun add ai @ai-sdk/anthropic`
- AI route: `/api/ai/handoff/route.ts`
  - Generates structured briefing from last 8 hours of data
  - Pulls vitals, med logs, observations for the patient
  - Returns sections: critical alerts, medication status, vital trends, behavioral notes, pending tasks
- AI route: `/api/ai/summarize/route.ts`
  - Auto-summarize notes on creation
  - TL;DR appended to long observations
- Handoff view page: formatted briefing with severity color indicators
- Wire up: `observations.list`, `observations.create` + new AI routes

### Week 4: Voice-to-Everything

**Goal**: Caregivers speak naturally, AI creates structured records.

- Install OpenAI for Whisper: `bun add @ai-sdk/openai`
- Web Audio API recording component
  - Tap to record, tap to stop
  - Visual waveform indicator during recording
  - Auto-upload on stop
- AI route: `/api/ai/voice/route.ts`
  - Pipeline: audio -> Whisper transcription -> Claude extraction -> structured records
  - Tool calling: AI can invoke `logVital()`, `logMedication()`, `createObservation()`, `createTask()`
- Voice memo creates multiple records simultaneously
  - Example: "Connie refused her 4pm Carbidopa, BP was 158/94, she seemed agitated"
  - Result: medication_log (refused) + vital_reading (BP 158/94, HIGH) + observation (behavioral note)
- Confirmation UI: show extracted records before saving, allow edits
- Shared tool definitions: `apps/web/src/app/api/ai/tools.ts`

### Week 5: Caregiver Portal + Admin + Polish

**Goal**: Role-specific experiences, admin oversight, production polish.

- Caregiver "Today" view
  - Assigned patients with what's due now
  - Recent alerts and unread handoff briefings
  - Quick-action buttons (log vital, log med, add note, voice memo)
- Caregiver profile setup
  - displayName, initials, color picker (schema exists in `caregiver_profile`)
- Admin panel (CARE_OS_ADMIN only)
  - User list with role badges
  - Role management (change user roles)
  - Audit log viewer with filtering
- Care assignment management
  - Assign/unassign caregivers to patients
  - Active/inactive toggle
- Polish pass
  - Loading skeletons for all data-fetching pages
  - Error boundaries with retry buttons
  - Empty states with helpful prompts
  - Mobile responsiveness audit
  - Toast notifications for actions (save, delete, log)

---

## Phase 2: Enhanced Coordination (Weeks 6-9)

### Week 6: Medication Management Deep Dive
- Visual pill identification (photo upload + description)
- Medication interaction checker (AI-powered, flag conflicts)
- Adherence tracking dashboard (percentage over time, streaks)
- AI: medication adherence pattern detection ("Connie consistently refuses evening Carbidopa")

### Week 7: Appointments + Documents
- Appointment tracking with reminders
- Document storage and sharing (encrypted vault)
- Photo/scan upload for insurance cards, prescriptions, advance directives
- Calendar sync (Google/Apple/Outlook via CalDAV)

### Week 8: Privacy Circles + Notifications
- Privacy Circles: granular permissions with visual indicators
  - Inner circle (family admin) sees everything
  - Outer circles (extended family, friends) see filtered views
- Notification infrastructure
  - Twilio SMS for critical alerts
  - SendGrid email for daily summaries
  - Web Push for real-time updates
- AI: daily check-in generation (auto-compose morning update for family)

### Week 9: Integration + Testing
- API/Webhooks for external integrations
- End-to-end testing with Playwright
- Performance optimization (lazy loading, query caching)
- Security audit (RBAC edge cases, data isolation)

---

## Phase 3: Advanced Features (Weeks 10-13)

### Week 10: Wearable Integration
- Apple Health, Google Fit, Fitbit data ingestion
- Auto-log vitals from wearable readings
- AI: wearable data correlation with observations ("BP spikes correlate with agitation episodes")

### Week 11: Offline-First
- Dexie.js offline storage (already in deps)
- Background sync when connectivity returns
- Conflict resolution for concurrent edits
- Service worker for PWA install

### Week 12: AI Predictive Analytics
- Predictive health trends (BP trajectory, medication effectiveness)
- Caregiver burnout detection (logging frequency, note sentiment analysis)
- Anomaly detection (unusual vital patterns, missed medication spikes)

### Week 13: Voice-First + Streaming
- Real-time transcription streaming (live captions during recording)
- Voice-first notes with auto-categorization
- Conversational AI assistant ("What was Connie's BP trend this week?")

---

## Phase 4: Specialized + Marketplace (Weeks 14-18)

### Week 14-15: Caregiver Marketplace
- Caregiver search with filters (specialization, availability, location, ratings)
- Hire/invite flow with background check integration
- Review and rating system
- Scheduling and availability management

### Week 16: Commerce Hub
- Shopping list generation from voice ("Connie needs more Ensure and adult wipes")
- Amazon/pharmacy/grocery ordering integration
- Prescription refill reminders with pharmacy API

### Week 17: Specialized Modules
- End-of-life planning (advance directives, emergency access protocols)
- Autism/IEP module (behavior logging, therapy tracking, visual schedules)
- Insurance navigation (document scanning, appeal letter drafting with AI)

### Week 18: AI Care Assistant
- Full conversational AI with patient context
- Multi-turn dialogue for complex care questions
- Proactive suggestions based on care patterns
- Research mode: answer care questions with citations

---

## AI Architecture

```
apps/web/src/app/api/ai/
  handoff/route.ts      — Generate shift handoff briefing
  summarize/route.ts    — Auto-summarize care notes
  voice/route.ts        — Transcribe + extract + act on voice input
  research/route.ts     — Answer care questions with patient context
  trends/route.ts       — Analyze vitals/meds/observations over time
  tools.ts              — Shared tool definitions for AI function calling
```

### Tool Functions the AI Can Call

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `logVital` | patientId, type, values, notes | Record a vital reading |
| `logMedication` | medicationId, status, notes | Log medication intake |
| `createObservation` | patientId, type, content | Create a care note |
| `createTask` | title, assignee, dueDate | Create a follow-up task |
| `addToShoppingList` | items[] | Add items to care supplies list |
| `getPatientHistory` | patientId, days | Retrieve recent care records |
| `getMedicationSchedule` | patientId | Get current medication schedule |
| `getRecentVitals` | patientId, type, count | Get recent vital readings |

---

## Success Metrics

| Phase | Metric |
|-------|--------|
| Phase 1 | 3 caregivers can manage Connie's care entirely through the app |
| Phase 2 | Family members get automated updates without asking |
| Phase 3 | App predicts issues before they become emergencies |
| Phase 4 | OnePoint! is the only app families need |

---

## Competitive Advantage

Based on analysis of 19 competitors (see `competitive-feature-tracker.csv`):

- Only 1 competitor (Caring Village) has AI features, and they are buggy/limited
- No competitor has voice-to-task or voice-to-structured-data
- No competitor has AI handoff briefings
- No competitor has caregiver burnout detection
- No competitor has predictive health analytics

**Blue ocean features** (OnePoint! will be the first):
1. Voice-to-everything (speak naturally, create structured records)
2. AI handoff briefing (auto-generated shift summaries)
3. Caregiver burnout detection (sentiment + frequency analysis)
4. Predictive health analytics (trend detection, anomaly alerts)
5. Commerce hub (voice-to-shopping-list-to-order)

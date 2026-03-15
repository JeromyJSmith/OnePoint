# OnePoint! Caregiving Colorado — Project Context

## What This Is

An AI-native caregiving super-app that bridges family caregivers and professional caregivers. Built for AliAnn's care team managing Connie's care (Parkinson's + Dementia + BP issues). The platform coordinates medication tracking, vitals logging, shift handoffs, and AI-powered voice-to-everything — so caregivers spend less time on paperwork and more time on care.

**Landing page**: https://jeromyjsmith.github.io/OnePoint/ (Vite + React + Remotion Player, source in cli-anything repo)

**Status**: Backend foundation complete (auth, DB, API, types, seed data). Frontend has login/signup forms and an empty dashboard shell. Phase 1 build-out starts with patient dashboard and navigation.

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Monorepo | Turborepo + Bun 1.2.19 | `bun run dev` starts all services |
| Frontend | Next.js 16 (App Router), React 19 | Port 3001 |
| Styling | Tailwind CSS 4, shadcn/ui (base-lyra) | Mobile-first, lucide-react icons |
| API | oRPC v1.12.2 | Type-safe RPC, `os.$context<Context>()` + `o.middleware()` |
| Auth | BetterAuth 1.5.2 | Email/password, session cookies, RBAC via user.role |
| Database | Drizzle ORM + Supabase PostgreSQL | Push-based schema management |
| Validation | Zod v4 | Use `zod/v3` for oRPC input schemas (compatibility) |
| State | TanStack Query + oRPC client | `createTanstackQueryUtils` pattern |
| Offline | Dexie.js (IndexedDB) | PWA offline support (planned) |
| AI | Vercel AI SDK (`ai`), Claude, Whisper | Reasoning/extraction + transcription (Phase 1 Week 3-4) |
| Linting | Biome | Tabs, double quotes, noExplicitAny |
| Hooks | Lefthook | pre-commit: biome, pre-push: check-types |
| Deployment | Vercel (planned) | Local dev for now |

## Package Structure

```
apps/
  web/                    # Next.js PWA (port 3001)
  fumadocs/               # Documentation site (port 4000)

packages/
  types/                  # @WeCareALOT/types — Roles, permissions, entity types
  utils/                  # @WeCareALOT/utils — BP classification, dates, IDs, Zod schemas
  env/                    # @WeCareALOT/env — Environment variable validation (server + web)
  db/                     # @WeCareALOT/db — Drizzle schema, migrations, seed
  auth/                   # @WeCareALOT/auth — BetterAuth config, roles re-export, client
  api/                    # @WeCareALOT/api — oRPC procedures, routers, middleware
  ui/                     # @WeCareALOT/ui — Shared components (button, card, input, etc.)
  config/                 # @WeCareALOT/config — Base tsconfig
```

## What's Built

- **Auth system**: BetterAuth with 5 roles (FAMILY_ADMIN, CAREGIVER, PATIENT, EMERGENCY_CONTACT, CARE_OS_ADMIN), 25 permissions
- **Database**: 9 tables (user, patient, medication, medication_log, vital_reading, threshold_rule, observation, care_assignment, caregiver_profile, audit_log)
- **API**: 7 routers with 30+ endpoints, all with role-based access control
- **Types**: Complete TypeScript types for all entities
- **Seed data**: Patient "Connie" with 3 caregivers (AliAnn, Valita, Hannah), 5 meds, 6 BP readings, 5 observations
- **UI**: Login/signup forms working, empty dashboard shell
- **Landing page**: https://jeromyjsmith.github.io/OnePoint/ (built with Remotion)

## What's NOT Built (Phase 1 Target)

- Dashboard pages (patient list, detail, vitals, meds, notes)
- Caregiver portal (today view, quick log forms)
- Voice-to-everything (AI transcription to structured extraction)
- AI handoff briefing (auto-generated shift summary)
- AI note summaries (auto-summarize care notes)
- Notifications (push/email/SMS)
- Admin panel (user management, audit logs)

See `DEVELOPMENT_PLAN.md` for the full phased roadmap.

## Database Schema (9 tables)

| Table | Key Fields | Notes |
|-------|-----------|-------|
| `user` | id, name, email, role, phone | BetterAuth managed + role/phone added |
| `session` / `account` / `verification` | — | BetterAuth internal tables |
| `patient` | familyAdminId, name, medicalConditions (jsonb), emergencyContacts (jsonb), weight, gaitBelt | Owned by FAMILY_ADMIN |
| `medication` | patientId, name, dose, schedule, purpose, active | Cascades from patient |
| `medication_log` | medicationId, patientId, caregiverId, status, loggedAt | given/refused/skipped/late |
| `vital_reading` | patientId, caregiverId, type, values (jsonb), status | BP auto-classified |
| `threshold_rule` | patientId, vitalType, field, minValue, maxValue, action | Per-patient alert config |
| `observation` | patientId, caregiverId, type, subtype, content | Incidents, shift notes, checklists |
| `care_assignment` | patientId, caregiverId, role, startDate, active | Links caregivers to patients |
| `caregiver_profile` | userId (unique), displayName, initials, color | Visual identity |
| `audit_log` | userId, action, resource, resourceId, details (jsonb) | Who did what when |

## API Router Map

```
appRouter
  healthCheck              # GET /api/rpc — returns "OK"
  patient.*                # list, get, create, update, delete
  medication.*             # list, get, create, update, delete, logIntake, logs
  vitals.*                 # list, get, create, delete
  vitals.thresholds.*      # list, create, delete
  observation.*            # list, get, create, update, delete
  caregiver.profile.*      # get, upsert
  caregiver.assignments.*  # list, create, update, delete
  admin.users.*            # list, updateRole (CARE_OS_ADMIN only)
  admin.audit.*            # list (CARE_OS_ADMIN only)
```

## RBAC Roles

| Role | Description |
|------|-------------|
| FAMILY_ADMIN | Owns patients, full CRUD, manages caregivers |
| CAREGIVER | Log vitals/meds/observations for assigned patients |
| PATIENT | Read-only access to own records |
| EMERGENCY_CONTACT | Receives notifications only |
| CARE_OS_ADMIN | System admin, audit access |

## Build & Development

```bash
cd ~/Desktop/WeCareALOT
bun install             # Install all dependencies
bun run dev             # Start all dev servers
bun run dev:web         # Start web app only (port 3001)
bun run build           # Production build
bun run check-types     # TypeScript compilation check
bun run check           # Biome lint + format
bun run db:push         # Push schema to Supabase
bun run db:generate     # Generate migration files
bun run db:migrate      # Run migrations
bun run db:studio       # Open Drizzle Studio
bun run db:seed         # Seed demo data (Connie + 3 caregivers)
```

## Environment Variables Required

```
DATABASE_URL=            # Supabase PostgreSQL connection string
BETTER_AUTH_SECRET=      # Min 32 chars, session signing
BETTER_AUTH_URL=         # e.g. http://localhost:3001
CORS_ORIGIN=             # e.g. http://localhost:3001
ANTHROPIC_API_KEY=       # For AI features (Claude)
OPENAI_API_KEY=          # For Whisper transcription
```

## Key Files

### Auth & Config
- `packages/auth/src/index.ts` — BetterAuth config, role definitions, plugin setup
- `packages/auth/src/client.ts` — Client-side auth helpers
- `packages/auth/src/roles.ts` — Role and permission constants
- `packages/env/src/server.ts` — Server env validation
- `packages/env/src/web.ts` — Client env validation

### Database
- `packages/db/src/schema/` — All table definitions (patients.ts, medications.ts, vitals.ts, observations.ts, caregivers.ts, audit.ts, auth.ts)
- `packages/db/src/seed.ts` — Demo data seeder (Connie + 3 caregivers)
- `packages/db/src/index.ts` — Drizzle client export

### API
- `packages/api/src/routers/index.ts` — App router composition
- `packages/api/src/routers/patients.ts` — Patient CRUD
- `packages/api/src/routers/medications.ts` — Medication CRUD + intake logging
- `packages/api/src/routers/vitals.ts` — Vital readings + thresholds
- `packages/api/src/routers/observations.ts` — Notes, incidents, checklists
- `packages/api/src/routers/caregivers.ts` — Caregiver profiles + assignments
- `packages/api/src/routers/admin.ts` — User management + audit log
- `packages/api/src/context.ts` — oRPC context (session, db, user)
- `packages/api/src/lib/access.ts` — verifyPatientAccess() helper
- `packages/api/src/lib/errors.ts` — Typed error helpers

### Types & Utils
- `packages/types/src/auth.ts` — Role/permission type definitions
- `packages/types/src/database.ts` — Entity types (Patient, Medication, etc.)
- `packages/types/src/api.ts` — API request/response types
- `packages/utils/src/bp.ts` — BP classification (HIGH/LOW/NORMAL)
- `packages/utils/src/dates.ts` — Date formatting helpers
- `packages/utils/src/ids.ts` — UUID generation

### Web App
- `apps/web/src/app/layout.tsx` — Root layout with providers
- `apps/web/src/app/page.tsx` — Landing/redirect page
- `apps/web/src/app/login/page.tsx` — Login page
- `apps/web/src/app/dashboard/page.tsx` — Dashboard page (stub)
- `apps/web/src/app/dashboard/dashboard.tsx` — Dashboard component (empty shell)
- `apps/web/src/app/api/rpc/[[...rest]]/route.ts` — oRPC API handler
- `apps/web/src/app/api/auth/[...all]/route.ts` — BetterAuth handler
- `apps/web/src/utils/orpc.ts` — oRPC client + TanStack Query utils
- `apps/web/src/lib/auth-client.ts` — Client-side auth
- `apps/web/src/components/sign-in-form.tsx` — Login form
- `apps/web/src/components/sign-up-form.tsx` — Registration form

### Project Root
- `CLAUDE.md` — This file (project context)
- `DEVELOPMENT_PLAN.md` — Phased development roadmap
- `HANDOFF.md` — Quick-start for new sessions
- `TECH_SPEC.md` — Full technical specification
- `competitive-feature-tracker.csv` — 19 competitors, 145 features, RICE-scored
- `package.json` — Workspace root
- `turbo.json` — Turborepo pipeline config
- `biome.json` — Linting and formatting config
- `lefthook.yml` — Git hooks config

## Architecture Decisions

- **oRPC over tRPC**: Type-safe RPC with better DX, simpler middleware composition
- **BetterAuth over NextAuth**: Simpler setup, native RBAC, session-based auth
- **Drizzle over Prisma**: Lighter weight, faster, SQL-like query builder
- **Every API handler has `verifyPatientAccess()`** — never skip access control. This function checks that the requesting user has permission to access the given patient (owns them or is assigned as caregiver).
- **AI features use Vercel AI SDK with tool calling** — AI can read AND write patient data through structured tool calls (logVital, logMedication, createObservation, etc.)
- **Zod v3 compat for oRPC**: Import `z` from `"zod/v3"` for oRPC input schemas, not plain `zod` or `@orpc/zod`

## Competitive Context

- 19 competitors analyzed (see `competitive-feature-tracker.csv`)
- Only 1 competitor (Caring Village) has AI, and it is buggy
- Blue ocean features: voice-to-task, AI handoff briefing, burnout detection, predictive analytics
- See `DEVELOPMENT_PLAN.md` for full phased roadmap

## Conventions

- All IDs: `text("id").$defaultFn(() => crypto.randomUUID())`
- Indentation: tabs (Biome enforced)
- Quotes: double (Biome enforced)
- oRPC inputs: `import { z } from "zod/v3"` (NOT `@orpc/zod` or plain `zod`)
- DB imports: `import { tableName } from "@WeCareALOT/db/schema/filename"`
- Auth middleware: `requirePermission("domain.action")` or `requireRole("ROLE")`
- Access control: `verifyPatientAccess(patientId, userId, userRole)` in every handler
- BP classification: systolic >= 140 OR diastolic >= 90 = HIGH, systolic < 90 OR diastolic < 60 = LOW, else NORMAL
- Import types from `@WeCareALOT/types`
- Use shadcn/ui components from `@WeCareALOT/ui`
- AI route handlers go in `apps/web/src/app/api/ai/`
- Voice features use Web Audio API for recording, Whisper for transcription, Claude for extraction
- Never hardcode data — always use API with proper role checks
- Mobile-first design with Tailwind responsive classes

## Demo Users (seeded)

| Name | Email | Role | Password | Color |
|------|-------|------|----------|-------|
| AliAnn | aliann@wecarealot.com | FAMILY_ADMIN | carewell2024 | #0F766E |
| Valita | valita@wecarealot.com | CAREGIVER | carewell2024 | #7C3AED |
| Hannah | hannah@wecarealot.com | CAREGIVER | carewell2024 | #D97706 |

## Node Version

Use Bun 1.2.19 as runtime. Node 22 for compatibility if needed (`fnm use 22`).

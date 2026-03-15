# OnePoint! Caregiving Colorado — Session Handoff

## Start Here

1. Read `CLAUDE.md` for full project context (tech stack, schema, API map, conventions)
2. Read `DEVELOPMENT_PLAN.md` for the phased roadmap
3. Read `competitive-feature-tracker.csv` for competitor analysis (19 competitors, 145 features)
4. Read `TECH_SPEC.md` for detailed technical architecture

## Current State (as of 2026-03-15)

| Area | Status |
|------|--------|
| Backend (auth, DB, API, types) | COMPLETE |
| Seed data (Connie + 3 caregivers) | COMPLETE |
| Frontend (login/signup forms) | COMPLETE |
| Dashboard pages | EMPTY SHELL |
| AI features | NOT STARTED |
| Landing page | LIVE at https://jeromyjsmith.github.io/OnePoint/ |
| Competitive analysis | DONE (19 competitors, RICE-scored) |

## What to Build Next

**Phase 1, Week 1: Patient Dashboard + Navigation**

1. Create `apps/web/src/app/dashboard/patients/page.tsx` — role-aware patient list
2. Create `apps/web/src/app/dashboard/patients/[id]/page.tsx` — patient detail with tabs (Overview / Vitals / Meds / Notes)
3. Add sidebar navigation component with role-based menu
4. Wire up to existing `patients.list` and `patients.get` API endpoints
5. Use oRPC client from `apps/web/src/utils/orpc.ts`
6. Use TanStack Query for data fetching (already configured)

## Demo Data

Login with any of these to see different role perspectives. All passwords: `carewell2024`

| User | Email | Role | Sees |
|------|-------|------|------|
| AliAnn | aliann@wecarealot.com | FAMILY_ADMIN | Owns patient Connie, full CRUD |
| Valita | valita@wecarealot.com | CAREGIVER | Assigned to Connie, can log vitals/meds/notes |
| Hannah | hannah@wecarealot.com | CAREGIVER | Assigned to Connie, can log vitals/meds/notes |

Seeded patient: **Connie** — Parkinson's, Dementia, Hypertension. 5 medications, 6 BP readings, 5 observations.

## Key Architecture Patterns

### oRPC Query Pattern
```typescript
// apps/web/src/utils/orpc.ts exports the client and query utils
import { orpc } from "@/utils/orpc";

// In a component — use TanStack Query with oRPC
const { data: patients } = orpc.patient.list.useQuery({
  input: {},
});
```

### Access Control Pattern
```typescript
// Every API handler MUST call verifyPatientAccess
import { verifyPatientAccess } from "../lib/access";

// Inside a procedure handler:
await verifyPatientAccess(input.patientId, ctx.user.id, ctx.user.role);
// Throws FORBIDDEN if user has no access to this patient
```

### AI Route Handler Pattern (for Phase 1 Week 3+)
```typescript
// apps/web/src/app/api/ai/handoff/route.ts
import { createAnthropic } from "@ai-sdk/anthropic";
import { generateText } from "ai";

export async function POST(req: Request) {
  const { patientId } = await req.json();
  // 1. Verify access
  // 2. Fetch last 8 hours of data (vitals, meds, observations)
  // 3. Generate briefing with Claude
  const result = await generateText({
    model: createAnthropic("claude-sonnet-4-20250514"),
    system: "You are a caregiving handoff assistant...",
    prompt: `Generate a shift handoff briefing for: ${JSON.stringify(patientData)}`,
  });
  return Response.json({ briefing: result.text });
}
```

## Files to Know

### Core Infrastructure
| File | Purpose |
|------|---------|
| `packages/db/src/schema/patients.ts` | Patient table definition |
| `packages/db/src/schema/medications.ts` | Medication + medication_log tables |
| `packages/db/src/schema/vitals.ts` | vital_reading + threshold_rule tables |
| `packages/db/src/schema/observations.ts` | Observation table (notes, incidents) |
| `packages/db/src/schema/caregivers.ts` | care_assignment + caregiver_profile |
| `packages/db/src/schema/audit.ts` | Audit log table |
| `packages/db/src/seed.ts` | Demo data seeder |
| `packages/api/src/routers/index.ts` | App router composition (all 7 routers) |
| `packages/api/src/context.ts` | oRPC context (session, db, user) |
| `packages/api/src/lib/access.ts` | `verifyPatientAccess()` — never skip this |
| `packages/auth/src/index.ts` | BetterAuth config with RBAC |
| `packages/types/src/database.ts` | TypeScript types for all entities |
| `packages/utils/src/bp.ts` | BP classification (HIGH/LOW/NORMAL) |

### Web App
| File | Purpose |
|------|---------|
| `apps/web/src/utils/orpc.ts` | oRPC client + TanStack Query utils |
| `apps/web/src/lib/auth-client.ts` | Client-side auth helpers |
| `apps/web/src/app/layout.tsx` | Root layout with providers |
| `apps/web/src/app/dashboard/page.tsx` | Dashboard page (stub — build this out) |
| `apps/web/src/app/api/rpc/[[...rest]]/route.ts` | oRPC API handler |
| `apps/web/src/components/providers.tsx` | App providers (theme, query, auth) |

### Project Root
| File | Purpose |
|------|---------|
| `CLAUDE.md` | Full project context for Claude sessions |
| `DEVELOPMENT_PLAN.md` | Phased roadmap with weekly breakdown |
| `TECH_SPEC.md` | Detailed technical architecture |
| `competitive-feature-tracker.csv` | 19 competitors, 145 features, RICE scores |
| `biome.json` | Linting config (tabs, double quotes) |
| `turbo.json` | Turborepo pipeline config |

## Quick Commands

```bash
cd ~/Desktop/WeCareALOT
bun install              # Install dependencies
bun run dev              # Start all services
bun run db:push          # Push schema changes
bun run db:seed          # Re-seed demo data
bun run check-types      # TypeScript check
bun run check            # Biome lint + format
```

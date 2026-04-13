# META AGENT — Quality Report

**Date:** 2026-04-11
**Scope:** 9 primary research documents + PRD
**QA source:** `99_qa_report.md` (by QA_AGENT) + META AGENT cross-review

---

## Headline Verdict

**PASS WITH ONE BLOCKING REVISION.**

The body of work is internally consistent, source-traceable, and executable. The single blocking item before Saturday's in-person session with Ali Ann is a 5-minute URL verification.

---

## Scorecard

| Document | No Fluff | Real Tools | Sourced | Actionable | Overall |
|----------|:--------:|:----------:|:-------:|:----------:|:-------:|
| `OnePoint_PRD.md` | ✅ | ✅ | n/a | ✅ | **PASS** |
| `10_skill_landscape.md` | ✅ | ✅ | ✅ | ✅ | **PASS** |
| `11_oss_landscape.md` | ✅ | ✅ | ⚠️ (1) | ✅ | **PASS w/ revision** |
| `20_competitor_matrix.md` | ✅ | ✅ | ✅ | ✅ | **PASS** |
| `21_review_intelligence.md` | ✅ | ✅ | ✅ | ✅ | **PASS** |
| `30_gap_analysis.md` | ✅ | ✅ | ⚠️ (1) | ✅ | **PASS w/ revision** |
| `31_ai_advantage.md` | ✅ | ✅ | ✅ | ⚠️ (1) | **PASS w/ revision** |
| `40_system_architecture.md` | ✅ | ✅ | ✅ | ✅ | **PASS** |
| `50_onepoint_strategy.md` | ✅ | ✅ | ✅ | ✅ | **PASS** |

---

## Required Revisions (Ranked)

### 🛑 R1 — BLOCKING (pre-Saturday)
**File:** `11_oss_landscape.md` §A
**Issue:** The Medplum HITRUST/SOC2/HIPAA claim is the single most load-bearing assertion in the stack decision. It must be verified live on `https://www.medplum.com/docs/compliance` before Jero commits to Medplum in the working session.
**Owner:** Jero
**Time to fix:** 5 minutes
**Action:** Open the compliance page, screenshot it, paste the verbatim compliance string into `11_oss_landscape.md` as a quoted citation.

### ⚠️ R2 — NON-BLOCKING (Sunday morning)
**File:** `30_gap_analysis.md` §Segment Opportunity
**Issue:** The ~30,600 Residential Care Community figure sourced to `sr03-47-508.pdf` is the only hard segment-sizing number in the body of work. If that PDF doesn't contain the figure, the $30M–$85M ARR floor claim in `50_onepoint_strategy.md` collapses.
**Owner:** research support
**Time to fix:** 15 minutes
**Action:** Fetch the PDF, search for "30,600" or "residential care community," cite the exact page. If it doesn't verify, replace with a verifiable alternative source (e.g. AHCA/NCAL annual report).

### ⚠️ R3 — NON-BLOCKING (Sunday morning)
**File:** `31_ai_advantage.md` §AI-03 (Medical Research Agent)
**Issue:** The cost-paragraph contains a mid-reasoning "wait, recompute" editorial artifact that survived the first write. The arithmetic is correct but the narrative is unclean.
**Owner:** META AGENT (self-fix)
**Time to fix:** 5 minutes
**Action:** Rewrite the paragraph as a single clean calculation; add an inline link to `https://www.anthropic.com/pricing`; call out the 5% Opus escalation rate as the biggest cost sensitivity.

---

## Consistency Check (Cross-Document)

Spot-checked 7 cross-document dependencies:

| Claim | Doc A | Doc B | Status |
|-------|-------|-------|--------|
| AI cost $6.50/mo/care-recipient | `31_ai_advantage.md` | `50_onepoint_strategy.md` | ✅ Match |
| Sherpa pricing $525/mo/community | `20_competitor_matrix.md` | `50_onepoint_strategy.md` | ✅ Match |
| APFM TCPA settlement $6M | `20_competitor_matrix.md` | `30_gap_analysis.md` + `50_onepoint_strategy.md` | ✅ Match |
| Medplum license = Apache 2.0 | `11_oss_landscape.md` | `40_system_architecture.md` | ✅ Match |
| Krayin license = MIT | `11_oss_landscape.md` | `40_system_architecture.md` | ✅ Match |
| Lucia deprecated | `11_oss_landscape.md` | n/a — used Better-Auth consistently | ✅ No ghost reference |
| Week 1–4 v0 cut covers all P0 stories | `40_system_architecture.md` | `OnePoint_PRD.md` | ✅ Match |

**Zero contradictions detected.**

---

## Hallucination Check

- **15 URLs spot-checked live** by QA_AGENT — all 200 OK.
- **Zero fabricated quotes** detected in `21_review_intelligence.md` — each cluster cites real sources.
- **Zero invented tools** — every recommended skill/OSS/API maps to a real repo or documented endpoint.
- **One citation flagged** for verification: CDC NCHS residential care count (R2 above). Not fabricated, just unverified.

---

## Strengths (What to Preserve)

1. **Traceability discipline.** Every strategic claim in `50_onepoint_strategy.md` cites an upstream doc inline. This is the single highest-value property of the body of work.
2. **Forced decisions.** No "consider X or Y" ambiguity. Every stack choice, every gap, every moat is named and committed.
3. **Cost honesty.** The $6.50/mo AI cost is built bottoms-up from real API pricing, not asserted.
4. **Competitive precision.** ECP is correctly identified as the ONLY real bridge competitor, differentiated on the operator-to-operator vs. family-to-facility axis. This matters — it prevents the common startup failure of either ignoring a real competitor or inflating a fake one.
5. **Segment honesty.** Anti-goals are explicit. OnePoint is not trying to beat Yardi at multi-community ops, and saying so out loud is a strategic asset.

## Weaknesses (Honest)

1. **Thin on international / non-US regulation.** The body of work is CO/CA-centric. This is fine for v0 but the roadmap has no non-US path.
2. **Pricing assumption untested.** $50/care-recipient/month AI budget is a founder guess. One real buyer conversation would replace it with truth.
3. **Skill inventory lean on low-tech web patterns.** FR-7 ("the sister on a flip phone") is the softest-supported requirement — HTMX is a stack choice, not a proven UX pattern for this specific user.
4. **Ianacare / Cariloop / CircleOf / Roobrik** have thin public review surfaces — the competitive picture for employer-sponsored caregiver tools is partially interpolated, not fully observed.

---

## Saturday-Night Readiness

**Is this work ready to hand to Ali Ann?**
**YES**, once R1 is completed.

What Ali Ann should see first:
1. `50_onepoint_strategy.md` — the 15-minute read
2. `30_gap_analysis.md` §Two Segment Opportunities — to validate the Longmont facility is treated as a first-class goal
3. The 7 Critical Open Questions at the end of `50_onepoint_strategy.md` — these drive the Saturday agenda
4. `40_system_architecture.md` §The V0 Cut — the week-by-week plan she can agree or push back on

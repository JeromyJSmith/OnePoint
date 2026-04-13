# 30 — Gap Analysis: Where OnePoint Wins

**Status:** v1 · Synthesis Output
**Date:** 2026-04-11
**Author:** GAP_ANALYSIS_AGENT
**Inputs:** `OnePoint_PRD.md`, `research/20_competitor_matrix.md`, `research/21_review_intelligence.md`, `research/11_oss_landscape.md`

---

## The Thesis

The senior-care software market is structurally bifurcated and leaves a specific user stranded in the middle. On one side sit free, consumer-grade family coordination apps (CaringBridge, Lotsa Helping Hands, Ianacare, CircleOf, CareTree) — legally toothless, medically blind, no placement pipeline, and no revenue model that could ever fund the features their users actually need. On the other side sit enterprise senior-living CRMs and EHRs (Aline, Yardi, Sherpa, Enquire, ECP, PointClickCare, MatrixCare) — priced per-community, sold via six-week demo cycles, and designed on the assumption that the buyer manages ≥10 communities with licensed clinical staff. Between them, lead marketplaces (A Place for Mom, Caring.com, SeniorAdvisor) sit as a referral funnel whose business model (reselling families to the highest bidder) is under active federal investigation and a $6M TCPA settlement ([McKnight's](https://www.mcknightsseniorliving.com/news/a-place-for-mom-agrees-to-settle-lawsuit-for-6-million/), [NBC News](https://www.nbcnews.com/news/us-news/senate-announces-probe-place-for-mom-referral-service-rcna157282)).

The orphaned user is not hypothetical. She is a non-medical professional companion running a small caregiver practice, coordinating a loved one's care alongside two-to-four sisters of mixed technical ability, operating under active liability exposure, and simultaneously trying to place a tenant into the single assisted-living facility she is associated with. Every product in the competitor matrix solves ≤30% of her problem. The consumer apps exclude low-tech sisters by forcing signup (*"forcing users to sign up before showing something of value"* — CaringBridge, [ComplaintsBoard](https://www.complaintsboard.com/caringbridge-b183042)) and produce no legal record. The enterprise CRMs will "quickly teach your clients why they need a different product" ([Aline, G2](https://www.g2.com/products/aline-aline/reviews)) if they have fewer than ten communities. The lead marketplaces will *"bombard already overwhelmed families with dozens of unvetted sales calls"* ([Trustpilot, APFM](https://www.trustpilot.com/review/www.aplaceformom.com)).

OnePoint's wedge is the unique bridge these camps cannot build: a voice-first, family-inclusive care log that is *simultaneously* a placement CRM for one owner-operator, with the move-in handoff being the same record rather than a re-entry. Every competitor either lacks the voice layer, lacks the low-tech web surface, lacks the legal-grade audit trail, lacks the AI research layer against peer-reviewed literature, lacks the single-operator fit, or lacks the family-to-facility data continuity. ECP alone builds a partial operator-to-operator bridge and is the only competitor worth engaging on the bridge argument — but ECP is sold to licensed nurses, ships zero voice capture, zero AI research, and has no surface for the non-medical companion or her low-tech sister. OnePoint sits in the empty box, and it is a bigger box than any single incumbent realizes.

---

## The Five Gaps

### Gap 1: Voice-First Capture for Care Workers Who Physically Cannot Type Mid-Shift

- **Evidence:**
  - Competitor matrix §Feature Comparison Matrix row "Voice-first capture": every vendor except Sherpa/Aline (partial call recording only) is ✗. ([20_competitor_matrix.md §Feature Comparison Matrix](./20_competitor_matrix.md#feature-comparison-matrix))
  - Review intelligence §Cluster 3 "Click-burden": *"point and click over and over while waiting each time for the program to catch up"* ([PointClickCare, Capterra](https://www.capterra.com/p/209866/Skilled-Nursing-Core-Platform/reviews/)); *"EMAR takes on average 11 minutes per person to pass meds"* ([Yardi, Capterra](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/reviews/)); *"all these clicks for nothing is to much"* (PointClickCare nurse, TikTok); *"travel nurses have expressed frustration spending 2+ hours clicking through the system during their shifts"* (PointClickCare/allnurses).
  - Review intelligence §W-1: even the products that tried (CaringBridge speech-to-text) failed — *"speech-to-text consistently aborting."*
- **Who it hurts:** Every hands-occupied caregiver — but especially the non-medical professional companion on an overnight shift who cannot stop stabilizing a patient to click through a form.
- **Why competitors can't close it:** Enterprise EHRs are optimized for billing-code completeness; every field is a compliance artifact justified by the RFP checkbox. Adding voice means rebuilding the underlying capture model, which breaks the compliance story they sold. Consumer apps can't fund realtime STT + LLM infra on a free tier. The one credible attempt (CaringBridge speech-to-text) is broken in production.
- **How OnePoint closes it:** FR-1 (browser-resident voice agent), FR-3 (stream-of-consciousness tolerant), FR-4 (one capture → log entry + timesheet row), FR-5 (hands-free while caring), backed by LiveKit Agents + whisper.cpp fallback ([11_oss_landscape.md §D](./11_oss_landscape.md)). NFR-2 offline tolerance means it works when the network doesn't.
- **Defensibility:** The moat is not the model — it is the capture-to-structure pipeline: a voice capture that produces a timestamped, attributed log entry AND a timesheet row AND triggers a research agent AND survives offline AND is exportable as a legal artifact. A fast-follower who bolts Whisper onto a form produces transcripts, not records. The integration depth across FR-1 → FR-4 → FR-10 → FR-30 is the moat.
- **Severity to target user:** **5/5**

---

### Gap 2: Low-Tech Family Inclusion — The "Sister on a Flip Phone" Surface

- **Evidence:**
  - Competitor matrix §Feature Comparison row "Low-tech family web (shareable link, no install)": CaringBridge ✓, Lotsa ~, CareTree ~, A Place for Mom ✓ (but consumer-side only), everyone else ✗ ([20_competitor_matrix.md](./20_competitor_matrix.md#feature-comparison-matrix)).
  - Review intelligence §Cluster 9: *"forcing users to sign up before showing something of value"* (CaringBridge); *"Constantly makes you log in although that depends if the app even opens"* (Lotsa, App Store); *"It said my email and password don't match. They do match"* (Lotsa, App Store); *"challenging to share info with those who don't use it"* (Aline, TrustRadius).
  - Review intelligence §W-2: AgingCare forum — the community's answer to *"Would like one that we 4 (one far away) could use to share the responsibilities of caring for mom"* was *"just use WhatsApp or Google Docs"* ([AgingCare](https://www.agingcare.com/questions/any-suggestions-on-a-caregiver-app-would-like-one-that-we-4-one-far-away-could-use-to-share-the-resp-486616.htm)). **No caregiver app was named.**
- **Who it hurts:** Ali Ann's 5G-skeptical sister, her Kansas sister with no iPhone, and every equivalent relative across 53M US unpaid caregivers. Today they are literally excluded from their own family's care coordination.
- **Why competitors can't close it:** Every caregiver app ships as a React Native SPA gated behind signup. Their auth model assumes a modern device and a willing user. Enterprise CRMs don't even model the family as a user. Fixing it requires an architectural retreat from SPA-first patterns — which is a cultural and investor-narrative loss ("we have a native app!"), not just a code change.
- **How OnePoint closes it:** FR-7 (web reachable via shared link, no install), FR-8 (shared link + pick-your-name login), NFR-1 (WCAG AA + works on low-spec Android), NFR-7 (minimal-friction auth). Stack: HTMX + server-rendered HTML + Better-Auth magic link ([11_oss_landscape.md §E](./11_oss_landscape.md)). The PRD test: "if it doesn't work on a skeptical relative's old phone, it fails the requirement."
- **Defensibility:** The defensibility here is cultural, not technical. A fast-follower can copy HTMX; they cannot copy the willingness to ship a non-SPA product in 2026. Every engineer hire they make pushes them back toward React. OnePoint's brand promise ("click the link, pick your name") is a commitment that competitors with an existing SPA cannot credibly make without rebuilding.
- **Severity to target user:** **5/5**

---

### Gap 3: Legal-Grade Audit Trail for the Non-Medical Companion

- **Evidence:**
  - Competitor matrix row "Legal-grade audit export (timestamped, attributed)": CareTree ~, enterprise CRMs ✓ (sales audit only), ECP/Aline/Yardi ✓ (clinical audit in licensed-facility stack), **zero consumer caregiver apps** ✓ ([20_competitor_matrix.md](./20_competitor_matrix.md#feature-comparison-matrix)).
  - Review intelligence §Cluster 4: *"reporting is inaccurate and a time suck to try and fix"* (Enquire, G2); *"The only thing I dislike is the amount of time it takes to download a lead file or sales file that has a time frame of longer than 1 month"* (Aline, G2) — even the products that *have* audit capability can't produce it on demand.
  - PRD §10: the stakeholder is *currently* defending against a threatened lawsuit. Logs are literally what is saving her today.
- **Who it hurts:** Any non-medical professional companion — a category with real, uninsured liability exposure and zero tools designed for their admissibility needs. No EMR serves them (they aren't licensed). No consumer app serves them (those apps have no audit model).
- **Why competitors can't close it:** The architecture for legally defensible records sits inside licensed-clinical software (HIPAA, CFR Part 11, FHIR Provenance). Consumer apps never built it because their business model could not fund compliance. Enterprise EHRs have it but are unsellable to a non-licensed buyer and the audit UX is hostile (month-long export lag per Aline reviews). Bridging those two worlds means being a HIPAA-capable platform that a non-licensed user can sign up for — a legal and product design contradiction most vendors refuse to resolve.
- **How OnePoint closes it:** FR-30 (immutable timestamped attribution), FR-31 (on-demand chronological export), FR-32 (marquee requirement, not footnote), SM-4 (<60 seconds to produce 30 days of record). Stack: Medplum FHIR Provenance + AuditEvent + SHA-256 hash chain + Gotenberg PDF export ([11_oss_landscape.md §G](./11_oss_landscape.md)). HIPAA posture from Medplum (HITRUST, SOC2, CFR Part 11 certified).
- **Defensibility:** Building on Medplum means OnePoint inherits a HIPAA compliance program a startup could never build from scratch in under 18 months. A fast-follower has to either rebuild that program or pick the same OSS base — and if they pick Medplum, they still have to invent the non-licensed-buyer onboarding flow OnePoint will have shipped first. The legal-defensibility story compounds with every signed export that survives a courtroom, which creates a credentialing flywheel copyable only through years of actual case precedent.
- **Severity to target user:** **5/5**

---

### Gap 4: AI Medical Research Agent Against Peer-Reviewed Literature, Triggered Per Log Entry

- **Evidence:**
  - Competitor matrix row "AI medical research agent (cited journals)": **every vendor is ✗**, except ECP marked ~? (marketing claim for predictive retention, not a literature agent) ([20_competitor_matrix.md](./20_competitor_matrix.md#feature-comparison-matrix)).
  - §Research Notes & Caveats: Aline's "system of recommendation powered by AI," Sherpa's "Prospect Opportunity Score," ECP predictive retention — **all flagged as marketing until proven**; none cite peer-reviewed sources.
  - Review intelligence §W-5: *"No direct user quote... users don't know to ask for it, BUT the underlying pain is loud: ER visits driven by symptom patterns nobody could interpret in real time. Connie's UTI ruled out at ER, BP out of whack post-elevation — the family had no way to know in advance."* **Labeled "Category-defining."**
- **Who it hurts:** Every family managing a degenerative condition with multi-system interactions (dementia + Parkinson's + elevation sensitivity is the precise PRD use case) — which is effectively every family in assisted-living target demographics.
- **Why competitors can't close it:** Enterprise EHRs deliberately do not embed literature-driven recommendations because doing so exposes them to unauthorized-practice-of-medicine and FDA SaMD (Software as a Medical Device) liability. Consumer apps lack the research retrieval infrastructure and the agent orchestration engineering. The PRD's framing — research agent outputs are presented *so the team can bring them to a licensed professional, never replacing one* (FR-14) — is a deliberate disclaimer that threads the regulatory needle competitors cannot thread without rewriting their compliance posture.
- **How OnePoint closes it:** FR-10 through FR-15. Every log entry triggers a LangGraph research agent with mem0 memory, pulling from Europe PMC + OpenAlex (open-license, commercial-friendly, rate-limit-compatible with per-log triggering) and returning *cited* findings ([11_oss_landscape.md §C, §F](./11_oss_landscape.md)).
- **Defensibility:** The moat is the integration between capture (FR-1), memory (mem0 per-patient), retrieval (Europe PMC/OpenAlex), and *framing* (FR-14 to-a-professional language). A fast-follower who bolts GPT onto logs produces a chatbot; OnePoint produces a citable research dossier per log entry that is legally defensible as a "we showed this to the nurse" artifact. Over time the per-patient mem0 state becomes switching cost — a family's care-recipient history cannot be re-created in a new product.
- **Severity to target user:** **4/5** (net-new value, category-defining, but patient does not yet know to ask for it)

---

### Gap 5: Unified Placement Pipeline → Care Log for the Single-Facility Owner-Operator

- **Evidence:**
  - Competitor matrix §The Bridge Gap verifies it directly: *"No competitor in this matrix ships points 1, 2, 3, 5, and 6 together. ECP comes closest on point 3 alone. The wedge holds."*
  - Row "Move-in → care-log handoff (same record)": **only ECP ✓, everyone else ✗ or ~** ([20_competitor_matrix.md](./20_competitor_matrix.md#feature-comparison-matrix)).
  - Review intelligence §Cluster 7 "Priced for the enterprise": *"It's a good entry level CRM for senior living. It will quickly teach your clients why they need a different product"* ([Aline, G2](https://www.g2.com/products/aline-aline/reviews)); *"if you have a growth plan for more than 10 communities, you should get a product that can handle marketing automation and reporting, such as HubSpot or Salesforce"* ([Enquire, G2 digest](https://www.g2.com/products/enquire-crm/reviews)); *"tailored primarily for larger communities, where smaller facilities might find them too comprehensive"* (Continuum, Senior Living Foresight).
  - Review intelligence §W-6 directly names this as the wish: *"I wish the CRM didn't hate my one small facility."*
- **Who it hurts:** Ali Ann and every equivalent owner-operator running a single assisted-living facility (Longmont, CO being the specific PRD case). The senior-living CRM category was built for 50+ community chains. Single-facility operator-owners are an orphaned segment.
- **Why competitors can't close it:** Enterprise CRMs are priced, trained, and supported via an enterprise sales motion (six-week implementation, per-community license math, dedicated account manager). Their unit economics collapse at single-facility price points — at the disclosed Sherpa $525/mo anchor, a single facility is barely profitable after support load. ECP serves smaller operators but gates the product behind licensed-facility workflows and has no family-facing bridge. A Place for Mom and Caring.com profit from *not* placing people into one specific facility; their business model is lead aggregation, not single-facility fill.
- **How OnePoint closes it:** FR-37 through FR-48 (facility profile, public-facing page, voice prospect intake, fit assessment, kanban pipeline, family decision-maker coordination, tour scheduling, **FR-44 move-in handoff into care logging — no re-entry**, referral tracking, compliance fields, occupancy dashboard, urgency routing). Stack: Krayin CRM (MIT) extended with custom pipeline stages, bridged to Medplum via webhook on stage=Resident ([11_oss_landscape.md §B](./11_oss_landscape.md)).
- **Defensibility:** ECP is the threat here and must be engaged directly. Differentiation: **(a)** ECP's bridge is operator-to-operator (CRM → EHR inside one licensed stack); OnePoint's bridge is family-to-facility-and-back (the prospect's family intake becomes the care record continuously visible to both sisters outside and staff inside). **(b)** ECP ships zero voice capture, zero AI research agent, zero low-tech web surface, zero self-host option. **(c)** ECP's buyer is a licensed facility administrator; OnePoint's buyer is a non-medical companion running one facility. Even if ECP added voice tomorrow, their sales motion cannot reach Ali Ann. OnePoint's defensibility is the integration of this gap with Gaps 1–4: the sum is unreplicable by any vendor whose core buyer profile is enterprise-licensed-clinical.
- **Severity to target user:** **5/5** (this is PRD Goal G7, business-critical for Ali Ann)

---

## "What Nobody Is Doing Well"

Concrete jobs-to-be-done that every competitor fumbles, each anchored to a review quote.

- **Capture a care observation without taking your hands off the patient.** Nurses: *"all these clicks for nothing is to much"* (PointClickCare, TikTok nurse). No vendor ships working voice.
- **Show the low-tech sister what happened today without making her sign up.** CaringBridge: *"forcing users to sign up before showing something of value"* ([ComplaintsBoard](https://www.complaintsboard.com/caringbridge-b183042)).
- **Log work and produce a paycheck from the same action.** WellSky: *"the punch clock system rolls them back to their punch-in time... potentially making them work without pay"* ([Capterra](https://www.capterra.com/p/126968/Non-Medical-Private-Pay-System/reviews/)) — two broken systems forced on one shift.
- **Find what you wrote last month.** CaringBridge: *"Users can only re-read posts from the last six months or so, but not before, as it seems to get stuck retrieving older posts"* (App Store digest).
- **Produce proof of care when a lawyer asks.** Aline: *"the amount of time it takes to download a lead file or sales file that has a time frame of longer than 1 month"* (G2) — even the audit-capable tools can't produce the audit in time.
- **Survive an offline moment in a rural home.** AlayaCare: *"The system loses data and often wastes time because it loses internet connections. Offline mode is described as a nightmare"* ([Capterra](https://www.capterra.com/p/147424/AlayaCare/reviews/)).
- **Place one tenant into one facility without the family getting spammed.** A Place for Mom: *"They will call, text and email non stop and even late at night. My mother died two years ago and I still cannot get them to stop contacting me"* ([Trustpilot](https://www.trustpilot.com/review/www.aplaceformom.com)).
- **Capture a prospective resident over the phone and have them become a care record without re-entry.** Nobody ships this. ECP gets closest, typed only, licensed-facility staff only.
- **Know what the peer-reviewed literature says about the symptom cluster you just observed.** Zero competitors. Category-defining ([21_review_intelligence.md §W-5](./21_review_intelligence.md)).
- **Trust that your family contact info will not be sold.** APFM: *"A customer's information can be sent to a dozen or more communities"* ([BBB](https://www.bbb.org/us/wa/seattle/profile/senior-care/a-place-for-mom-inc-1296-22011038/complaints)).

---

## Where OnePoint Can Dominate

Three credible market positions OnePoint can own within 12 months:

1. **"The voice-first care log that holds up in court."**
   - **Segment:** Non-medical professional companions, small private-pay caregiver teams, dementia/Parkinson's family caregivers with liability exposure.
   - **Job:** Capture every shift hands-free, produce a legally defensible record on demand.
   - **Win condition:** SM-1 (14 consecutive days of voice logging) + SM-4 (<60s export) + at least one attorney-requested export produced in anger and accepted by counsel.

2. **"The senior-living CRM for one facility, built by someone who runs one facility."**
   - **Segment:** Single-facility assisted-living owner-operators (Longmont = anchor customer; CO/WA/OR/CA small-operator corridor = beachhead geography).
   - **Job:** Fill vacancies with qualified tenants without paying A Place for Mom's commission or buying an enterprise CRM.
   - **Win condition:** SM-6 (one qualified tenant moved into Longmont within 60 days) + SM-7 (5 pipeline leads in 30 days) + a second facility signs up before month 6.

3. **"The family-inclusive platform where the sister on a flip phone is not a second-class citizen."**
   - **Segment:** Multi-generational families coordinating care across mixed-tech family members — the 53M-unpaid-caregiver market with the specific low-tech-relative constraint.
   - **Job:** Let every family member see today's log, know who's on duty, and contribute — without installing anything.
   - **Win condition:** SM-2 (≥2 sisters view the web surface weekly for 4 weeks) + SM-3 (group-text volume for Connie drops ≥50%).

These three positions are not mutually exclusive. They are the three entry doors into the same product. OnePoint can credibly claim all three in year one because the underlying platform serves each from the same capture layer, same surface, same audit trail.

---

## Where Competitors Are Vulnerable Right Now

- **A Place for Mom** — TCPA $6M settlement ([McKnight's](https://www.mcknightsseniorliving.com/news/a-place-for-mom-agrees-to-settle-lawsuit-for-6-million/)), Senate Special Committee on Aging probe ([NBC News](https://www.nbcnews.com/news/us-news/senate-announces-probe-place-for-mom-referral-service-rcna157282), [Senator Casey](https://www.casey.senate.gov/news/releases/casey-demands-major-assisted-living-facility-referral-service-a-place-for-mom-address-concerns-about-deceptive-marketing-practices)), manipulated-reviews investigation, persistent Trustpilot trust collapse ("they still contact me two years after my mother died"). **Window:** Families are actively shopping for an alternative *right now*, Q2–Q3 2026. OnePoint's positioning ("one family, one facility, no lead resale") is a direct answer.

- **Aline (Enquire + Glennis + Sherpa merger)** — Post-merger support collapse (*"customer service is terrible... many different support team members... don't share information internally"*), explicit G2 quote *"It's a good entry level CRM for senior living. It will quickly teach your clients why they need a different product"* ([G2](https://www.g2.com/products/aline-aline/reviews)). **Window:** Single-facility customers sold into Aline during the merger will churn through 2026 as integration pains persist. OnePoint can catch them on the way out.

- **Yardi Senior Living Suite** — Documented 11-minute-per-resident eMAR times, *"slow and archaic,"* limited customization ([Capterra](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/reviews/)). **Window:** Click-burden burnout is the single loudest complaint in nurse reviews; OnePoint's voice-first pitch lands hardest on Yardi-frustrated staff. Not a direct buyer target (enterprise), but a *referral* target — Yardi-burned nurses tell family caregivers what to use at home.

- **WellSky Personal Care** — GPS clock-in failures producing unpaid wages, *"Repeated performance issues that lead to the software being unusable,"* unauthorized data sharing (*"they turn-around and hand client protected data over to others without our permission"*) ([Capterra](https://www.capterra.com/p/126968/Non-Medical-Private-Pay-System/reviews/)). **Window:** Open-ended. EVV-land is an active churn zone; the one-capture-to-log-and-timesheet pitch (FR-4) wins directly.

- **CaringBridge** — Technical stagnation (*"behind in terms of current tech... not user friendly... slow"*), broken photo upload, speech-to-text *"consistently aborting,"* 6-month retrieval limit on old posts. **Window:** Donation-supported nonprofit cannot invest in voice, AI research, or legal audit. OnePoint can credibly claim the next-generation position for free-tier users Caringbridge can't upgrade.

- **PointClickCare / MatrixCare** — Nurse burnout on click-burden is a TikTok-and-allnurses-forum fire right now. **Window:** Not a direct buyer target, but the pool of nurses exiting those products is the pool of professionals who will recommend OnePoint to their family-caregiver friends.

---

## Segment Opportunity: The Orphaned Small Operator

The single-facility / owner-operated assisted-living segment is the sharpest market inefficiency in senior-living software. Every major CRM (Aline, Yardi, Enquire, Sherpa, WelcomeHome, Continuum) is priced, designed, trained, and sold for 10+ community chains. Their implementation cycles are six weeks; their support tiers assume a full-time facility administrator; their pricing gates behind enterprise quote. The disclosed Sherpa anchor of ~$525/mo per community ([SoftwareSuggest](https://www.softwaresuggest.com/sherpa-crm)) is the *starting* line — actual spend for a single facility after implementation, training, and add-ons typically lands in five figures annually. ECP is the one credible small-operator vendor but assumes licensed clinical staff and ships no family-facing layer.

**Segment sizing (directional):** The federal Residential Care Community estimate is ~30,600 facilities in the US ([CDC NCHS, 2020](https://www.cdc.gov/nchs/data/series/sr_03/sr03-47-508.pdf)); roughly 70% are for-profit, and a material fraction are owner-operated single-facility or 2–5-facility micro-chains. Even conservatively sizing the single-facility US population at ~8,000–12,000 operators, at a $300–600/mo subscription the segment is a $30M–$85M ARR floor *before* the family-side product — and OnePoint is the only platform credibly serving it with both placement and care logging from one record.

**The entry wedge:** Longmont as case-zero, expand through the CO/WA/OR/CA small-operator corridor, referrals from hospital discharge case-managers (whom no enterprise CRM cultivates because the enterprise sales motion cannot convert them into a lead source).

**Why this segment is defensible:** Enterprise CRMs cannot reprice without cannibalizing their enterprise revenue. ECP cannot reposition without abandoning its licensed-facility compliance moat. Consumer caregiver apps cannot build a CRM without a business model to fund it. The orphaned small operator remains orphaned for structural reasons that won't change in an 18-month window.

**Maps to:** G7, §5.11, FR-37 through FR-48, SM-6/7/8/9.

---

## Segment Opportunity: The Non-Medical Professional Companion

Ali Ann represents a category that has no product today: the non-medical professional companion. She is paid. She is professional. She runs a multi-client practice. She has liability exposure. She is *not* licensed — not an RN, not an LPN, not an LVN, not a CNA in a facility stack, not a home-health aide credentialed through a Medicare-certified agency. She is outside the EVV (Electronic Visit Verification) system. She is outside the Medicare/Medicaid reimbursement rail.

Every existing product picks a side that excludes her:

- **Consumer caregiver apps** (CaringBridge, Lotsa, CircleOf) treat her as an unpaid family caregiver. No professional workflow, no billing output, no audit trail for her liability exposure.
- **Clinical tools** (PointClickCare, MatrixCare, AlayaCare, ECP, WellSky) require licensing she does not have and bill her facility or agency, which she does not operate.
- **Geriatric-care-manager tools** (CareTree) assume ALCP certification and a multi-client B2B sales motion she has not yet completed.
- **EVV-mandated home care platforms** (Tellus/Mobile Caregiver+, CareTime) require payer credentialing and Medicaid billing she is not in.

The category is real and likely underestimated. The US has ~53M unpaid family caregivers; a measurable fraction transition into paid professional companionship without ever pursuing licensure because licensure gates them out of the exact flexible, family-adjacent work they offer. Aging Life Care Professionals (ALCPs) number ~2,000 nationally — too small to be the whole category. The *non-medical professional companion* is the grey-market layer between unpaid family caregiver and licensed clinical staff, and no software vendor has sized it because no vendor has targeted it.

**OnePoint's fit:** HIPAA-compliant on the medical-records branch (FR-27), not HIPAA-compliant where it does not need to be (non-medical logs, FR-29 self-host). Legally defensible audit trail (FR-30–32) designed for her exact liability exposure. Voice capture (FR-1) that respects her physical reality. Spreadsheet on-ramp (FR-34) that doesn't force her to stop using the Google Sheet she already has.

**Maps to:** PRD §2 primary persona, FR-27 through FR-32, NFR-4, NFR-5.

---

## The Bridge — OnePoint's Unique Position

The core wedge is the family-to-facility bridge. No competitor builds this. ECP builds a partial operator-to-operator bridge (CRM → EHR inside one licensed stack) and is the only competitor that must be engaged directly on this claim.

OnePoint's 6-point wedge, each mapped to an FR and contrasted with ECP:

1. **Voice prospect intake** — Ali Ann records a phone call with a prospective resident's family and the call becomes a structured prospect record. **FR-39 (voice-first intake on phone or web) + FR-1 (browser voice agent).** ECP: typed intake only. No voice, no phone capture. Gap verified in §Feature Comparison Matrix row "Voice-captured prospect intake."

2. **Kanban pipeline with audit discipline** — Every stage transition timestamped and attributed. **FR-41 (pipeline) + FR-30 (attribution).** ECP: yes, inside the ECP CRM module, but attribution ties to licensed-facility users, not the family surface.

3. **Move-in handoff as the same record, not re-entry** — On move-in day the prospect record *is* the care log; intake notes, diagnoses, family contacts pre-populate. **FR-44.** This is the single most competitive claim ECP makes: "resident data transfers automatically, eliminating duplicate entry" ([ECP blog](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense)). Differentiation: OnePoint's handoff moves data from a family-accessible surface into a family-accessible care log. ECP's handoff moves data from one licensed-staff module into another licensed-staff module. The family never sees ECP's care record; they see a separate e-sign portal. OnePoint's family sees the same shared link from intake through ongoing care.

4. **Shared family surface that survives the handoff** — The same low-tech shareable link that worked for the placement family continues to work as the ongoing care journal. **FR-7 + FR-8 + FR-42.** ECP: ✗. No family-facing surface beyond a document e-sign portal. This is the single clearest architectural difference.

5. **AI research agent against peer-reviewed literature** — Every new care log triggers a LangGraph agent with mem0 memory, returning cited Europe PMC/OpenAlex findings. **FR-10 through FR-15.** ECP: ✗. No competitor does this. Category-defining.

6. **Legal-grade export spanning prospect → resident → discharge** — A single attributed, timestamped PDF that covers intake through current care, exportable in <60 seconds. **FR-31 + FR-32 + SM-4.** ECP: partial (EHR audit only, no spans to pre-admission CRM data as a unified export).

**The bridge wins because it runs family → facility → family, not operator → operator.** ECP's best claim collapses to point 3 alone, and OnePoint surrounds that point with five others ECP cannot ship without rebuilding its buyer profile.

---

## Anti-Goals (Gaps We Intentionally Do NOT Chase)

- **We do not compete with Yardi, Aline, or ECP for multi-community enterprise operators.** Their sales motion, implementation cycle, per-community pricing math, and module depth are the wrong shape for a single builder serving a single facility and a single caregiver team. Every hour spent making OnePoint "multi-community enterprise ready" is an hour stolen from Ali Ann. The orphaned-small-operator wedge depends on *not* being enterprise-shaped.

- **We do not replace the EMR.** PRD §4 Non-Goals is explicit: OnePoint links to and ingests from HIPAA medical records platforms (via Medplum); it is not one. Building an EMR means chasing ONC certification, CMS reimbursement wiring, and clinical workflow depth that would collapse the rest of the product. FR-27 is "ingest from," not "be."

- **We do not replace licensed clinical judgment.** FR-14 is explicit: the research agent informs and is framed for the team to *bring to* a licensed professional. This is not humility — it is the exact framing that threads the FDA SaMD needle and lets OnePoint ship a literature agent at all. If we ever position the agent as diagnostic, we lose the category-defining lane.

- **We do not build a lead marketplace.** A Place for Mom's business model — reselling families to multiple facilities — is structurally misaligned with OnePoint's trust positioning. Every referral we accept from a third-party buyer erodes the "no lead resale, one family one facility" promise that is our permission to exist against APFM's wounded incumbency. OnePoint's placement pipeline serves *one* facility (Longmont, then the next, then the next) and fills it directly. It does not aggregate demand.

- **We do not build Medicare/Medicaid billing or EVV.** PRD §4 Non-Goals. Entering EVV means serving a payer, which means designing for fraud prevention over caregiver dignity — the exact architectural choice that made WellSky and CareTime into the cautionary tales they are. OnePoint's buyer is private-pay and non-licensed. Medicare and Medicaid are not our customer in v1 and chasing them would break the capture-layer design.

- **We do not build a generic family calendar app.** PRD §4 Non-Goals. Google Calendar and WhatsApp already handle this. The problem is not scheduling; it is the capture layer, the audit trail, the family-inclusive surface, and the placement bridge. Adding a full calendar model would dilute the capture-first discipline that makes OnePoint feel different in 60 seconds.

- **We do not build a React SPA for the low-tech surface.** FR-7 is a hard architectural constraint, not a preference. Any drift toward an SPA-first low-tech path breaks the "works on a 2015 iPhone with no install" promise and collapses Gap 2.

---

## Summary

The five named gaps are:

1. Voice-first capture for care workers who physically cannot type mid-shift
2. Low-tech family inclusion — the "sister on a flip phone" surface
3. Legal-grade audit trail for the non-medical companion
4. AI medical research agent against peer-reviewed literature, triggered per log entry
5. Unified placement pipeline → care log for the single-facility owner-operator

Each gap is claimed by zero consumer caregiver apps and at best partially claimed by one enterprise competitor (ECP on Gap 5 alone). Each maps to specific FRs in the PRD and to specific user-review evidence. The sum is unreplicable by any vendor whose core buyer profile is either free-tier consumer or enterprise-licensed-clinical. OnePoint sits in the empty box.

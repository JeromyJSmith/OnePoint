# 20 — Competitor Matrix

**Scope:** OnePoint competitive analysis across two adjacent markets — family caregiver coordination tools and senior living placement / CRM systems. All claims sourced inline. Unverified vendor marketing is flagged.

**Date:** 2026-04-11
**Owner:** COMPETITOR_AGENT

---

## Summary

The market bifurcates cleanly into two non-overlapping camps: **(1) consumer-grade family caregiver coordination apps** (CaringBridge, Lotsa Helping Hands, Ianacare, CircleOf, CareTree, Cariloop) that are free or employer-sponsored, low-stakes, and legally toothless; and **(2) enterprise senior living CRM / operations suites** (Aline, Yardi, ECP, WelcomeHome, Sherpa — now consolidated under Aline) that are sold to multi-community operators for thousands of dollars per community per month. Lead marketplaces (A Place for Mom, Caring.com, SeniorAdvisor.com) sit adjacent to segment 2 as a funnel rather than a system of record. The consumer segment has zero placement pipeline, zero legal-grade audit, and no medical research layer; the enterprise segment has zero voice-first capture, zero low-tech family inclusion, and its care logging is an eMAR compliance checkbox, not a journal-style log. **Only ECP credibly claims a "CRM-to-EHR bridge," but it is sold into licensed 8,000-community operators and has no family-facing layer, no voice capture, no AI research agent, and no low-tech sister entry point** ([ECP all-in-one](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense)). OnePoint's wedge is the hybrid: a voice-first, family-inclusive care log that is *also* a placement CRM for an owner-operator running a single facility, with move-in data flowing into the care record automatically.

---

## Segment Map

| Vendor | Care Coordination (family-facing) | Placement CRM (facility-facing) | Both |
|---|---|---|---|
| CareZone (defunct / acquired) | ✓ (was) | — | — |
| CaringBridge | ✓ | — | — |
| Lotsa Helping Hands | ✓ | — | — |
| Ianacare | ✓ | — | — |
| Cariloop | ✓ (concierge) | — | — |
| CircleOf | ✓ | — | — |
| CareTree | ✓ (+ ALCP pro use) | — | — |
| Enquire (now Aline) | — | ✓ | — |
| Yardi Senior Living Suite | partial (eMAR) | ✓ | partial |
| Sherpa CRM (now Aline) | — | ✓ | — |
| Aline (merged co.) | partial (Aline Care eMAR) | ✓ | partial |
| ECP Lead Cloud / ECP CRM | partial (eMAR, EHR) | ✓ | **claimed** |
| Roobrik | — | ✓ (top-of-funnel only) | — |
| A Place for Mom | — | adjacent (marketplace) | — |
| Caring.com | — | adjacent (marketplace) | — |
| SeniorAdvisor.com | — | adjacent (marketplace) | — |
| **OnePoint (target)** | **✓** | **✓** | **✓ (first-class)** |

The "both" column is nearly empty. The only credible entrant is ECP, and the bridge they describe is enterprise-to-enterprise (CRM module → EHR module inside one licensed facility stack), not family-log-to-placement-record. Details in **The Bridge Gap** section below.

---

## Per-Competitor Deep Dives

### 1. CareZone — *defunct as originally branded*
- **Target customer:** Consumer family caregivers managing medications and health info for a loved one.
- **Status:** Acquired by Walmart in 2020; original app taken offline around May 2021. A re-branded "Medisafe CareZone: PillMemo" app exists under Medisafe, but this is effectively a medication reminder app, not the original care coordination product ([Tech-enhanced Life](https://www.techenhancedlife.com/reviews/carezone-medication-app), [App Store](https://apps.apple.com/us/app/medisafe-carezone-pillmemo/id6499107849)).
- **Pricing:** Free.
- **Core features (legacy):** Medication list, pharmacy scan, notes, shared calendar.
- **Integrations:** None meaningful post-acquisition.
- **Strengths:** Brand recognition; pill-bottle OCR was a breakout feature pre-shutdown.
- **Weaknesses:** Discontinued as a coordination platform; users lost data in the Walmart transition.
- **Bridges care ↔ placement?** No. Never attempted.

### 2. CaringBridge
- **Target customer:** Families sharing health-journey updates with a broad friend-and-family audience during illness. 501(c)(3) nonprofit ([CaringBridge](https://www.caringbridge.org/)).
- **Pricing:** Free, donation-supported.
- **Core features:** Personal "site" per patient, journal posts, SupportPlanner task/meal calendar, guestbook, photo gallery ([CaringBridge resources](https://www.caringbridge.org/resources/what-is-caringbridge)).
- **Integrations:** GoFundMe partnership for donations ([GoFundMe](https://www.gofundme.com/partners/caringbridge)); no EHR, no wearables.
- **Strengths:** Enormous brand trust, hospital partnerships (UChicago Medicine, Inova list it officially), true low-friction web experience.
- **Weaknesses:** "Behind in terms of current tech... not user friendly... slow" per user reviews ([ComplaintsBoard](https://www.complaintsboard.com/caringbridge-b183042)); donation UX is confusing — users believe they are funding a specific patient when funds go to the nonprofit ([Sitejabber](https://www.sitejabber.com/reviews/caringbridge.org)); no structured medical data, no audit trail, no voice capture.
- **Bridges care ↔ placement?** No.

### 3. Lotsa Helping Hands
- **Target customer:** Caregiver support communities coordinating meals, rides, visits for a family in crisis. Over 1M caregivers in network ([Lotsa](https://caregiver.lotsahelpinghands.com/how/)).
- **Pricing:** Free.
- **Core features:** Help Calendar (flagship), message board, personal blog, photo sharing, document storage ([Lotsa How It Works](https://lotsahelpinghands.com/how-it-works)).
- **Integrations:** Hosted white-label editions for disease associations (lung, healing, aamds subdomains).
- **Strengths:** Dominant brand in meal-train / task-signup; nonprofit-aligned; partnerships with disease foundations.
- **Weaknesses:** Interface reportedly dated — Play Store users say the app "needs a massive facelift"; App Store users report the calendar icon "DOES NOTHING" and the app is list-view-only ([Lotsa on Play Store](https://play.google.com/store/apps/details?id=com.lotsahelpinghands.android.lotsa)). No medication tracking, no vitals, no research layer, no audit export.
- **Bridges care ↔ placement?** No.

### 4. Ianacare
- **Target customer:** Working family caregivers whose employer sponsors the benefit; also available direct-to-consumer ([Ianacare](https://ianacare.com/)).
- **Pricing:** Core Caregiver Organizer is free; "Ianacare Plus" (Caregiver Navigator concierge, employer resources) is gated behind employer sponsorship ([Ianacare support](https://support.ianacare.com/hc/en-us/articles/35224600644621-What-is-ianacare-and-what-do-I-have-access-to)). Enterprise per-employee pricing not publicly disclosed.
- **Core features:** Team feed, task requests, Amazon wishlist / gift-card / money requests, calendar, notifications via email/SMS/push, Caregiver Navigator concierge (enterprise tier) ([Ianacare how-to](https://support.ianacare.com/hc/en-us/articles/30555221162509)).
- **Integrations:** Employer benefits platforms; enterprise clients include Koch, HPE ([Ianacare Koch](https://ianacare.com/koch/), [HPE](https://ianacare.com/hpe/)).
- **Strengths:** Human Navigator concierge layer (differentiator vs. pure software); enterprise distribution through employers.
- **Weaknesses:** No care log / vitals / medication discipline; no defensibility story; enterprise sales motion means single families without an employer sponsor get the free-tier-only experience.
- **Bridges care ↔ placement?** No. Navigators refer out but do not operate a placement pipeline.

### 5. Cariloop
- **Target customer:** Large employers offering caregiver benefits; nearly 2M employees covered ([Cariloop](https://cariloop.com)).
- **Pricing:** Sold B2B to employers; per-employee-per-month, not publicly disclosed. Claims 3x employer ROI ([Cariloop employers](https://cariloop.com/employers)).
- **Core features:** 1:1 matching with licensed Care Coach (RN, LCSW, LMSW, PT, OT, etc.), document vault, secure messaging ([Cariloop coaching](https://cariloop.com/solutions/caregiver-support-platform/coaching)).
- **Integrations:** Benefitfocus catalog ([Benefitfocus Cariloop](https://www.benefitfocus.com/solutions/catalog/cariloop/caregiver-support-platform)); university HR portals (MSU, SMU).
- **Strengths:** Licensed-professional human layer is the product, not software; clear HR buyer; established ROI narrative.
- **Weaknesses:** Coach-driven, not data-driven — no voice capture, no AI research, no timeline of vitals. Software is thin compared to the concierge. Not accessible to non-enterprise families.
- **Bridges care ↔ placement?** Coaches advise on placement verbally; no pipeline data model.

### 6. CircleOf
- **Target customer:** Family caregivers wanting a combined task/med/document/chat app ([CircleOf](https://circleof.com/)).
- **Pricing:** Free core app; marketplace partners monetize via discounts.
- **Core features:** Tasks, medication/refill reminders, drug interaction warnings, private chat, video calls, document storage, caregiver marketplace ([App Store](https://apps.apple.com/us/app/circleof-by-myways-io/id1298712207)).
- **Integrations:** Marketplace partners (home health products, meal delivery, legal essentials).
- **Strengths:** Broadest *feature* coverage in the consumer segment (meds + tasks + chat + video + docs); 4.5 Apple / 4.0 Google ratings.
- **Weaknesses:** Small user base (48 Apple reviews, 86 Google reviews per listings) suggests limited traction. No audit export, no HIPAA posture, no research layer.
- **Bridges care ↔ placement?** No.

### 7. CareTree
- **Target customer:** **Aging Life Care Professionals (ALCPs) / geriatric care managers** who need a client portal for families — this is an important nuance. CareTree is sold to the *professional* running the case, not direct-to-family ([CareTree Families](https://www.caretree.me/families)).
- **Pricing:** Not publicly disclosed; sold B2B to ALCP practices.
- **Core features:** Per-client profile, activity feed, centralized health records, medication list, vitals tracking, document storage, calendar ([CareTree communication](https://web.caretree.me/communication)).
- **Integrations:** Internal only, per available documentation.
- **Strengths:** Closest market-fit analog to Ali Ann's professional-companion model — it is designed for a paid non-medical coordinator running multi-client care. Activity feed has audit-trail discipline.
- **Weaknesses:** Users report "glitches and bug fixes" needed; receipt uploads and note posting break ([CareScout](https://www.carescout.com/resources/the-best-apps-for-caregivers-7-tools-to-make-caregiving-easier)). No voice capture, no AI research, no placement pipeline, no facility profile, no low-tech-sister web surface.
- **Bridges care ↔ placement?** No. ALCPs who use CareTree refer out to placement agencies or A Place for Mom.

### 8. Enquire (now Aline)
- **Target customer:** Senior living operators managing the sales funnel. Merged into Aline in 2023 ([Senior Housing News](https://seniorhousingnews.com/2023/05/04/senior-living-tech-company-formed-by-merger-of-glennis-enquire-sherpa-rebrands-as-aline/)).
- **Pricing:** Not publicly disclosed; enterprise sales motion via demo request ([Capterra Enquire→Aline](https://www.capterra.com/p/174910/Aline/)).
- **Core features:** Lead pipeline, tour tracking, lead-to-speed metrics, activity snapshots, tour-to-occupancy reporting ([Capterra reviews](https://www.capterra.com/p/174910/Aline/)).
- **Integrations:** Aline's 100+ partner ecosystem post-merger.
- **Strengths:** Purpose-built for senior living sales teams; modern UI relative to Yardi.
- **Weaknesses:** "Going through growing pains in account support... many different support team members... don't share information internally" ([Capterra review](https://www.capterra.com/p/174910/Aline/reviews/)). "Limited capacity to customize" ([Capterra Yardi vs Enquire](https://www.capterra.com/assisted-living-software/compare/174910-164514/)). Enterprise sales gate excludes owner-operators.
- **Bridges care ↔ placement?** Partial — within Aline's suite, CRM data can flow into Aline Care, but this is a within-product handoff in an enterprise stack, not a family-facing bridge.

### 9. Yardi Senior Living Suite
- **Target customer:** Enterprise senior living operators; incumbent multi-community player ([Yardi Senior Living](https://www.yardi.com/market/senior-living/)).
- **Pricing:** Not publicly disclosed; per-unit module-based pricing is standard Yardi practice. Not publicly listed ([Capterra Yardi](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/)).
- **Core features:** Voyager Senior Housing (finance/accounting), RentCafe Senior CRM (sales), EHR, eMAR, activities, marketing ([Yardi Voyager](https://www.yardi.com/product/voyager-senior-housing/)).
- **Integrations:** Yardi's proprietary ecosystem; open integration is not Yardi's strength.
- **Strengths:** Single database across finance, sales, care; recent updates include gender/pronouns on prospect profiles ([Yardi blog](https://www.yardi.com/blog/news/senior-living/explore-new-functionality-yardi-senior-living-suite/38133.html)).
- **Weaknesses:** **eMAR takes ~11 minutes per resident to pass meds** due to slow load times per Capterra reviewer; "slow and archaic," monthly load-time frustration reports, "no emergency backup system other than emailing to users," limited customization ([Capterra Yardi reviews](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/reviews/)). Built for chains, hostile to owner-operators.
- **Bridges care ↔ placement?** Within the enterprise suite, yes — sales → care → billing. But family-facing and voice-first capture are absent.

### 10. Sherpa CRM (now Aline)
- **Target customer:** Senior living sales teams; merged into Aline in 2023 but brand still surfaces ([Aline / Sherpa](https://sherpacrm.com/solutions/)).
- **Pricing:** **$525/month starting** per one third-party listing ([SoftwareSuggest](https://www.softwaresuggest.com/sherpa-crm)) — unusually a disclosed number for this segment; treat as starting tier, per-community.
- **Core features:** Call recording, transcription, call summaries, Prospect Opportunity Score, Daily Lineup ranked call list, lead summaries, methodology-based sales coaching ([Sherpa Solutions](https://sherpacrm.com/solutions/crm/)).
- **Integrations:** PointClickCare, Yardi, RealPage, Eldermark, Alis ([SoftwareSuggest Sherpa](https://www.softwaresuggest.com/sherpa-crm)).
- **Strengths:** Sales methodology + software combo is unique in segment; call recording + AI summaries are a real feature, not vaporware; strong integration surface.
- **Weaknesses:** Sales-only — no care log, no family portal. Now folded into Aline, so Sherpa-branded product lifecycle is in transition. Prospect Opportunity Score is undocumented under the hood — flagged as unverified-specific-mechanism.
- **Bridges care ↔ placement?** No — outbound integration pushes contact info to PointClickCare/Yardi EHRs, but that is data export, not a bidirectional care-record bridge.

### 11. Aline (the merged company — Enquire + Glennis + Sherpa)
- **Target customer:** Multi-community senior living operators, post-acute, home care ([Aline](https://alineops.com/)).
- **Pricing:** Not publicly disclosed.
- **Core features:** Aline CRM ("system of recommendation powered by AI" — flagged: specific AI mechanism unverified), Marketing Automation, Contact Center, Aline Care (care planning), eMAR, Grove Menus, Aline Intelligence (executive dashboards), leasing, billing, payments, accounting, quality, BI ([Aline](https://alineops.com/)).
- **Integrations:** 100+ partners.
- **Strengths:** Most complete all-in-one stack aimed at the segment; 2023 merger consolidated three previously-competing products.
- **Weaknesses:** Post-merger integration pains reflect in reviews — "custom build everything... customer support is terrible... in constant conflict with other web servers," clunky navigation, limited adaptability ([Capterra Aline reviews](https://www.capterra.com/p/174910/Aline/reviews/)). Enterprise-only sales motion. No voice-first capture; no family low-tech web surface.
- **Bridges care ↔ placement?** Within Aline's own suite, yes. Family-accessible? No.

### 12. ECP Lead Cloud / ECP CRM
- **Target customer:** 8,000+ assisted living, long-term care, and IDD communities across all 50 states — broadly distributed, including smaller operators. ECP is the closest analog to a "mid-market" vendor in this list ([ECP](https://www.ecp123.com/)).
- **Pricing:** Not publicly disclosed; custom per community ([Capterra ECP CRM](https://www.capterra.com/p/218918/Leads-CRM/)).
- **Core features:** ECP CRM (lead capture, pipeline, tour scheduling, marketing campaigns, retention prediction), ECP Move-Ins (admission workflow, e-sign, family document submission), ECP Clinical (EHR), ECP eMAR, ECP Billing ([ECP all-in-one](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense)).
- **Integrations:** Native across own modules; external APIs documented ([ECP APIs blog](https://www.ecp123.com/blog/apis-in-senior-living-the-key-to-smarter-more-connected-care)).
- **Strengths:** **The only vendor in this matrix that credibly operationalizes the move-in → care-record handoff inside one product.** ECP Move-Ins "simplifies the admission process by managing every step from initial inquiry to move-in day... seamless integration with ECP Clinical allows resident data to transfer automatically, eliminating duplicate entry" ([ECP blog](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense)). 50-state compliance footprint.
- **Weaknesses:** Licensed-facility product. No family-facing low-tech surface, no voice capture, no AI research agent, no defensibility story tailored to non-medical professional companions, no consumer-grade pricing or sign-up. The bridge exists but it is operator-to-operator, not family-to-facility.
- **Bridges care ↔ placement?** **Closest "yes" in the market — and still not what OnePoint is.** See Bridge Gap section.

### 13. Roobrik
- **Target customer:** Senior living communities running top-of-funnel lead qualification via decision-support surveys. 200+ provider partners ([Roobrik](https://roobrik.com/)). Also offered as part of Aline's stack ([Aline Roobrik](https://alineops.com/senior-living/sales-software/roobrik-solutions/)).
- **Pricing:** "Simple per-community pricing"; claim of 50% savings vs multi-vendor stacks — specific dollars not published ([Roobrik](https://roobrik.com/)).
- **Core features:** Decision-support surveys (care/cognitive, finances, readiness, barriers), 20+ data points per lead, Roobrik Chat, Roobrik Afford financial survey, motivational-interviewing framing ([Roobrik Surveys](https://roobrik.com/senior-living-surveys/), [Roobrik Afford](https://roobrik.com/afford-senior-living-survey/)).
- **Integrations:** Aline-native; exports to partner CRMs.
- **Strengths:** Thoughtful prospect assessment methodology (motivational interviewing is a real clinical framework, not vaporware); useful Afford calculator.
- **Weaknesses:** Top-of-funnel only. Not a CRM, not a care log, not a system of record. Complementary to CRMs, not a replacement.
- **Bridges care ↔ placement?** No — pre-placement only.

### 14. A Place for Mom (as product)
- **Target customer:** Families searching for senior care options; paid by the 20,000+ facility network ([A Place for Mom — Wikipedia](https://en.wikipedia.org/wiki/A_Place_for_Mom)).
- **Pricing:** Free to families. Facilities pay a commission equal to roughly **first month's rent and care** per move-in ([Vizologi APFM](https://vizologi.com/business-strategy-canvas/a-place-for-mom-business-model-canvas/)); reported average commission of ~$3,500 in Washington state with ~$650 to the advisor ([ElderLawAnswers](https://www.elderlawanswers.com/elder-care-referral-services-attracting-increased-scrutiny-9119)).
- **Core features:** Advisor-matching call, curated facility list, tour booking.
- **Integrations:** None for the facility side beyond lead push.
- **Strengths:** Dominant brand awareness; ~40% of U.S. senior-living searches funnel through it.
- **Weaknesses:** **$6M class-action settlement under the Telephone Consumer Protection Act** for robocalling 56,000 consumers without proper written consent ([McKnight's](https://www.mcknightsseniorliving.com/news/a-place-for-mom-agrees-to-settle-lawsuit-for-6-million/), [Dallas Elder Lawyer](https://dallaselderlawyer.com/maybe-you-dont-have-to-read-the-small-print-a-place-for-mom-pays-6-million-due-to-class-action-lawsuit-for-violation-of-telephone-consumer-protection-act/)). **Senate Special Committee on Aging investigation** for steering families to facilities with "documented safety and regulatory violations" ([NBC News](https://www.nbcnews.com/news/us-news/senate-announces-probe-place-for-mom-referral-service-rcna157282), [Senator Casey release](https://www.casey.senate.gov/news/releases/casey-demands-major-assisted-living-facility-referral-service-a-place-for-mom-address-concerns-about-deceptive-marketing-practices)). Only recommends paying facilities ([SeniorSite review](https://seniorsite.org/resource/a-place-for-mom-reviews-the-good-bad-pricing-details-you-need-to-know/)). Nearly 40% of referred families reportedly pay ~$1,000/month over budget ([Washington Post](https://www.washingtonpost.com/business/2024/05/16/place-for-mom-assisted-living-referral/)).
- **Bridges care ↔ placement?** No. It is pure top-of-funnel referral; once a resident moves in, A Place for Mom's data role ends.

### 15. Caring.com
- **Target customer:** Families searching senior care; facilities and home care agencies paying for leads ([Caring.com partners](https://partners.caring.com/)).
- **Pricing:** Pay-per-lead model (bid-priced) for home care agencies; listing subscription fees for senior housing; free to consumers ([Caring.com on Wikipedia](https://en.wikipedia.org/wiki/Caring.com)).
- **Core features:** Directory, 100k+ consumer reviews, editorial content, advisor-assisted referral ([Caring.com](https://www.caring.com/about/news-room/top-ten-senior-living-providers/)).
- **Integrations:** Lead push to partner CRMs.
- **Strengths:** Review-driven SEO moat — listings with 16+ reviews get ~3x more leads, 4x more tours, 4x more move-ins per their own partner data ([Caring.com partners](https://partners.caring.com/get-leads-caring-com/)). Partners with 8 of top 10 senior living operators.
- **Weaknesses:** Pure marketplace; no record of care after placement. Pay-per-lead forces agencies to buy leads that don't convert ([HCMP blog](https://www.homecaremarketing.com/home-care-lead-generation/home-care-lead-providers/)).
- **Bridges care ↔ placement?** No.

### 16. SeniorAdvisor.com
- **Target customer:** Families researching senior care; one of largest review databases in the space ([SeniorAdvisor](https://www.senioradvisor.com/)). Owned by A Place for Mom family of brands.
- **Pricing:** Facility partners pay only upon move-in ([SeniorAdvisor about](https://www.senioradvisor.com/about/about-us)); free claim-your-listing for providers.
- **Core features:** Facility directory with pricing, photos, amenities; curated and verified reviews; advisor match-making.
- **Integrations:** Shares lead flow with A Place for Mom network.
- **Strengths:** Curated review verification (100% human-read); 4.3-star average across assisted living; free listing tier.
- **Weaknesses:** Inherits A Place for Mom criticisms; directory-only, no post-placement product.
- **Bridges care ↔ placement?** No.

---

## Feature Comparison Matrix

Legend: ✓ = yes, ~ = partial / marketing claim / limited, ✗ = no / not applicable, ? = unverified.

| Feature | CareZone* | CaringBridge | Lotsa | Ianacare | Cariloop | CircleOf | CareTree | Enquire | Yardi | Sherpa | Aline | ECP | Roobrik | A Place for Mom | Caring.com | SeniorAdvisor | **OnePoint** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Voice-first capture | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ (call recording) | ~ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Low-tech family web (shareable link, no install) | ✗ | ✓ | ~ | ✗ | ✗ | ✗ | ~ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ (consumer-side) | ✓ | ✓ | **✓** |
| Stream-of-consciousness / dictation tolerant | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ~ | ✗ | ✗ | ✗ | ✗ | **✓** |
| AI medical research agent (cited journals) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~? | ✗ | ✗ | ✗ | ✗ | **✓** |
| Wearables / biometrics ingest (Oura, patches) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| iMessage / SMS historical backfill | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Medication tracking | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ (eMAR) | ✗ | ✓ (eMAR) | ✓ (eMAR) | ✗ | ✗ | ✗ | **✓** |
| Placement pipeline / CRM | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (top-funnel) | ~ (marketplace) | ~ (marketplace) | ~ (marketplace) | **✓** |
| Facility profile / public-facing facility page | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | **✓** |
| Voice-captured prospect intake | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ (call rec) | ~ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Move-in → care-log handoff (same record) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✗ | ~ | **✓** (claimed) | ✗ | ✗ | ✗ | ✗ | **✓** |
| HIPAA-compliant records link (external EHR ingest) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Legal-grade audit export (timestamped, attributed) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ (sales audit) | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Per-caregiver attribution on log entries | ✗ | ✓ (post author) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Self-hostable deployment | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Video family check-in (LifeKit-equivalent) | ✗ | ✗ | ✗ | ✗ | ~ (coach call) | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Spreadsheet on-ramp (mirror existing sheet) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Pricing transparent on website | ✓ (free) | ✓ (free) | ✓ (free) | ~ | ✗ | ✓ (free) | ✗ | ✗ | ✗ | ~ ($525/mo) | ✗ | ✗ | ~ | ~ | ✗ | ~ | TBD |
| Owner-operator / single-facility sales motion | n/a | n/a | n/a | n/a | n/a | n/a | ~ | ✗ | ✗ | ✗ | ✗ | ~ | ✗ | n/a | n/a | n/a | **✓** |

*CareZone effectively defunct as a coordination product.

---

## Pricing Landscape

| Vendor | Pricing model | Starting price | Enterprise tier | Source |
|---|---|---|---|---|
| CareZone (legacy) | Free | — | — | Acquired/discontinued ([Tech-enhanced Life](https://www.techenhancedlife.com/reviews/carezone-medication-app)) |
| CaringBridge | Donation-supported nonprofit | Free | Free | [CaringBridge](https://www.caringbridge.org/) |
| Lotsa Helping Hands | Free (B2B2C sponsorships) | Free | Sponsored by disease foundations | [Lotsa](https://lotsahelpinghands.com/) |
| Ianacare | Freemium → employer-sponsored | Free | Employer PMPM (not disclosed) | [Ianacare support](https://support.ianacare.com/hc/en-us/articles/35224600644621) |
| Cariloop | B2B to employers | Not disclosed | Enterprise PEPM | [Cariloop](https://cariloop.com/employers) |
| CircleOf | Freemium + marketplace | Free | — | [CircleOf](https://circleof.com/) |
| CareTree | B2B to ALCP practices | Not disclosed | Per-client seat | [CareTree](https://www.caretree.me/families) |
| Enquire (Aline) | Enterprise quote | Not disclosed | Per-community | [Capterra](https://www.capterra.com/p/174910/Aline/) |
| Yardi Senior Living Suite | Enterprise quote | Not disclosed | Per-unit / module | [Capterra Yardi](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/) |
| Sherpa CRM | Per community per month | **~$525/mo starting** | Higher tiers not disclosed | [SoftwareSuggest](https://www.softwaresuggest.com/sherpa-crm) |
| Aline (company) | Enterprise quote | Not disclosed | Multi-module bundle | [Aline](https://alineops.com/) |
| ECP (CRM + EHR + eMAR + Move-Ins) | Per-community custom | Not disclosed | All-in-one bundle | [Capterra ECP](https://www.capterra.com/p/90493/ECP/) |
| Roobrik | "Simple per-community" | Not disclosed; ~50% cheaper than multi-vendor stacks (vendor claim) | Per-community | [Roobrik](https://roobrik.com/) |
| A Place for Mom | **Commission — ~first month's rent + care per move-in** | $0 to family | ~$3,500 avg commission (WA) | [Vizologi](https://vizologi.com/business-strategy-canvas/a-place-for-mom-business-model-canvas/), [ElderLawAnswers](https://www.elderlawanswers.com/elder-care-referral-services-attracting-increased-scrutiny-9119) |
| Caring.com | Pay-per-lead (home care) + subscription (housing) | Bid-priced | Variable | [Caring.com partners](https://partners.caring.com/) |
| SeniorAdvisor.com | Commission on move-in | $0 to claim listing | Per move-in | [SeniorAdvisor](https://www.senioradvisor.com/about/about-us) |

**Pricing pattern:** The family side is free-or-employer-paid; the facility side is either enterprise-quote opaque or commission-per-move-in. There is no established price point for a product that serves *both* sides simultaneously. OnePoint has pricing freedom here — plausible anchors are the disclosed Sherpa $525/mo per-facility line ([SoftwareSuggest](https://www.softwaresuggest.com/sherpa-crm)) and the A Place for Mom ~first-month-rent commission ([Vizologi](https://vizologi.com/business-strategy-canvas/a-place-for-mom-business-model-canvas/)).

---

## The Bridge Gap

**The thesis:** OnePoint's wedge is that nobody connects care logging with the placement pipeline *for the same team, in the same record, with a family-accessible surface*. This section tests that thesis against evidence.

**Claim 1: The consumer caregiver segment has no placement pipeline.** Verified. CaringBridge, Lotsa Helping Hands, Ianacare, CircleOf, CareTree, Cariloop — none of them ship a placement CRM, facility profile, tour scheduling, or occupancy dashboard. Their product universe ends at the threshold of a licensed facility. Ianacare Navigators and Cariloop Coaches refer out verbally; that is a human referral, not a pipeline of record ([Ianacare](https://ianacare.com/), [Cariloop coaching](https://cariloop.com/solutions/caregiver-support-platform/coaching)).

**Claim 2: The placement CRM segment has no family-facing care log.** Verified. Enquire, Sherpa, Aline, Yardi, ECP, Roobrik are all sold to the operator. Their "care" surface is an eMAR (medication pass) and a care-planning chart — regulatory artifacts, not a family journal. No voice-first capture, no low-tech-sister shareable link, no AI research cited to peer-reviewed literature. Yardi's own eMAR has documented 11-minute-per-resident load times ([Capterra Yardi reviews](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/reviews/)) — this is a compliance surface, not a living record.

**Claim 3: The lead marketplaces are not bridges.** Verified. A Place for Mom, Caring.com, SeniorAdvisor.com all end their data role at the move-in. They have no care record, no post-placement product. A Place for Mom's own $6M TCPA settlement and Senate investigation demonstrate that their incentives are at odds with ongoing family trust ([McKnight's](https://www.mcknightsseniorliving.com/news/a-place-for-mom-agrees-to-settle-lawsuit-for-6-million/), [NBC News](https://www.nbcnews.com/news/us-news/senate-announces-probe-place-for-mom-referral-service-rcna157282)).

**Claim 4: ECP is the one credible edge case, and it still isn't OnePoint.** ECP explicitly advertises "all-in-one" with Move-Ins → Clinical → eMAR → Billing in one database ([ECP blog](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense)). Resident data transfers automatically from the admission workflow into the clinical record. Families can e-sign and submit documents remotely. **This is the single strongest competitive threat to OnePoint's bridge positioning and must be engaged directly.** However:

- ECP is licensed-facility software. It assumes a nurse, an eMAR workflow, a facility administrator. Ali Ann's non-medical companion team does not fit the buyer profile.
- ECP has no voice-first capture. Logs are typed.
- ECP has no AI research agent against peer-reviewed literature.
- ECP has no low-tech-sister web surface. Family access is a formal e-sign / document portal, not a shareable journal link.
- ECP has no historical iMessage backfill, no Oura integration, no self-host option.
- ECP's "bridge" runs operator → operator. OnePoint's bridge runs **family → facility and back**, such that a prospective resident's family intake data becomes the care record once they move in, and the same care record is visible to both the sisters coordinating outside and the facility staff inside.

**The actual bridge OnePoint ships that nobody else ships:**
1. A **voice-captured prospect intake** (Ali Ann records a family phone call) becomes a structured prospect record.
2. The same record moves through a kanban pipeline with audit-trail discipline.
3. On move-in day, that record **is** the initial care log — no re-entry.
4. The same shareable-link family surface that worked for the placement family *continues to work* as the ongoing care journal.
5. The AI research agent treats the care log as an input and returns cited literature — which no CRM does, period.
6. The legal-grade export spans prospect → resident → discharge as a single attributed, timestamped timeline.

No competitor in this matrix ships points 1, 2, 3, 5, and 6 together. ECP comes closest on point 3 alone. **The wedge holds.**

---

## Research Notes & Caveats

- **"AI" claims flagged as unverified:** Aline's "system of recommendation powered by AI," Sherpa's "Prospect Opportunity Score," and ECP's predictive retention module are all marketed as AI but the specific mechanism (model, training data, validation) is not publicly documented. Treat as marketing until proven.
- **Sherpa $525/mo starting price** comes from a third-party software-listings site ([SoftwareSuggest](https://www.softwaresuggest.com/sherpa-crm)) rather than Sherpa's own site, where pricing is gated. Directionally useful anchor but not first-party confirmed.
- **CareZone** is the only vendor in this list that is effectively defunct as originally branded. The Medisafe relaunch is a different product.
- **Aline merger (2023)** means Enquire, Glennis, and Sherpa reviews dated pre-2023 may not reflect current product; post-2023 Capterra reviews indicate integration pains persist.
- **A Place for Mom** is legally and reputationally wounded ([Senator Casey release](https://www.casey.senate.gov/news/releases/casey-demands-major-assisted-living-facility-referral-service-a-place-for-mom-address-concerns-about-deceptive-marketing-practices), [Washington Post](https://www.washingtonpost.com/business/2024/05/16/place-for-mom-assisted-living-referral/)) — this is a market opening for a trustworthy placement alternative, not just a competitive note.
- **Family caregiver segment is free.** OnePoint's pricing conversation cannot anchor to this segment without a facility-side revenue engine. The placement pipeline is what makes OnePoint commercially viable *and* what makes it defensible against consumer caregiver apps that can't monetize.

---

## Sources (consolidated)

### Care coordination segment
- CareZone: [Tech-enhanced Life review](https://www.techenhancedlife.com/reviews/carezone-medication-app), [Medisafe CareZone App Store](https://apps.apple.com/us/app/medisafe-carezone-pillmemo/id6499107849), [CB Insights](https://www.cbinsights.com/company/carezone)
- CaringBridge: [Homepage](https://www.caringbridge.org/), [Support](https://support.caringbridge.org/), [Resources](https://www.caringbridge.org/resources/what-is-caringbridge), [GoFundMe partnership](https://www.gofundme.com/partners/caringbridge), [ComplaintsBoard](https://www.complaintsboard.com/caringbridge-b183042), [Sitejabber](https://www.sitejabber.com/reviews/caringbridge.org)
- Lotsa Helping Hands: [How it works](https://lotsahelpinghands.com/how-it-works), [Caregiver subsite](https://caregiver.lotsahelpinghands.com/how/), [Google Play listing](https://play.google.com/store/apps/details?id=com.lotsahelpinghands.android.lotsa)
- Ianacare: [Homepage](https://ianacare.com/), [Employers](https://ianacare.com/employers/), [Koch partnership](https://ianacare.com/koch/), [HPE partnership](https://ianacare.com/hpe/), [Support — features](https://support.ianacare.com/hc/en-us/articles/30555221162509), [Support — access levels](https://support.ianacare.com/hc/en-us/articles/35224600644621)
- Cariloop: [Homepage](https://cariloop.com), [Employers](https://cariloop.com/employers), [Coaching](https://cariloop.com/solutions/caregiver-support-platform/coaching), [Benefitfocus listing](https://www.benefitfocus.com/solutions/catalog/cariloop/caregiver-support-platform), [MSU HR FAQ](https://hr.msu.edu/benefits/caregiving/cariloop-faqs.html)
- CircleOf: [Homepage](https://circleof.com/), [About the app](https://circleof.com/app/), [App Store](https://apps.apple.com/us/app/circleof-by-myways-io/id1298712207)
- CareTree: [Families](https://www.caretree.me/families), [Communication](https://web.caretree.me/communication), [Family portal](https://caretree.me/family-portal), [CareScout review roundup](https://www.carescout.com/resources/the-best-apps-for-caregivers-7-tools-to-make-caregiving-easier)

### Placement CRM / senior living ops segment
- Enquire → Aline: [Capterra Aline / Enquire](https://www.capterra.com/p/174910/Aline/), [Capterra reviews](https://www.capterra.com/p/174910/Aline/reviews/), [Capterra Yardi vs Enquire](https://www.capterra.com/assisted-living-software/compare/174910-164514/EnquireCRM-vs-Yardi-Senior-Living-Suite), [Senior Housing News merger coverage](https://seniorhousingnews.com/2023/05/04/senior-living-tech-company-formed-by-merger-of-glennis-enquire-sherpa-rebrands-as-aline/), [BusinessWire rebrand](https://www.businesswire.com/news/home/20230504005190/en/Enquire-Glennis-Solutions-and-Sherpa-CRM-rebrand-as-Aline)
- Yardi Senior Living Suite: [Market page](https://www.yardi.com/market/senior-living/), [Voyager Senior Housing](https://www.yardi.com/product/voyager-senior-housing/), [Blog — new functionality](https://www.yardi.com/blog/news/senior-living/explore-new-functionality-yardi-senior-living-suite/38133.html), [Capterra Yardi Senior Living Suite](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/), [Capterra Yardi reviews](https://www.capterra.com/p/164514/Yardi-Senior-Living-Suite/reviews/), [G2 Yardi Senior Living Suite](https://www.g2.com/products/yardi-senior-living-suite/reviews)
- Sherpa CRM: [Homepage](https://sherpacrm.com/pricing/), [Methodology](https://sherpacrm.com/solutions/crm/), [SoftwareSuggest Sherpa pricing](https://www.softwaresuggest.com/sherpa-crm)
- Aline: [Homepage](https://alineops.com/), [About / mission](https://alineops.com/about-us/), [Billing software](https://alineops.com/senior-living/billing-software/), [Roobrik module](https://alineops.com/senior-living/sales-software/roobrik-solutions/), [G2 Aline reviews](https://www.g2.com/products/aline-aline/reviews)
- ECP: [Homepage](https://www.ecp123.com/), [All-in-one blog](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense), [APIs blog](https://www.ecp123.com/blog/apis-in-senior-living-the-key-to-smarter-more-connected-care), [CRM page](https://www.ecp123.com/crm), [Capterra ECP Leads/CRM](https://www.capterra.com/p/218918/Leads-CRM/), [Capterra ECP](https://www.capterra.com/p/90493/ECP/)
- Roobrik: [Homepage](https://roobrik.com/), [Surveys](https://roobrik.com/senior-living-surveys/), [Chat](https://roobrik.com/senior-living-chat/), [Afford](https://roobrik.com/afford-senior-living-survey/), [Sales enablement](https://www.roobrik.com/enable-sales-teams/)

### Lead marketplaces (adjacent)
- A Place for Mom: [Wikipedia](https://en.wikipedia.org/wiki/A_Place_for_Mom), [Vizologi business model](https://vizologi.com/business-strategy-canvas/a-place-for-mom-business-model-canvas/), [CanvasBusinessModel](https://canvasbusinessmodel.com/blogs/how-it-works/a-place-for-mom), [ElderLawAnswers scrutiny](https://www.elderlawanswers.com/elder-care-referral-services-attracting-increased-scrutiny-9119), [SeniorSite review](https://seniorsite.org/resource/a-place-for-mom-reviews-the-good-bad-pricing-details-you-need-to-know/), [McKnight's $6M settlement](https://www.mcknightsseniorliving.com/news/a-place-for-mom-agrees-to-settle-lawsuit-for-6-million/), [Dallas Elder Lawyer TCPA settlement](https://dallaselderlawyer.com/maybe-you-dont-have-to-read-the-small-print-a-place-for-mom-pays-6-million-due-to-class-action-lawsuit-for-violation-of-telephone-consumer-protection-act/), [NBC News Senate probe](https://www.nbcnews.com/news/us-news/senate-announces-probe-place-for-mom-referral-service-rcna157282), [Senator Casey statement](https://www.casey.senate.gov/news/releases/casey-demands-major-assisted-living-facility-referral-service-a-place-for-mom-address-concerns-about-deceptive-marketing-practices), [Washington Post](https://www.washingtonpost.com/business/2024/05/16/place-for-mom-assisted-living-referral/)
- Caring.com: [Wikipedia](https://en.wikipedia.org/wiki/Caring.com), [Partners — get leads](https://partners.caring.com/get-leads-caring-com/), [Top 10 operators](https://www.caring.com/about/news-room/top-ten-senior-living-providers/), [HCMP home care lead providers](https://www.homecaremarketing.com/home-care-lead-generation/home-care-lead-providers/)
- SeniorAdvisor.com: [Homepage](https://www.senioradvisor.com/), [About](https://www.senioradvisor.com/about/about-us), [News room](https://www.senioradvisor.com/about/news)

### Segment / gap corroboration
- ECP all-in-one: [ECP blog](https://www.ecp123.com/blog/what-is-an-all-in-one-senior-living-platform-and-when-does-it-make-sense)
- Integrated senior living workflow patterns: [WelcomeHome CRM](https://www.welcomehomesoftware.com/senior-living-crm), [HousingTree placement](https://www.housingtree.com/)

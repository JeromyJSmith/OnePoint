# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.7"]
# ///
"""
Build OnePoint.html — a self-contained, CSS-only-tabs, mobile-first HTML page
for Ali Ann to read on her iPhone. Zero JavaScript. StyleSeed Stripe skin.

Usage:  uv run build_html.py
"""

import re
from pathlib import Path

import markdown

BASE = Path("/Users/ojeromyo/Desktop/OnePoint")
OUTPUT = BASE / "OnePoint.html"

md_converter = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "attr_list", "md_in_html"],
    output_format="html",
)


def md_to_html(text: str) -> str:
    md_converter.reset()
    return md_converter.convert(text)


# ═══════════════════════════════════════════════════════════════════════
# TAB CONTENT GENERATORS
# Each function returns an HTML string ready to drop into a panel div.
# ═══════════════════════════════════════════════════════════════════════


def tab_conversations() -> str:
    """Tab 1 — The Conversations"""
    files = [
        ("Call with Ali Ann", BASE / "Call with Ali Ann.transcript.txt"),
        ("Call with Ali Ann (Part 2)", BASE / "Call with Ali Ann 2.transcript.txt"),
        ("Call with Ali Ann (Clinical Session)", BASE / "Call with AlyAnn.transcript.txt"),
    ]
    parts = [
        '<div class="intro">'
        "<p>These are the conversations that started OnePoint. Three phone calls "
        "between Ali Ann and Jero, talking through what Ali Ann actually needs to "
        "take care of Connie and coordinate her sisters. Raw, real, and unpolished "
        "-- because the best products start with honest conversations.</p>"
        "</div>"
    ]
    for title, path in files:
        raw = path.read_text(encoding="utf-8")
        # Strip the "# Verbatim transcript" header and source line
        lines = raw.strip().split("\n")
        cleaned = []
        for line in lines:
            if line.startswith("# Verbatim") or line.startswith("source:"):
                continue
            cleaned.append(line.strip())
        text = "\n".join(cleaned).strip()

        # Format as conversation — add paragraph breaks for readability
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        formatted = ""
        for p in paragraphs:
            # Try to identify speakers based on context
            formatted += f"<p>{_escape(p)}</p>\n"

        parts.append(f'<h2>{title}</h2>\n<div class="conversation">{formatted}</div>')
    return "\n".join(parts)


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tab_what_we_heard() -> str:
    """Tab 2 — What We Heard. Generated narrative from transcripts."""
    return """
<div class="intro">
<p>Before we wrote a single line of code, we listened. Here is the story those conversations told us.</p>
</div>

<h2>Meet Ali Ann</h2>

<p>Ali Ann is a caregiver. Not the hospital kind with scrubs and a badge -- the real-life kind. She runs a small caregiving practice, working overnight shifts, driving between clients, coordinating schedules, and keeping people safe when the rest of the world is asleep.</p>

<p>Right now she is juggling two care situations at once. First, there is Connie -- a woman who has lived with dementia for twenty years, now also dealing with suspected Parkinson's progression. Connie recently spent a month at sea level, then returned home to Lake of the Pines at higher elevation. Within a week of coming back, she was in the emergency room. Her blood pressure went haywire. She became less verbal, more confused, weaker on her feet. The family had no way to see the pattern forming until it was already an emergency.</p>

<p>Then there is Ali Ann's own father, who she recently relocated. He has Parkinson's too, with dementia-adjacent changes. Moving him was a massive undertaking, and Ali Ann cannot lose sight of his needs while building something new.</p>

<h2>The Team</h2>

<p>Ali Ann coordinates care with her sisters. The challenge is that they all live in different places and use technology very differently. One sister is deeply skeptical of modern tech -- she is still worried about 5G, let alone AI. She does not use smartphone apps. Another sister, in Kansas, does not even have an iPhone. The rest are comfortable with Google Sheets and Docs, but nobody has found a system that works for everyone.</p>

<p>Right now, the whole team coordinates through group text messages. When something happens with Connie, someone sends a text. Important details get buried. Nobody can search the thread. If something goes wrong and they need to produce records, all they have is a messy text chain that no attorney would consider reliable.</p>

<h2>What Ali Ann Needs</h2>

<p>In every conversation, the same themes kept coming up:</p>

<p><strong>Voice first.</strong> Ali Ann works with her hands. She cannot stop helping Connie walk to the bathroom to type a note into an app. She needs to hit record, talk about what happened, and have the system figure out the rest.</p>

<p><strong>Everyone included.</strong> If the tech-skeptical sister cannot see the daily log by clicking a simple link in a text message -- no app install, no account creation, no passwords -- then the tool has failed. The whole point is that everyone stays in the loop.</p>

<p><strong>Something that actually helps medically.</strong> When Connie came back from sea level and her symptoms changed, nobody on the team could tell whether this was the elevation, the Parkinson's progressing, or something else entirely. Ali Ann wants the system to look things up -- to check the medical research and come back with what the literature actually says about the symptoms they are observing.</p>

<p><strong>Legal protection.</strong> Ali Ann is currently dealing with a situation where someone threatened to sue her. Her defense? The logs she kept. She knows firsthand that timestamped, attributed records are not just nice to have -- they are what protect you when things go sideways.</p>

<p><strong>A way to fill the Longmont facility.</strong> Ali Ann is associated with an assisted-living facility in Longmont, Colorado, and she needs to place a qualified tenant. This is not a side project -- it is a real business need. She needs a way to capture prospective residents, assess whether they are a good fit, coordinate with their families, and manage the process from first call through move-in day.</p>

<h2>The Gap</h2>

<p>We looked at everything on the market. Free caregiver apps like CaringBridge and Lotsa Helping Hands are fine for sharing updates with friends, but they have no medical intelligence, no legal protection, and they still make you create an account. Enterprise systems like Yardi and Aline cost hundreds of dollars a month, take six weeks to set up, and are designed for chains of fifty communities -- not one person running one facility. Referral services like A Place for Mom are under federal investigation for selling families' information to the highest bidder.</p>

<p>Nothing exists that does what Ali Ann needs: a single place to log care by voice, share it with every sister regardless of tech comfort, get medical insights from real research, protect yourself legally, and fill one assisted-living facility -- all in one product, all from the same record.</p>

<p>That is what OnePoint is being built to do.</p>
"""


def tab_big_picture() -> str:
    """Tab 3 — The Big Picture. Generated from 50_onepoint_strategy.md."""
    return """
<div class="intro">
<p>Here is the short version of what OnePoint is and why it matters.</p>
</div>

<h2>What OnePoint Is</h2>

<p>OnePoint is a voice-first care coordination platform built for people like Ali Ann -- non-medical caregivers who take care of aging loved ones without a hospital, without an electronic medical record system, and right now, without any product designed for them. It is the shared brain for small caregiver teams: one place to log, one place to hand off shifts, one place to see what is actually happening to the person you love.</p>

<h2>Why It Matters</h2>

<p>There are roughly 53 million unpaid family caregivers in the United States. The overwhelming majority coordinate by group text. Critical observations live in text threads nobody can search. Health trends are invisible until an emergency room visit. Low-tech family members are silently locked out of the loop. And when something goes wrong -- when a family member gets adversarial, when a legal question comes up -- there is no defensible record.</p>

<p>OnePoint changes that by bridging two things nobody else connects: <strong>care logging</strong> (the day-to-day record of what is happening with someone) and <strong>tenant placement</strong> (the process of finding and moving someone into an assisted-living facility). When a prospective resident moves into Ali Ann's Longmont facility, their record does not start over. Everything captured during the placement process -- the intake call, the tour notes, the family questions -- becomes the opening chapter of their care log. Zero re-entry, one record, from first phone call to daily shift notes.</p>

<h2>Who It Is For</h2>

<p><strong>Ali Ann and caregivers like her</strong> -- non-medical professional companions running small practices, coordinating care across family members with different devices and different comfort levels with technology.</p>

<p><strong>Ali Ann's sisters</strong> -- family members who need to stay in the loop, especially the ones who will not download an app or create an account. They get a simple link, they click it, they see today's log. That is it.</p>

<p><strong>Small facility operators</strong> -- owner-operators of one or two assisted-living facilities who cannot afford the enterprise software designed for fifty-building chains, and who do not want to pay A Place for Mom thousands of dollars per referral.</p>

<h2>What Makes It Different</h2>

<p><strong>Voice first.</strong> Hit record, talk about your shift, hang up. Your voice note becomes a timestamped log entry, a timesheet row, and a trigger for the AI research agent -- all from one 90-second recording.</p>

<p><strong>Everyone included.</strong> The sister on an old phone clicks a link from a text message and sees the log. No app. No account. No password.</p>

<p><strong>Medical intelligence.</strong> When you log something unusual, the system checks peer-reviewed medical journals and comes back with what the research actually says. Not a diagnosis -- a research summary you can bring to the doctor.</p>

<p><strong>Legal protection.</strong> Every log entry is immutably timestamped and attributed. On demand, you can produce a complete care record as a PDF in under sixty seconds. When someone threatens to sue, your logs are what protect you.</p>

<p><strong>You own your data.</strong> OnePoint can be self-hosted. If we ever disappear, your records do not disappear with us. Your information is never sold. Ever.</p>

<p>The whole system runs for about six dollars and fifty cents per month per person you are caring for. That is less than a single referral commission, less than one month of the cheapest enterprise CRM, and it does more than both combined.</p>
"""


def tab_features() -> str:
    """Tab 4 — What You'll Get. Rewritten from PRD functional requirements."""
    return """
<div class="intro">
<p>Here is what OnePoint actually does, in plain language. No jargon, no feature codes -- just what it does for you.</p>
</div>

<h2>Voice Logging</h2>

<p><strong>Talk, Don't Type</strong> -- Open OnePoint, tap record, and just talk about your shift. Your voice note becomes a timestamped log entry visible to your whole team within seconds. You can talk while you are still helping someone walk to the bathroom -- no need to stop what you are doing.</p>

<p><strong>Stream of Consciousness Welcome</strong> -- You do not need to speak in perfect sentences. Say "she walked to the bathroom and then she said her back hurt and I gave her the blue one" and the system will figure out the structure. Talk naturally. The system handles the rest.</p>

<p><strong>One Recording, Two Outputs</strong> -- Every voice note automatically produces both a care log entry AND a timesheet row. One recording, two artifacts. No double entry.</p>

<p><strong>Show and Tell</strong> -- Point your phone camera at a pill bottle, a blood pressure reading, or a rash. The system sees what you see and adds it to the record alongside your voice note.</p>

<h2>Family Access</h2>

<p><strong>Click the Link, See the Log</strong> -- Your sisters get a link via text message. They click it, pick their name, and see today's care log. No app to install. No account to create. No password to remember. Works on any phone, any browser, any age of device.</p>

<p><strong>Everyone Sees Who's On Duty</strong> -- The dashboard shows who is currently working, the latest log entries, any alerts, and what the AI research agent has found. Everyone stays in the same loop.</p>

<p><strong>Family Video Calls Built In</strong> -- A private family video check-in lives inside OnePoint, so the call and the care log are in the same place.</p>

<p><strong>Weekly Digests</strong> -- Every Sunday, each family member gets a summary of the week tailored to their preferences. One sister might want the clinical details; another might want "Mom had a good week with one concern." The system writes both.</p>

<h2>Medical Insights</h2>

<p><strong>Automatic Research</strong> -- Every time you log something, an AI research agent checks peer-reviewed medical journals for relevant findings. If you mention confusion plus blood pressure changes, it will look up what the literature says about that combination -- and come back with actual citations.</p>

<p><strong>Trend Detection</strong> -- Over time, the system watches for patterns. If blood pressure is trending down in the evenings over ten days and coincides with weaker gait reports, it connects the dots and flags it for you -- with a note saying "bring this to the doctor."</p>

<p><strong>Never a Diagnosis</strong> -- The system informs. It never diagnoses. Every finding is framed so you can bring it to a licensed professional. It is research support, not medical advice.</p>

<h2>Tenant Placement</h2>

<p><strong>Capture Prospects by Voice</strong> -- When you are on the phone with a prospective resident's family, hit "capture prospect" and keep talking. The system transcribes the call and extracts all the intake details -- name, diagnoses, mobility, urgency, who the decision-maker is. Missing info gets flagged for follow-up.</p>

<p><strong>See Who Fits</strong> -- Every prospect is automatically scored against your facility's capabilities. Green means strong fit. Yellow means worth a conversation. Red means it is not the right place -- and the system drafts a compassionate response suggesting better options.</p>

<p><strong>Track the Pipeline</strong> -- See every prospect moving through stages: New Lead, Qualified, Tour Scheduled, Application, Move-In Scheduled, Resident. Every stage change is timestamped, just like the care logs.</p>

<p><strong>Share Your Facility</strong> -- A mobile-friendly facility page with a shareable link and QR code. Hand it to a prospect's family in one motion. No login required for them to view it.</p>

<p><strong>Move-In Day is Seamless</strong> -- When someone goes from prospect to resident, their information carries over automatically. The intake notes, the family contacts, the tour conversations -- all of it becomes the opening chapter of their care log. No re-entering data. No starting over.</p>

<h2>Legal Protection</h2>

<p><strong>Every Entry is Permanent</strong> -- Every log entry is immutably timestamped, attributed to a specific team member, and locked into a tamper-proof chain. Nobody can alter the record after the fact.</p>

<p><strong>Export on Demand</strong> -- Need to produce every log entry from the last 90 days? One tap, and you have a complete, chronological, attributed care record as a PDF in under sixty seconds. If someone threatens legal action, your logs are ready.</p>

<p><strong>Backfill Your History</strong> -- Import old text messages about care into the OnePoint timeline. The timestamps are preserved. Years of care history locked in iMessage become part of your searchable, exportable record -- with everyone's explicit permission first.</p>

<h2>Works for Everyone</h2>

<p><strong>Start with the Spreadsheet</strong> -- If your team already uses a shared spreadsheet, keep using it. OnePoint mirrors it and reads the changes. Over time, the center of gravity moves to OnePoint naturally. Nobody is ever forced to stop using what they are comfortable with.</p>

<p><strong>Works Offline</strong> -- Recording works even without cell service. Your voice note saves locally and syncs when you get back online. Caregivers work in homes, cars, and rural areas -- the tool has to work everywhere.</p>

<p><strong>Wearable Data</strong> -- Connect an Oura Ring or similar wearable, and the biometric data -- heart rate, sleep, activity -- shows up on the same timeline as your voice logs. Subjective observations and objective data side by side.</p>
"""


def tab_market() -> str:
    """Tab 5 — The Market. Simplified from 20_competitor_matrix.md."""
    return """
<div class="intro">
<p>We looked at every product in this space. Here is what is out there and why none of it fits what Ali Ann needs.</p>
</div>

<h2>The Free Caregiver Apps</h2>

<p>Products like CaringBridge, Lotsa Helping Hands, Ianacare, and CircleOf are free or employer-sponsored. They are great for sharing updates with friends and family during a health crisis -- a journal post here, a meal-train signup there. But they have no voice capture, no medical research, no legal-grade record keeping, and most of them still force you to create an account before you can see anything. They are designed for sharing, not for coordinating professional care. And because they are free, they cannot invest in the features their users actually need.</p>

<h2>The Enterprise Software</h2>

<p>On the other end sit products like Aline, Yardi, and Sherpa CRM -- enterprise systems designed for chains of ten, fifty, or a hundred senior living communities. They cost hundreds of dollars a month per community, take weeks to set up, and assume you have a licensed clinical staff, a dedicated facility administrator, and an IT department. One reviewer described the experience: "It will quickly teach your clients why they need a different product." Yardi's medication system takes an average of eleven minutes per person just to pass meds because of how slow and click-heavy it is. These tools were not built for someone running one facility.</p>

<h2>The Referral Marketplaces</h2>

<p>A Place for Mom is the biggest name in senior living referrals. Families think it is a free service to help them find care. In reality, facilities pay roughly one month's rent per move-in as a commission -- often around $3,500. A Place for Mom recently paid a $6 million settlement for robocalling consumers without proper consent. The U.S. Senate launched an investigation into the company for steering families to facilities with documented safety violations. One reviewer wrote: "My mother died two years ago and I still cannot get them to stop contacting me."</p>

<h2>Where OnePoint Fits</h2>

<p>The market splits cleanly into two camps that do not talk to each other: consumer apps that know families but have no placement pipeline, and enterprise software that knows facilities but has no family-facing surface. Lead marketplaces sit in between, profiting from the gap rather than closing it.</p>

<p>OnePoint is the bridge. It is a care log that is also a placement CRM, where the same record serves the family at home and the facility on move-in day. It costs less than a single referral commission from A Place for Mom. It works for the sister on an old phone. And it is built for one facility, not fifty.</p>

<h2>Pricing in This World</h2>

<p>The family-caregiver side of the market is almost entirely free -- which means those products cannot invest in serious features. The facility side is enterprise-priced and opaque: most vendors do not even list their prices. The one disclosed number we found was Sherpa CRM at about $525 per month per community, and that is the starting tier. A Place for Mom charges the equivalent of one month's rent per move-in, typically $3,000-$4,000. OnePoint plans to land at $49 per month per care recipient for the family side, and $499 per month for a single-facility placement CRM -- less than Sherpa, less than one referral commission, and it does both.</p>
"""


def tab_reviews() -> str:
    """Tab 6 — What Users Say. Simplified from 21_review_intelligence.md."""
    return """
<div class="intro">
<p>We read hundreds of reviews of caregiver tools and senior living software. Here is what the people who use them every day are actually saying.</p>
</div>

<h2>"I Spent My Whole Shift Clicking"</h2>

<p>The number-one complaint from nurses and caregivers using clinical software is how long it takes to document anything. One nurse wrote about PointClickCare: <em>"charting is very time consuming because of the lag time and the cumbersome and convoluted features... having to point and click over and over while waiting each time for the program to catch up."</em> Travel nurses report spending two or more hours per shift just clicking through the system.</p>

<p><strong>What OnePoint does instead:</strong> You hit record, talk for 90 seconds, and hang up. The system does the structuring. You never see a form.</p>

<h2>"The System Ate My Work"</h2>

<p>Across multiple products -- AlayaCare, PointClickCare, WellSky, CaringBridge -- users report losing data when the app crashes, the network drops, or they accidentally navigate away. One user described the experience: <em>"The system loses data and often wastes time because it loses internet connections. Offline mode is described as a nightmare."</em></p>

<p><strong>What OnePoint does instead:</strong> Voice capture saves locally first and syncs when the network comes back. Your recording never disappears, even in a dead zone.</p>

<h2>"They Bombard Overwhelmed Families"</h2>

<p>A Place for Mom reviews are devastating. One family member wrote: <em>"They will bombard already overwhelmed families with dozens of unvetted sales calls to make their money through referral fees."</em> Another: <em>"My mother died two years ago and I still cannot get them to stop contacting me."</em> The company has faced a $6 million settlement and a Senate investigation.</p>

<p><strong>What OnePoint does instead:</strong> One family, one facility, no lead resale. Your information is never sold. You will never be contacted after you say stop.</p>

<h2>"My Low-Tech Relatives Are Locked Out"</h2>

<p>Every caregiver app assumes you have a modern phone, an account, and a password. CaringBridge users complain about <em>"forcing users to sign up before showing something of value."</em> Lotsa Helping Hands users report: <em>"This app is a disaster! Constantly makes you log in although that depends if the app even opens."</em> On an AgingCare forum, when someone asked for an app that four family members (one far away) could use to share caregiving responsibilities, the community's answer was: "just use WhatsApp or Google Docs." Nobody could name a caregiver app that actually solved it.</p>

<p><strong>What OnePoint does instead:</strong> Click the link. Pick your name. That is it. No app, no account, no password, no install. Works on any phone.</p>

<h2>"It is Built for Giants, Not for Me"</h2>

<p>Small facility operators find themselves paying for enterprise software that was never designed for them. One Aline user wrote: <em>"It's a good entry level CRM for senior living. It will quickly teach your clients why they need a different product."</em> Another industry review noted that these systems are <em>"tailored primarily for larger communities, where smaller facilities might find them too comprehensive."</em></p>

<p><strong>What OnePoint does instead:</strong> Built for one facility from day one. No six-week implementation. No per-community license math. No dedicated account manager required.</p>
"""


def tab_gaps() -> str:
    """Tab 7 — Where We Win. Simplified from 30_gap_analysis.md."""
    return """
<div class="intro">
<p>These are the specific things nobody else does well -- and where OnePoint is different.</p>
</div>

<h2>Voice Capture for People Who Cannot Type Mid-Shift</h2>

<p>Every caregiver tool on the market requires typing. Not one ships working voice-first capture. This matters because caregivers are physically occupied -- they are helping someone stand, they are in a car, they are holding someone's hand. Making them type is not just inconvenient; it means the observations never get recorded at all. Nurses report spending hours clicking through charting systems. OnePoint lets you hit record, talk naturally, and the system handles structure, timestamps, and attribution.</p>

<h2>Including the Sister on the Old Phone</h2>

<p>In every caregiver family, there is at least one person who will not download an app. Ali Ann has a sister who is skeptical of smartphones entirely and another who does not have an iPhone. Every existing product locks these people out by requiring an account, a modern device, or both. OnePoint sends a text message with a link. The sister clicks it, picks her name, and sees the log. No install, no signup, works on any browser. If it does not work on a skeptical relative's old phone, it fails the test.</p>

<h2>A Legal Record That Holds Up</h2>

<p>Consumer caregiver apps have no audit trail. Enterprise systems have one, but it is locked inside clinical software designed for licensed nurses, and even then, users complain it takes forever to export. Ali Ann is currently defending against a threatened lawsuit -- and her logs are what is protecting her. OnePoint produces a timestamped, attributed, tamper-proof record that you can export as a PDF in under sixty seconds. Every entry is immutable from the moment it is created. This is not a nice-to-have feature -- for people like Ali Ann, it is the reason to use the product.</p>

<h2>AI That Actually Helps</h2>

<p>Every enterprise vendor claims to have "AI." None of them can tell you what it does, and none of them cite peer-reviewed medical literature. When Connie came back from sea level and her blood pressure went haywire, nobody on the team could tell whether it was the elevation, the Parkinson's, or something new. OnePoint's research agent checks real medical journals every time you log something and comes back with what the science says -- with actual citations, framed so you can show them to a doctor. Nobody else in this market does this.</p>

<h2>One Record from First Call to Daily Care</h2>

<p>Today, if a family contacts a facility about placing a loved one, that entire intake process lives in one system. Then the person moves in, and their care record starts from scratch in a different system. All the information from the placement process -- the family conversations, the medical history, the tour notes -- has to be re-entered. OnePoint does not have two systems. The prospect record <em>becomes</em> the care log on move-in day. Everything captured during placement is already there. The family who was reading tour notes through a shared link continues reading shift logs through the same link. Only one competitor even partially does this, and they sell to licensed facility chains, not to Ali Ann.</p>
"""


def tab_smart_features() -> str:
    """Tab 8 — The Smart Features. Simplified from 31_ai_advantage.md."""
    return """
<div class="intro">
<p>Here is where AI actually helps instead of just being a buzzword. Every feature below runs automatically -- you do not have to do anything special to trigger them.</p>
</div>

<h2>Voice to Structured Record</h2>

<p>When you hit record and talk for 90 seconds, the AI turns your stream-of-consciousness into a structured care log entry. It pulls out symptoms, medications, vital signs, and timeline information. It creates a timesheet row at the same time. If the AI is not confident about something, it flags it for you to review rather than guessing. If you are offline, the recording saves locally and processes when you reconnect.</p>

<p><em>Cost: about half a cent per recording.</em></p>

<h2>Medical Research Agent</h2>

<p>Every time a new log entry is created, the system searches peer-reviewed medical databases -- covering over 33 million publications. It looks for research relevant to what you just observed, considering the person's full history. For Connie, that means it would cross-reference Parkinson's progression, dementia patterns, blood pressure instability, and elevation changes all at once. Results come back with real citations -- actual paper titles, authors, and journal names -- and are always framed as "here is what the research says; bring this to a licensed professional."</p>

<p><em>Cost: about six dollars per month per person you are caring for. This is the most expensive feature, and it is still less than a single copay.</em></p>

<h2>Placement Fit Scoring</h2>

<p>When a new prospect enters the pipeline, the AI compares their needs against your facility's capabilities. It scores the fit, explains why, and flags anything that needs a conversation. For strong fits, it recommends a tour. For non-fits, it drafts a compassionate response suggesting better options -- because the way you handle a "no" matters as much as the way you handle a "yes."</p>

<p><em>Cost: about five cents per prospect.</em></p>

<h2>Voice Prospect Intake</h2>

<p>When you are on the phone with a prospective resident's family, you can capture the entire call. The AI transcribes it, identifies who said what, and extracts all the intake details: name, diagnoses, mobility, urgency, decision-maker contacts. Missing information gets flagged, and a follow-up email is drafted for you to send with one click.</p>

<p><em>Cost: about eight cents per call.</em></p>

<h2>Trend Detection</h2>

<p>Every night, the system looks across the last 30 days of log entries and any wearable data. It runs statistical checks for drifts -- is blood pressure trending down? Is confusion being mentioned more often? Are sleep patterns changing? When it spots a compound pattern (like blood pressure plus gait changes plus elevation), it writes up what it found and alerts you and the designated family member. Simple patterns are handled by faster, cheaper AI. Complex compound patterns get escalated to the most thorough AI model available.</p>

<p><em>Cost: about 75 cents per month per person.</em></p>

<h2>Weekly Family Digest</h2>

<p>Every Sunday evening, each family member gets a summary of the week. The system writes it in the tone each person prefers -- clinical detail for the medically minded sister, a warm overview for someone who just wants to know Mom is okay. Each summary includes top moments, any concerns flagged by the trend detector, key numbers (medications taken, hours of sleep, blood pressure range), and links back to the specific log entries.</p>

<p><em>Cost: about one dollar per month per family.</em></p>

<h2>Move-In Handoff</h2>

<p>When a prospect becomes a resident, the AI assembles everything captured during the placement process into an opening care record: intake notes, diagnoses, family contacts, compliance documents. It generates a day-one checklist of what is still needed and drafts an initial care plan based on the fit assessment. The care team's AI memory is seeded with this history, so the system already knows the new resident on day one.</p>

<p><em>Cost: about ten cents per move-in.</em></p>

<h2>All Together</h2>

<p>All of this runs for about <strong>$6.50 a month per person you are caring for</strong>. Hosting the system costs about $45 a month total. For comparison, a single Sherpa CRM seat costs $525 a month, and a single A Place for Mom referral commission costs about $3,500.</p>
"""


def tab_how_built() -> str:
    """Tab 9 — How It's Built. Simplified from 40_system_architecture.md."""
    return """
<div class="intro">
<p>OnePoint is built on proven open-source tools, not from scratch. Here are the building blocks in plain English.</p>
</div>

<h2>The Building Blocks</h2>

<p><strong>Medical Records Backbone (Medplum)</strong> -- This is the system of record for every person, every log entry, and every clinical event. It is the same platform used in hospitals, it meets healthcare privacy and security standards, and it is open source. Every write is automatically tracked with who did it, when, and what changed.</p>

<p><strong>Placement Pipeline (Krayin CRM)</strong> -- This handles the prospect-to-resident journey: leads, pipeline stages, tour scheduling, and occupancy tracking. It is an open-source CRM system that we customize with the specific stages and fields Ali Ann's facility needs.</p>

<p><strong>Voice and Video (LiveKit)</strong> -- This powers the voice capture, the vision features (showing a pill bottle to the camera), and family video calls. It is the same technology that runs real-time communication apps used by millions of people.</p>

<p><strong>AI Agents (LangGraph + memory)</strong> -- The research agent, trend detection, and all the smart features run on an open-source agent framework that keeps track of what it has learned about each person over time. The more it learns, the better it gets at spotting patterns and finding relevant research.</p>

<p><strong>Low-Tech Web Pages (HTMX)</strong> -- The pages the tech-skeptical sister sees are built with the simplest possible web technology. No fancy frameworks, no heavy JavaScript, nothing that could break on an old phone. Just fast, simple HTML pages that load instantly.</p>

<p><strong>Legal Export (Gotenberg)</strong> -- When you need to produce a care record for an attorney, this tool converts the timeline into a proper PDF document -- the kind that holds up in legal settings.</p>

<h2>The Move-In Handoff</h2>

<p>This is the most important piece of how OnePoint is built. When someone goes from prospect to resident, their information carries over automatically -- no re-entering data. Here is how it works:</p>

<p>The moment a prospect is marked as "qualified," the system quietly creates a shadow record in the medical backbone. From that point on, everything captured during the placement process -- tour notes, pre-admission documents, family conversations -- is attached to that record. When the prospect stage flips to "resident," it is a single switch: the shadow record becomes an active care record. The family's shared link continues working. The care team sees the full history from the first phone call forward.</p>

<p>No other product in this market does this for a single-facility operator with a family-facing surface.</p>

<h2>What It Costs to Run</h2>

<p>The entire system runs on a single server for about <strong>$45 per month</strong>. That covers the database, the medical records system, the CRM, the voice capture, the AI agents, and the web pages. For comparison, a Yardi license alone costs many times more than that, and it does not include voice capture or AI research.</p>

<p>Every piece of the system is open source. If OnePoint as a company ever went away, someone technical could keep the system running on their own. Your data is never locked into a service you cannot leave.</p>
"""


def tab_plan() -> str:
    """Tab 10 — The Plan. Simplified from 50_onepoint_strategy.md."""
    return """
<div class="intro">
<p>Here is the plan: what gets built, when, and how we will know if it is working.</p>
</div>

<h2>The Elevator Pitch</h2>

<p><em>"OnePoint is for people like Ali Ann -- non-medical companions who take care of someone's aging mom without the hospital, without an EMR, and right now, without any product built for them. She's coordinating her team through group text, she's running two cases at once, and she's being threatened with a lawsuit where the only thing saving her is the logs she barely has time to write. Most caregiver apps make her low-tech sister create an account before she can see anything. Enterprise senior-living software wants $500 a month and a six-week implementation. A Place for Mom is under federal investigation for selling families to the highest bidder. OnePoint is the single place where Ali Ann hits record, talks for 90 seconds, and every sister -- including the one on a flip phone -- sees the log from a text-message link. The same product is a placement CRM for the Longmont assisted-living facility she's trying to fill, and on the day someone moves in, their intake from the prospect phone call is already their care log. Zero re-entry, one record, family-to-facility and back."</em></p>

<h2>Week by Week</h2>

<p><strong>Week 0 (Saturday session):</strong> Jero and Ali Ann sit down together and figure out the details -- who we set up first, which sisters get links, what the Longmont facility profile looks like, and the timeline for the legal situation. This conversation is the foundation for everything that follows.</p>

<p><strong>Week 1:</strong> You can record voice notes and your sisters can see them through a link. The legal audit trail starts from day one -- every entry is timestamped and tamper-proof from the first recording.</p>

<p><strong>Week 2:</strong> The legal export works -- you can produce a PDF of every log in under sixty seconds. The AI research agent starts running against your logs. The Longmont facility gets its public page and the placement pipeline goes live. Prospects can be captured by voice.</p>

<p><strong>Week 3:</strong> The move-in handoff is wired. A prospect who becomes a resident has their record carry over automatically. The research agent is returning cited findings.</p>

<p><strong>Week 4:</strong> The low-tech sister has actually tested the system on her real phone. If it does not work, we fix it before going further. SMS fallback is live for anyone who will not tap a link. The weekly family digest starts sending. The legal export gets a dry run with an attorney.</p>

<p><strong>Week 8:</strong> First real move-in at Longmont, if a prospect is in the pipeline. Wearable integration. Historical text message import. The full system is running.</p>

<h2>How We Will Know It Is Working</h2>

<p>We will know it is working when:</p>

<ul>
<li>Ali Ann records a voice note every shift without being reminded</li>
<li>At least two sisters are checking the web link every week</li>
<li><strong>The group text gets quieter</strong> -- that is the real signal that OnePoint is replacing the scattered coordination</li>
<li>The legal export produces something an attorney accepts</li>
<li>At least one qualified tenant moves into the Longmont facility through OnePoint within 60 days</li>
</ul>

<h2>The Honest Checkpoints</h2>

<p><strong>At 30 days:</strong> If Ali Ann is recording logs regularly and one sister has used the link at least twice, we keep building. If Ali Ann has recorded fewer than five logs in a month, the core assumption is wrong and we need to figure out why.</p>

<p><strong>At 60 days:</strong> If a qualified prospect is moving through the Longmont pipeline and care logging is sticky, we double down. If neither side is getting traction despite direct outreach, we have a hard conversation about what is not working.</p>

<p><strong>At 90 days:</strong> If at least one tenant has moved into Longmont through OnePoint and the care-logging side is active, this is a real product. If the pipeline has no prospects past the first stage after three months, the facility buyer does not exist in the form we modeled.</p>
"""


def tab_questions() -> str:
    """Tab 11 — Your Questions. Generated for Saturday session."""
    return """
<div class="intro">
<p>Before we can start building, we need to figure out a few things together. These are the questions for our Saturday session -- each one shapes what gets built first.</p>
</div>

<h2>1. Who should we set up first -- Connie, your dad, or both?</h2>
<p>The system can handle both from day one, but starting with one person means we can focus on getting it right before expanding. Connie is the more acute case right now -- she just came back from sea level and things are changing fast. But your dad's situation matters too, and you know your own bandwidth best. Which one do you want to pilot with?</p>

<h2>2. Which sisters get links, and how do we reach them?</h2>
<p>We need names, phone numbers or email addresses, and a sense of each person's comfort level with technology. Specifically: is the 5G-skeptical sister willing to tap a link in a text message? If not, we need to set up a different notification path for her from the start.</p>

<h2>3. Can we import your old text messages about Connie's care?</h2>
<p>There is a way to pull care-related text conversations into OnePoint so the timeline does not start from zero -- it starts with the history you already have. We would need your permission for each person whose messages get imported, and we only take the care-related ones. Is that something you are comfortable with?</p>

<h2>4. What does the Longmont facility look like on paper?</h2>
<p>To build the facility's public page and the placement pipeline, we need: the facility name, location, what levels of care it offers, current vacancy count, pricing tiers, specializations (memory care? Parkinson's care?), and any photos. This is the information that goes on the shareable page families will see.</p>

<h2>5. What is the legal situation's timeline?</h2>
<p>You mentioned someone threatening to sue. How urgent is the legal export? If there is a near-term deadline, we make the "produce all your logs as a PDF" feature a week-one priority instead of building up to it. What date range would the export need to cover?</p>

<h2>6. How should we handle prospects who are not a good fit?</h2>
<p>When the system scores a prospect and they are not right for your facility, should it just tell you and let you handle the conversation? Or would it help to have a drafted response you can personalize? (Our recommendation: always show you first, never auto-decline, and draft a compassionate response you can edit.)</p>

<h2>7. What price feels right when you walk into the Longmont owner's office?</h2>
<p>We have numbers in mind -- $49/month per care recipient for the family side, $499/month for the facility side. But you are the one having that conversation. Does that feel right? Would a free trial make it easier to start? A different number entirely? You choose what you can sell.</p>
"""


def tab_next_steps() -> str:
    """Tab 12 — Next Steps. Simplified from research/next_steps.md."""
    return """
<div class="intro">
<p>Here is what happens next, week by week.</p>
</div>

<h2>This Saturday: The Working Session</h2>
<p>Jero and Ali Ann sit down and answer the seven questions from the previous tab. By the end of the evening, we have: a confirmed first care recipient, the sister contact list, the Longmont facility profile, and a plan for the next four weeks. Jero will already have a working prototype at a staging URL before Ali Ann arrives.</p>

<h2>Week 1: Record, Save, Share</h2>
<p>Ali Ann can record a voice note and her sisters can read it through a link. The legal trail starts from the first entry. By the end of the week, Ali Ann has logged at least one real shift.</p>

<h2>Week 2: Export and Placement</h2>
<p>The legal export works -- a full PDF in under sixty seconds. The AI research agent starts returning findings from medical journals. The Longmont facility page goes live with a shareable link. Prospects can be captured by voice.</p>

<h2>Week 3: The Bridge</h2>
<p>The move-in handoff is wired. A prospect becoming a resident gets their record carried over automatically. Research agent findings are showing up on the timeline after log entries.</p>

<h2>Week 4: Real-World Test</h2>
<p>The low-tech sister tests the system on her actual phone. SMS fallback goes live. The weekly digest starts sending. The legal export gets reviewed by an attorney.</p>

<h2>Month 2: Depth</h2>
<p>Wearable data integration. A dashboard with trends over time. The trend detection agent starts watching for patterns. A first tour is scheduled through OnePoint for the Longmont facility. Two sisters are checking the web link weekly.</p>

<h2>Month 3: Proof</h2>
<p>The headline question: has at least one qualified tenant moved into the Longmont facility through OnePoint? If yes, we expand to a second facility. If not, we have an honest conversation about what needs to change. Historical text message import ships. Medical records linking goes live for at least one family.</p>

<h2>Always True</h2>
<ul>
<li>Ali Ann's dad is her first priority. We never schedule anything that forces her to choose between her dad and OnePoint.</li>
<li>Connie is the acute case. Every week without a usable voice log is a week her care is happening on group text.</li>
<li>The legal situation is today, not someday. The export feature is not optional.</li>
<li>Longmont placement is revenue. Every week without a move-in is lost revenue for Ali Ann.</li>
</ul>
"""


def tab_full_research() -> str:
    """Tab 13 — Full Research. Lightly cleaned concatenation of all research docs."""
    research_files = [
        ("Skill Landscape", BASE / "research" / "10_skill_landscape.md"),
        ("OSS Landscape", BASE / "research" / "11_oss_landscape.md"),
        ("Competitor Matrix", BASE / "research" / "20_competitor_matrix.md"),
        ("Review Intelligence", BASE / "research" / "21_review_intelligence.md"),
        ("Gap Analysis", BASE / "research" / "30_gap_analysis.md"),
        ("AI Advantage Design", BASE / "research" / "31_ai_advantage.md"),
        ("System Architecture", BASE / "research" / "40_system_architecture.md"),
        ("Strategy", BASE / "research" / "50_onepoint_strategy.md"),
    ]
    parts = [
        '<div class="intro">'
        "<p>This tab has the full technical research -- competitor deep dives, "
        "open-source analysis, architecture details, AI feature designs, and "
        "strategy. It is dense on purpose. This is Jero's reference material.</p>"
        "</div>"
    ]
    for title, path in research_files:
        raw = path.read_text(encoding="utf-8")
        html = md_to_html(raw)
        # Wrap tables
        html = re.sub(
            r"(<table.*?</table>)",
            r'<div class="table-wrap">\1</div>',
            html,
            flags=re.DOTALL,
        )
        parts.append(f'<h2 class="research-section">{_escape(title)}</h2>\n{html}\n<hr>')
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE HTML
# ═══════════════════════════════════════════════════════════════════════

TABS = [
    ("Conversations", "p0", tab_conversations),
    ("Heard", "p1", tab_what_we_heard),
    ("Big Picture", "p2", tab_big_picture),
    ("Features", "p3", tab_features),
    ("Market", "p4", tab_market),
    ("Reviews", "p5", tab_reviews),
    ("Wins", "p6", tab_gaps),
    ("Smart", "p7", tab_smart_features),
    ("Built", "p8", tab_how_built),
    ("Plan", "p9", tab_plan),
    ("Questions", "p10", tab_questions),
    ("Next", "p11", tab_next_steps),
    ("Research", "p12", tab_full_research),
]

# Build radio inputs, labels, and panels
radio_inputs = []
tab_labels = []
panel_divs = []

for i, (label, cls, gen_fn) in enumerate(TABS):
    rid = f"r{i}"
    checked = " checked" if i == 0 else ""
    radio_inputs.append(
        f'<input type="radio" name="tabs" id="{rid}" class="tab-radio"{checked}>'
    )
    tab_labels.append(f'<label for="{rid}">{label}</label>')
    content = gen_fn()
    panel_divs.append(f'<div class="panel {cls}">{content}</div>')

# CSS rules for tab switching (13 tabs: r0-r12)
tab_css_rules = []
for i, (_, cls, _) in enumerate(TABS):
    tab_css_rules.append(
        f'#r{i}:checked ~ .header .tab-bar [for="r{i}"]{{color:var(--brand);font-weight:600;border-bottom-color:var(--brand)}}'
    )
    tab_css_rules.append(f'#r{i}:checked ~ .panels .{cls}{{display:block}}')

tab_css = "\n".join(tab_css_rules)

html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>OnePoint</title>
<style>
/* ── StyleSeed Stripe Skin ──────────── */
:root{{
  --brand:#533afd;
  --bg:#ffffff;
  --fg:#061b31;
  --text-1:#061b31;
  --text-2:#273951;
  --text-3:#64748d;
  --text-4:#9ba8b8;
  --surface:#f6f9fc;
  --border:#e5edf5;
  --card:#ffffff;
  --shadow-card:rgba(50,50,93,0.25) 0px 2px 5px -1px, rgba(0,0,0,0.1) 0px 1px 3px -1px;
  --radius:6px;
}}

*,*::before,*::after{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
body{{
  margin:0;padding:0;
  font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','Segoe UI',system-ui,sans-serif;
  font-size:15px;line-height:1.65;
  color:var(--text-2);background:var(--surface);
  -webkit-font-smoothing:antialiased;
}}

/* ── Tab Radio Mechanism (CSS-only) ─── */
.tab-radio{{position:absolute;opacity:0;width:0;height:0}}
.panel{{display:none}}

{tab_css}

/* ── Header ─────────────────────────── */
.header{{
  background:var(--card);
  padding:20px 16px 0;
  border-bottom:1px solid var(--border);
  position:sticky;top:0;z-index:100;
  box-shadow:var(--shadow-card);
}}
@media(min-width:600px){{
  .header{{padding:20px 24px 0}}
}}
.header h1{{
  margin:0 0 2px;font-size:24px;font-weight:700;
  color:var(--text-1);letter-spacing:-0.02em;
}}
.header .subtitle{{
  margin:0 0 12px;font-size:13px;color:var(--text-3);
  font-weight:400;
}}

/* ── Tab Bar ────────────────────────── */
.tab-bar{{
  display:flex;gap:0;
  overflow-x:auto;overflow-y:hidden;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
  padding-bottom:0;
  margin:0 -16px;
  padding-left:16px;
  padding-right:16px;
}}
@media(min-width:600px){{
  .tab-bar{{margin:0 -24px;padding-left:24px;padding-right:24px}}
}}
.tab-bar::-webkit-scrollbar{{display:none}}
.tab-bar label{{
  flex:0 0 auto;
  font-family:inherit;font-size:13px;
  color:var(--text-3);padding:10px 14px;
  cursor:pointer;white-space:nowrap;
  border-bottom:2px solid transparent;
  min-height:44px;
  display:flex;align-items:center;
  transition:color .15s,border-color .15s;
  font-weight:500;
  -webkit-tap-highlight-color:transparent;
}}
@media(min-width:600px){{
  .tab-bar label{{font-size:14px;padding:12px 16px}}
}}

/* ── Content ────────────────────────── */
.panels{{
  max-width:860px;
  margin:0 auto;
  padding:16px;
}}
@media(min-width:600px){{
  .panels{{padding:24px}}
}}
@media(min-width:1024px){{
  .panels{{padding:32px}}
}}

.panel > .intro,
.panel > h2,
.panel > h3,
.panel > p,
.panel > ul,
.panel > ol,
.panel > blockquote,
.panel > hr,
.panel > .table-wrap,
.panel > .conversation,
.panel > pre,
.panel > div {{
  background:var(--card);
  border-radius:var(--radius);
  box-shadow:var(--shadow-card);
  padding:20px 20px;
  margin:0 0 2px;
}}
@media(min-width:600px){{
  .panel > .intro,
  .panel > h2,
  .panel > h3,
  .panel > p,
  .panel > ul,
  .panel > ol,
  .panel > blockquote,
  .panel > hr,
  .panel > .table-wrap,
  .panel > .conversation,
  .panel > pre,
  .panel > div {{
    padding:24px 28px;
  }}
}}

/* Card wrappers for grouped content */
.panel > .intro{{
  background:linear-gradient(135deg, #f0edff 0%, #f6f9fc 100%);
  border-left:3px solid var(--brand);
  margin-bottom:12px;
}}
.panel > .intro p{{
  margin:0;color:var(--text-2);font-size:15px;
}}

/* ── Typography ─────────────────────── */
.panel h1{{
  font-size:24px;font-weight:700;
  color:var(--text-1);letter-spacing:-0.02em;
  margin:0;padding-top:24px;
}}
.panel h2{{
  font-size:20px;font-weight:700;
  color:var(--text-1);
  border-bottom:2px solid var(--border);
  padding-bottom:8px;
  margin:0;margin-top:16px;
}}
.panel h2:first-child{{margin-top:0}}
.panel h3{{
  font-size:18px;font-weight:700;
  color:var(--text-1);margin:0;margin-top:12px;
}}
.panel h4{{
  font-size:16px;font-weight:600;
  color:var(--text-2);margin:0;margin-top:8px;
}}
.panel p{{
  max-width:72ch;margin:0;
  color:var(--text-2);
}}
.panel p + p{{margin-top:12px;}}
.panel a{{color:var(--brand);text-decoration:none;font-weight:500}}
.panel a:hover{{text-decoration:underline}}
.panel strong{{color:var(--text-1)}}
.panel em{{color:var(--text-3);font-style:italic}}

/* ── Lists ──────────────────────────── */
.panel ul,.panel ol{{
  max-width:72ch;padding-left:1.4em;margin:0;
  color:var(--text-2);
}}
.panel li{{margin:6px 0}}
.panel li>ul,.panel li>ol{{margin:4px 0}}

/* ── Code ───────────────────────────── */
.panel code{{
  font-family:'SF Mono','Menlo','Consolas',monospace;
  font-size:0.85em;
  background:var(--surface);
  padding:0.15em 0.4em;
  border-radius:3px;
  color:var(--text-1);
}}
.panel pre{{
  background:var(--surface);
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  font-size:13px;line-height:1.5;
  border:1px solid var(--border);
}}
.panel pre code{{
  background:none;padding:0;font-size:inherit;
}}

/* ── Conversation blocks ───────────── */
.conversation{{
  border-left:3px solid var(--brand);
}}
.conversation p{{
  margin:0 0 10px;
  font-size:14px;line-height:1.75;
  color:var(--text-3);
}}

/* ── Blockquotes ────────────────────── */
.panel blockquote{{
  border-left:3px solid var(--brand);
  background:var(--surface);
  color:var(--text-3);
}}
.panel blockquote p{{margin:4px 0}}

/* ── Tables ─────────────────────────── */
.table-wrap{{
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  border:1px solid var(--border);
}}
.panel table{{
  width:100%;
  border-collapse:collapse;
  font-size:13px;
  min-width:500px;
}}
.panel th{{
  background:var(--surface);
  color:var(--text-1);
  font-weight:600;
  text-align:left;
  padding:8px 12px;
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:0.05em;
  border-bottom:2px solid var(--border);
}}
.panel td{{
  padding:8px 12px;
  border-bottom:1px solid var(--border);
  color:var(--text-2);
}}
.panel tr:hover td{{background:var(--surface)}}

/* ── Horizontal rules ───────────────── */
.panel hr{{
  border:none;
  border-top:1px solid var(--border);
  margin:0;
  padding:0;
  box-shadow:none;
  background:transparent;
}}

/* ── Images ──────────────────────────── */
.panel img{{max-width:100%;height:auto;border-radius:var(--radius)}}

/* ── Research tab special ────────────── */
.research-section{{
  color:var(--brand) !important;
  font-size:22px !important;
  margin-top:24px !important;
}}
</style>
</head>
<body>

{"".join(radio_inputs)}

<div class="header">
  <h1>OnePoint</h1>
  <p class="subtitle">The shared brain for caregiver teams</p>
  <nav class="tab-bar">
    {"".join(tab_labels)}
  </nav>
</div>

<div class="panels">
  {"".join(panel_divs)}
</div>

</body>
</html>"""

OUTPUT.write_text(html_output, encoding="utf-8")
size_kb = OUTPUT.stat().st_size / 1024
print(f"Built {OUTPUT} ({size_kb:.0f} KB)")
"""
Now run it and open the result.
"""

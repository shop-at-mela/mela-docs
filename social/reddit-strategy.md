# Reddit Strategy

**Created:** 2026-07-29
**Status:** Active — expands the 4-line Reddit stub in `accounts.md` into a real playbook.
**Cadence/status canonical in `accounts.md` → Reddit section** (this doc doesn't restate counts, it explains the how and why).

---

## Why Reddit — two distinct goals, don't conflate them

1. **Community trust.** Diaspora shoppers already ask "where do I buy X" in these communities. Genuine, helpful participation builds trust that no paid channel can buy — and is a real discovery surface for people actively looking, not scrolling.
2. **AEO co-mention value.** Reddit threads are heavily surfaced by Gemini/Google AI Overviews and Perplexity — this is the concrete "how" behind the Reddit line item in `aeo-next-steps.md` §1 (third-party co-mentions). A genuine, upvoted Reddit answer mentioning Mela is exactly the kind of independent-domain citation that audit was asking for. Don't run this as a separate initiative from that one — it's the same goal, executed here.

These two goals pull in the same direction (be genuinely useful) so they don't create conflicting incentives, but keep them distinct in your head: goal 1 succeeds even with zero SEO benefit, goal 2 is a bonus, not the reason to post.

---

## Non-negotiable ground rules

- **One real account, no sockpuppets.** No fake accounts posing as customers, no vote manipulation, no coordinated multi-account posting. Founder/team voice only — this is stated as "Automation: None — founder/team only" in `accounts.md` for a reason.
- **Always disclose affiliation the moment you're promoting Mela.** "I'm building Mela" — same honesty-first framing as `outreach-templates.md`. Reddit's culture punishes hidden marketing far harder than open honesty; if someone asks "are you the founder / is this an ad," the answer is always yes.
- **Respect each subreddit's self-promotion rules.** Most communities enforce roughly a 90/10 ratio — nine genuine contributions for every one promotional mention. Read each subreddit's rules/wiki before posting. A removed post or a ban does more damage than not posting at all.
- **No crossposting the same content verbatim across multiple subreddits at once.** Moderators actively detect and remove this pattern; it reads as spam even when the intent isn't.
- **No @ tagging brands yet** — same guardrail as the social captions per [[feedback_no_brand_tagging_yet]]: no affiliate agreement in place, accounts still in warmup.
- **Never claim unverified craft/certification details** — same `verify: true` discipline as `education-topics.yaml`. A wrong claim in a Reddit comment is public and permanent in a way a deleted Instagram post isn't.

---

## Three modes of participation (in order of how much this playbook should lean on them)

### 1. Comment-only engagement (default — most of the 3-5/week)
Answer real questions genuinely. Only mention Mela when it's a direct, honest answer to what was actually asked — not a drive-by plug on an unrelated thread. This is the lowest-risk, highest-trust mode and should be most of the weekly activity.

### 2. Original informational posts (occasional, higher risk/reward)
Value-first posts — a guide, not a product plug (e.g., "how India-to-US shipping timelines actually work," "US vs India sizing for footwear"). **Reuse the same seed topics as the content hub in `aeo-next-steps.md` §2 / `education-topics.yaml`** rather than building a third content pipeline from scratch. Post as a genuine community contribution; a Mela mention belongs in a reply if someone asks follow-up questions, not baked into the original post.

### 3. AMA (later-stage, not a Month-1 tactic)
Highest visibility, needs real prep and enough shipped proof to withstand scrutiny (founder story, real brand roster, real shipping experience to point to). Don't attempt this during cold-start warmup — revisit once the Month-1 checklist's "wife becomes the face" milestone (per `cold-start-checklist.md`) is closer, so there's a real story to tell.

---

## Target subreddits

**Already active (per `accounts.md`):**
- r/IndiaMoms
- r/AsianParenting
- r/SustainableFashion

**Candidates to evaluate — verify existence and current self-promotion rules before posting, don't assume either is still accurate:**
- r/AsianBeauty — large, active skincare community; fits Vilvah/Bipha Ayurveda-style brands.
- r/femalefashionadvice — general fashion advice community; fits sustainable/ethical fashion angle (Suta, Chidiyaa, The Alternate).
- r/BuyItForLife — values durability/craft over trend; strong fit for artisan/heritage-craft positioning (juttis, handloom).
- r/IndianSkincareAddicts — Indian-specific skincare community, if still active at time of use.

Subreddit rules and even existence change — confirm both before the first post in any candidate community, not just once at strategy-writing time.

---

## Cadence & tracking

- Cadence stays as defined in `accounts.md`: **3-5 quality interactions/week**, human-posted only. Reddit has no Blotato automation support — this is manual by design, not a gap to eventually close.
- Track in `metrics-log.md` alongside Instagram/Pinterest rows. Reddit has no "saves," so track: upvotes, reply engagement, and outbound clicks via UTM (per `category-routing.yaml` → `tracking`) if a link is dropped in a comment.
- Review as part of the existing Sunday review in `cold-start-checklist.md` — don't stand up a second review ritual just for Reddit.

---

## Guardrails specific to Reddit's backlash risk

- Don't reply to every competitor mention with a Mela plug — even done sincerely, a pattern of "user mentions X, founder-adjacent account shows up with Y" reads as astroturfing.
- If a post or comment gets downvoted/removed, don't repost elsewhere to route around it — read why it was removed (usually a self-promo ratio or rule violation) and adjust, rather than treating moderation as noise to dodge.
- Silence is an acceptable outcome. Not every thread needs a Mela mention — most weeks, most of the 3-5 interactions should have no promotional content at all.

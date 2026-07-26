# Positioning Copy Pack (P0.5)

Created 2026‑07‑26 for `storefront-validation-readiness-prd.md` P0.5. Exact strings for every positioning surface, mapped to the file and key where each lives. This is the copy source of truth for the execution session.

**Resolved positioning (2026‑07‑26):** Mela is Indian brand discovery for everyone. The brands are proven at home in India and already export globally. Family and baby are categories among equals, not the promise.

**Rules applied:** curator voice, never retailer (legal constraint: curated directory, no affiliate language). No dash characters in copy. Every claim verifiable: no GOTS, organic, or "10,000+ parents" claims survive unless we can prove them. The honest wedge stays: discover here, buy on each brand's own store.

***

## 1. Homepage hero (`web-client/src/translations/en.json`)

| Key | Current | New |
|-----|---------|-----|
| `SectionMelaHero.heroHeadline` (line 639) | Discover Quality Indian Brands for Your Family | **Discover India's Most Loved Brands** |
| `SectionMelaHero.heroSubheadline` (640) | The best brands from India rarely reach US shelves. Discover them here — then buy on each brand's own store. | **The brands India already loves rarely reach US shelves. We vet the ones with real export experience, then point you to each brand's own store.** |
| `SectionMelaHero.trustModelCallout` (641) | You browse here — then shop directly on each brand's own store. | **You browse here. You buy on each brand's own store.** |
| `SectionMelaHero.breadthQualitative` (643) | Handpicked Indian brands across baby, fashion & beauty | **Handpicked Indian brands across fashion, home, beauty, and kids** |

Keep as is: `shopNow` ("Explore Brands"), `categoryPillsLabel`, `breadthCount`.

Headline alternates, if testing later: "The Best of India's Brands, All in One Place" · "Indian Brands Worth Discovering". Do not A/B now; positioning was decided, not tested (PRD §9).

**Drift fix in the same pass:** `HeroSection.js` lines 232 and 238 carry stale `defaultMessage` values ("Independent Indian Brands, Curated for Your Family" and the dashed subhead). Update both defaults to match the new en.json strings so the fallback never resurrects old positioning.

## 2. Homepage meta (`web-client/src/containers/MelaHomePage/MelaHomePage.js`)

| Line | Current | New |
|------|---------|-----|
| 20 `pageTitle` | Sustainable Indian Design for Families \| Baby, Fashion & More \| Mela | **Discover India's Most Loved Brands \| Fashion, Home, Beauty & Kids \| Mela** |
| 23 `pageDescription` | Mela curates the best Indian baby, fashion, and home brands for families in the US. Discover quality-verified brands, explore products, and shop directly on brand stores. | **Mela is a curated home for proven Indian brands with real export experience. Explore fashion, home, beauty, jewelry, and kids, then buy directly on each brand's own store. Ships to all 50 states.** |

## 3. Brands directory (`en.json`)

| Key | Current | New |
|-----|---------|-----|
| `BrandsPage.title` (1693) | Indian Organic Baby Brands \| {brandCount}+ GOTS Certified Brands \| Mela | **All Brands \| {brandCount}+ Hand Vetted Indian Brands \| Mela** |
| `BrandsPage.description` (1694) | Discover {brandCount}+ verified Indian organic baby brands. Shop GOTS certified clothing, natural care products, and handcrafted toys. Trusted by 10,000+ parents. | **Browse {brandCount}+ hand vetted Indian brands across fashion, home, beauty, jewelry, and kids. Every brand ships to the US and accepts US cards. You buy directly on each brand's own store.** |
| `BrandsPage.heroTitle` (1695) | Discover India's Most Trusted Brands | keep unchanged |

Dropped claims: "Organic", "GOTS Certified" (only some brands qualify; per brand certifications stay on brand cards where they are true), "Trusted by 10,000+ parents" (unverifiable).

## 4. Category pages (`en.json` + `CategoryPage.js`)

| Location | Current | New |
|----------|---------|-----|
| `CategoryPage.title` (1684) | {categoryName} — Authentic Indian Baby Products \| {marketplaceName} | **{categoryName} \| Curated Indian Brands \| {marketplaceName}** |
| `CategoryPage.description` (1685) | Discover authentic Indian {categoryName} products for your baby. Curated brands with GOTS certified, organic, and handcrafted options — trusted by diaspora families. | **Discover {categoryName} from India's most loved independent brands. Curated by Mela, shipped to the US, purchased directly on each brand's own store.** |
| `CategoryPage.js` line 181, all categories intro | Discover authentic Indian baby products, handloom fashion, artisanal home décor, Ayurvedic beauty, gourmet foods, and handcrafted jewelry — curated from independent Indian brands shipping to the US. | **Discover authentic Indian baby products, handloom fashion, artisanal home décor, Ayurvedic beauty, gourmet foods, and handcrafted jewelry, curated from independent Indian brands shipping to the US.** |

The title fix here also closes the P0.4 bug ("Fashion — Authentic Indian Baby Products").

## 5. Adjacent cleanups spotted while auditing (log under P0.2/P0.4)

1. `MelaHomePage.heroHeadline` (en.json 602) and `heroSubheadline` (603) are legacy baby era strings, apparently superseded by `SectionMelaHero.*`. Verify unused, then delete so they cannot resurface.
2. `MelaHomePage.favoritesSubtitle` (618) contains a dash and an unverifiable tone ("Loved by families worldwide - see what our customers can't stop raving about"). Suggested: **"Bestsellers our shoppers keep coming back to"**.
3. `MelaHomePage.categorySubtitle` (608) contains a dash: "Explore curated Indian design across categories — for every age, occasion, and style" → **"Explore curated Indian design across categories, for every age, occasion, and style"**.

## Why these words (rationale, for the record)

1. **"Most Loved"** carries the proven at home claim in two words: these brands won India first. "Quality" (current) is empty; every store claims it.
2. **"Real export experience"** is the second half of the positioning decision and doubles as a trust signal: these brands already know how to ship abroad.
3. **The wedge stays in every description**: "buy directly on each brand's own store" is both honest and legally required framing. Short declaratives replace the em dash construction.
4. **Family language removed from the promise, kept in the assortment**: "kids" appears as one category among fashion, home, beauty, jewelry.

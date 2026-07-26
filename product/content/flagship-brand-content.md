# Flagship Brand Content Pack (P1.1)

Created 2026‑07‑26 for `storefront-validation-readiness-prd.md` P1.1a. This is the copy source of truth for the five flagship brand pages. Each brand's content is structured into the hero band slots defined in the approved mobile mockup.

**Voice rules applied here and for all future brand copy:**
* Confident curator, never retailer. We introduce the brand; we do not sell for it.
* Name the craft, the place, and the maker. Specificity is the trust signal.
* Short sentences. No dash characters in copy. Restructure with commas, colons, or new sentences instead.
* The hero summary is two short paragraphs at most. The full story lives in the About and Story tab.

**Slot mapping:** tagline → first sentence of `bio` · hero summary → opening of `bio` story · craft chip → `brand_craft` in `shopify_brands.py` (live; payload only, no label, tightened 2026‑07‑26) · meta → `brand_hq` · full story → About tab from `bio`.

***

## 1. Fizzy Goblet · fashion (footwear) · `fizzy-goblet`

**Meta:** Mumbai, India · global.fizzygoblet.com

**Tagline:** Handcrafted juttis, kolhapuris, and mules for the modern wardrobe.

**Hero summary:**
Fizzy Goblet brings India's traditional handcrafted footwear into contemporary fashion. Every pair of juttis, kolhapuris, and embroidered mules is stitched by hand by skilled karigars using techniques passed down through generations.

Modern silhouettes and playful embellishments make this craft you can wear anywhere, from a wedding to weekend brunch.

**Craft chip (payload only; UI adds any label):** juttis stitched by hand in Mumbai

**About and Story tab:**
Fizzy Goblet started in Mumbai with a simple idea: the jutti, one of India's oldest shoe forms, deserved a place in the modern wardrobe. The label works with skilled karigars who stitch each pair by hand, carrying forward techniques that have moved through families for generations. Silhouettes are cut for today: mules, wedges, sliders, and flats alongside the classic jutti shape. Embroidery, sequins, and unexpected materials give each collection its playful signature. The result is footwear that honors its origin and refuses to sit still in it.

***

## 2. House of Chikankari · fashion · `house-of-chikankari`

**Meta:** Lucknow, India · houseofchikankari.in

**Tagline:** Authentic Lucknow chikankari, made by the artisans behind the craft.

**Hero summary:**
House of Chikankari works directly with artisans in Lucknow, the city where this centuries old shadow work embroidery was born. Kurtas, sarees, and matching sets are embroidered by hand on fine cotton and georgette.

Real chikankari, at prices that still pay the artisan fairly.

**Craft chip (payload only; UI adds any label):** Lucknow chikankari, embroidered by hand

**About and Story tab:**
Chikankari is Lucknow's gift to Indian textiles: a delicate white on white embroidery tradition that reaches back centuries. House of Chikankari builds its entire label around the artisans who keep that tradition alive, working with them directly in Lucknow rather than through middlemen. Each kurta, saree, and matching set is embroidered by hand on breathable cotton, mulmul, and georgette. The direct relationship keeps prices honest in both directions: fair for the shopper, fair for the maker. What you wear is the real craft, from the city that invented it.

***

## 3. Ankid · baby and kids · `ankid`

**Meta:** India · ankid.in ⚠️ `brand_hq` is missing in `shopify_brands.py`; add city before seeding.

**Tagline:** Block printed ethnic and festive wear for babies and children.

**Hero summary:**
Ankid designs festive wear for India's youngest: bandhgala sets, sharara sets, lehenga cholis, and cotton separates printed by hand with wooden blocks. Pieces are finished by artisans and made to match across siblings and generations.

Playful without losing polish, they turn festivals like Eid and Sankranti into occasions the whole family dresses up for.

**Craft chip (payload only; UI adds any label):** block printed cotton, sized for children

**About and Story tab:**
Ankid makes Indian festive wear that children actually want to wear. The range runs from bandhgala and sharara sets to lehenga cholis and everyday cotton separates, each printed by hand with carved wooden blocks and finished by artisans. Sizing is built for real families: matching pieces across siblings, and often across generations, so festival photos come together without a scramble. Fabrics stay soft and breathable because dressing up should never be a negotiation. For Eid, Sankranti, Diwali, or a cousin's wedding, Ankid makes the occasion feel like one.

***

## 4. Vilvah Store · beauty and wellness · `vilvah-store`

**Meta:** Coimbatore, India · vilvah.com

**Tagline:** Farm fresh skincare made from ingredients grown on the brand's own farm in Tamil Nadu.

**Hero summary:**
Vilvah formulates its skincare around a working farm in Tamil Nadu, from soaps and moisturizers to hair oils and body butters. Goat milk, cold pressed oils, and botanical extracts go in at their freshest, closest to harvest.

No synthetic chemicals. Just ingredients the farm grows, presses, and bottles itself.

**Craft chip (payload only; UI adds any label):** skincare from one farm in Tamil Nadu

**About and Story tab:**
Most skincare brands buy their ingredients. Vilvah grows them. The label runs its own farm in Tamil Nadu, where goat milk, cold pressed oils, and botanical extracts are produced and used at their freshest. Formulations skip synthetic chemicals entirely, relying on the potency of raw ingredients close to harvest. The range covers the everyday essentials: cleansing soaps, moisturizers, hair oils, and body butters, made in small batches. It is skincare with a supply chain you can picture, because it fits inside one farm.

***

## 5. Kaunteya · home and kitchen · `kaunteya`

**Meta:** Delhi, India · kaunteya.in

**Tagline:** Ceramic tableware painted by hand, inspired by Indian manuscript art.

**Hero summary:**
Kaunteya paints its ceramic tableware with motifs drawn from Indian manuscript painting, temple architecture, and folk art. Each plate, bowl, and vase is thrown on the wheel or cast, then painted by trained artisans.

Functional pieces that bring a little cultural memory to the table.

**Craft chip (payload only; UI adds any label):** ceramics painted by hand in Delhi

**About and Story tab:**
Kaunteya treats the dinner table as a canvas for Indian art history. Its ceramic plates, bowls, mugs, and vases carry motifs drawn from manuscript painting, temple architecture, and folk traditions, researched and redrawn for contemporary tableware. Every piece is thrown on the wheel or cast, then painted by trained artisans in Delhi. The collections are fully functional: dishwasher realities and daily use are part of the design brief. Set a Kaunteya table and the art comes to dinner with you.

***

## Execution notes (for the seeding and build session)

1. ✅ Done 2026‑07‑26: copy folded into `shopify_brands.py` for the five flagships, and every active brand (all 19 with user IDs in `product-listing-integration/.env.dev`) now has dash free `brand_tagline` and `brand_story` plus a filled `brand_craft` chip. Inactive brands carry a `brand_craft: ""` placeholder and an ACTIVATION CHECKLIST at the top of the file explains how to fill it.
2. ✅ Done 2026‑07‑26: `brand_craft` is wired end to end. `export_brand_content.py` exports it as `craft`; `seed-brand-profiles.js` pushes it to `publicData.brandCraft`. Frontend read of `brandCraft` is part of the P1.1 build.
3. **Still open. Ankid gap:** `brand_hq` is an empty placeholder in its entry (city unconfirmed). Confirm with the brand or its site, fill it, then rerun the exporter and seeder.
4. **Hero summaries vs bio:** the hero band shows the first two paragraphs of the story. If the split ever needs to differ per brand, promote the hero summary to its own field; for now paragraph order in `brand_story` controls it.
5. All copy above contains no dash characters, per content style rule (see also the voice rules at the top of this document). Verified across all 19 active brands on 2026‑07‑26.

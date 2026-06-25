#!/usr/bin/env python3
"""
Generate the full LIPU RAG knowledge base as markdown files.
Run: python generate_kb.py
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

BASE_DIR = Path(__file__).resolve().parent
UPDATED = "2026-06-25"
DEFAULT_REGIONS = ["bhubaneswar", "cuttack", "puri", "odisha"]

SUBFOLDERS = [
    "faq",
    "catalog",
    "glass",
    "hardware",
    "warranty",
    "installation",
    "odisha-climate",
    "design-inspiration",
    "pricing-guide",
    "service-support",
]


def yaml_frontmatter(meta: dict) -> str:
    """Serialize frontmatter without external dependencies."""
    lines = ["---"]
    for key, val in meta.items():
        if val is None:
            continue
        if isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        elif isinstance(val, int):
            lines.append(f"{key}: {val}")
        elif isinstance(val, list):
            if not val:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in val:
                    lines.append(f"  - {item}")
        elif isinstance(val, str):
            if any(c in val for c in ":{}[]#&*!|>'\"%@`"):
                escaped = val.replace('"', '\\"')
                lines.append(f'{key}: "{escaped}"')
            else:
                lines.append(f"{key}: {val}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def write_doc(folder: str, slug: str, meta: dict, body: str) -> Path:
    meta.setdefault("regions", DEFAULT_REGIONS)
    meta.setdefault("version", 1)
    meta.setdefault("updated", UPDATED)
    meta.setdefault("language", "en")
    meta.setdefault("status", "published")
    meta["category"] = folder
    meta["id"] = f"{folder}/{slug}"

    out_dir = BASE_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug}.md"
    content = yaml_frontmatter(meta) + "\n\n" + body.strip() + "\n"
    path.write_text(content, encoding="utf-8")
    return path


def faq_body(title: str, faqs: list[tuple[str, str]]) -> str:
    parts = [f"# {title}", ""]
    for q, a in faqs:
        parts.append(f"## {q}")
        parts.append("")
        parts.append(a.strip())
        parts.append("")
    return "\n".join(parts)


def section_doc(title: str, sections: dict[str, str]) -> str:
    parts = [f"# {title}", ""]
    for heading, content in sections.items():
        parts.append(f"## {heading}")
        parts.append("")
        parts.append(content.strip())
        parts.append("")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# FAQ data — 38 categories × 6+ Q&As = 228+ questions
# ---------------------------------------------------------------------------

FAQ_CATEGORIES: list[dict] = [
    {
        "slug": "product-selection",
        "title": "UPVC Product Selection Guide",
        "tags": ["selection", "windows", "doors", "guide", "bhubaneswar"],
        "audience": "homeowner",
        "summary": "How to choose the right UPVC window or door system for your Odisha home.",
        "faqs": [
            (
                "Which window is best for a road-facing bedroom in Bhubaneswar?",
                "For road-facing bedrooms near NH-16, Jayadev Vihar, or Old Town lanes, a casement window with inward opening and laminated acoustic double glazing is usually the best choice. Casements seal tighter than sliders when closed, which matters when traffic noise peaks in the morning and evening. Pair it with a multi-point lock and good gaskets — sliders are fine for balconies but often leave a small gap that lets noise through. If the opening is wide, consider a fixed centre panel with casement sashes on either side for ventilation without sacrificing the acoustic seal.",
            ),
            (
                "How do I decide between sliding and casement for my living room?",
                "Sliding suits wide balcony openings where you want an unobstructed view and do not open windows daily for cross-ventilation. Casement works better when the opening is moderate, you face dust or noise, and you want maximum seal when closed. In Bhubaneswar apartments, living rooms opening to sit-outs often use sliding for the main span and a small casement ventilator above the kitchen pass-through. Match the system to how you actually use the space — not just how it looks in a brochure.",
            ),
            (
                "Should I use the same window type throughout my home?",
                "Not necessarily. Bedrooms, bathrooms, kitchens, and balconies have different needs for privacy, ventilation, and noise. A consistent colour and profile series looks cohesive, but mixing sliding on balconies with casement in bedrooms is common and sensible. What you should keep uniform is the glass specification for similar exposures — do not put single glass on a west-facing bedroom and double on an east-facing one without reason.",
            ),
            (
                "What profile thickness should I look for in Odisha?",
                "For residential work in Bhubaneswar and Cuttack, 70 mm multi-chamber profiles are the practical standard for main windows and doors. Lighter 60 mm sections exist for ventilators and small openings but are not ideal for large sliders or coastal installations. Thicker 80 mm systems add cost and are rarely needed unless you are doing very large commercial spans. Ask for chamber count and steel reinforcement specification — thickness alone does not tell the full story.",
            ),
            (
                "How many openings should I replace at once versus in phases?",
                "If budget is tight, prioritize road-facing and west-facing rooms first — they deliver the biggest comfort gain. Phase two can cover remaining bedrooms; phase three balconies and bathrooms. Replacing everything at once gives better fabrication batch pricing and one round of site disruption. Partial replacement works, but ensure the new profiles match the existing colour batch as closely as possible to avoid visible shade differences after a year of UV exposure.",
            ),
            (
                "Does floor level affect window choice in high-rise apartments?",
                "Yes. Upper floors in Bhubaneswar towers face stronger wind and driving rain during cyclones — drainage design and wind-load-rated hardware matter more above the fifth floor. Ground and first floors need stronger security hardware and may benefit from laminated glass even if noise is not the main concern. Mid-floor apartments often balance both: good sealing for monsoon and multi-point locking for security.",
            ),
        ],
    },
    {
        "slug": "upvc-vs-aluminium",
        "title": "UPVC vs Aluminium Windows",
        "tags": ["upvc", "aluminium", "comparison", "materials"],
        "audience": "homeowner",
        "summary": "Honest comparison of UPVC and aluminium for Odisha homes.",
        "faqs": [
            (
                "Is UPVC or aluminium better for coastal Odisha?",
                "For Puri, Konark, and Paradeep coastal belts, quality UPVC with stainless hardware and proper drainage usually outperforms standard aluminium on thermal comfort and salt corrosion resistance at similar price points. Aluminium with thermal break and powder coating can work well but needs disciplined maintenance — hinge and track lubrication, gasket checks after monsoon. Plain non-thermal-break aluminium gets hot to touch, sweats in humid months, and conducts heat into the room. UPVC's multi-chamber design naturally insulates better without extra engineering.",
            ),
            (
                "Which material lasts longer in Bhubaneswar heat?",
                "Both can last 15–25 years if installed correctly. UPVC does not corrode and handles humidity well; the risk is poor-quality profiles that yellow or warp. Aluminium does not warp but can pit if coating fails near the coast. In direct west-facing sun, UPVC with lead-free stabilizers and quality lamination holds colour better than budget aluminium that fades unevenly. Longevity depends more on brand, installation, and hardware than the base material alone.",
            ),
            (
                "Is aluminium stronger for large spans?",
                "Aluminium profiles can achieve slimmer frames on very large commercial spans, but reinforced UPVC handles typical residential openings up to 8–10 ft width without issue. For villa frontage or showroom glazing, engineered aluminium curtain walls may be specified. For standard homes in Bhubaneswar, UPVC reinforced with steel inserts is structurally adequate and easier to seal against monsoon rain.",
            ),
            (
                "Which is easier to maintain?",
                "UPVC needs periodic cleaning and occasional hardware adjustment — no painting. Aluminium may need track cleaning, lubrication, and touch-up of coating chips especially near the coast. Homeowners who want minimal upkeep usually prefer UPVC. Commercial clients sometimes accept aluminium maintenance schedules because of design requirements.",
            ),
            (
                "How do running costs compare over 10 years?",
                "UPVC typically wins on AC bills due to lower U-values, especially with double glazing. Aluminium without thermal break can add noticeable heat gain in Odisha summers. Initial aluminium quotes sometimes look lower on slim profiles, but add thermal break, good glass, and coastal hardware and the gap narrows. Factor energy savings and maintenance when comparing lifecycle cost, not just installation price.",
            ),
            (
                "Can I mix UPVC and aluminium in one project?",
                "You can, but colour matching and sightline alignment require careful planning. Some architects use aluminium for structural facade elements and UPVC for operable windows behind them. For most residential projects, a single material system simplifies warranty and service. Mixing is a design choice, not a performance requirement.",
            ),
        ],
    },
    {
        "slug": "upvc-vs-wooden",
        "title": "UPVC vs Wooden Windows",
        "tags": ["upvc", "wood", "wooden", "comparison", "termite"],
        "audience": "homeowner",
        "summary": "Comparing UPVC and wooden windows for humidity, termites, and Odisha climate.",
        "faqs": [
            (
                "Are wooden windows still viable in humid Odisha?",
                "Teak and sal windows can work in heritage or premium villas if maintained with regular polishing, sealing, and termite treatment — but most homeowners underestimate the upkeep in Bhubaneswar's humidity. Swelling during monsoon and shrinkage in dry months cause sticking and gap opening. UPVC does not absorb moisture and maintains dimensional stability year-round. Wooden windows suit aesthetic-driven projects with budget for carpentry maintenance; UPVC suits practical daily living.",
            ),
            (
                "How does termite risk compare?",
                "Termites are a real concern across Odisha, including in concrete apartments with wooden frames. UPVC is immune to termite damage. Wooden frames need periodic anti-termite treatment and inspection of adjoining wall woodwork. If your home has a history of termite issues, UPVC removes one major failure point entirely.",
            ),
            (
                "Which looks better in traditional Odia home design?",
                "Wood wins on warmth and authenticity for kutcha-era or heritage-style architecture. Modern UPVC comes in wood-grain laminates that mimic teak reasonably well from a distance, but purists notice the difference up close. Some owners use wooden doors internally and UPVC externally for weather-facing openings — a hybrid that preserves character where it matters.",
            ),
            (
                "Is wooden window insulation better than UPVC?",
                "Not inherently. Old wooden windows often have air gaps and single glass. Modern UPVC with double glazing typically outperforms traditional wooden single-glazed setups on heat and noise. Well-made wooden windows with double glazing exist but cost significantly more and still need maintenance. Performance comes from glass and seal quality as much as frame material.",
            ),
            (
                "What about cost over 15 years?",
                "Wooden windows may cost more upfront for good hardwood plus periodic repainting and hardware replacement. UPVC has higher initial cost than cheap wood but lower ongoing expense. In coastal Puri or Cuttack, wooden frames near sea air degrade faster unless you use marine-grade finishes. Total cost of ownership usually favours UPVC for typical middle-class homes.",
            ),
            (
                "Can I replace wooden windows with UPVC without changing wall openings?",
                "Usually yes, if the existing opening size and lintel condition are sound. The site survey measures the reveal and checks for rot in the surrounding frame. Sometimes wooden subframes are removed and UPVC fitted into the same opening with new sealing. Structural changes are rare unless the old frame was undersized or damaged by termites.",
            ),
        ],
    },
    {
        "slug": "sliding-windows",
        "title": "Sliding Window FAQs",
        "tags": ["sliding", "windows", "balcony", "apartment"],
        "audience": "homeowner",
        "summary": "Common questions about UPVC sliding windows for Odisha homes.",
        "faqs": [
            (
                "Why are sliding windows popular in Bhubaneswar apartments?",
                "Sliding windows do not swing inward or outward, which suits compact balconies and rooms with furniture against the wall. They give wide glass area for light and view — important in tower blocks across Patia, Nayapalli, and Khandagiri. When fitted with good rollers and drainage, they handle monsoon rain well. The trade-off is slightly lower acoustic seal than casement when fully closed.",
            ),
            (
                "Do sliding windows leak in heavy rain?",
                "Well-installed sliders with correct slope, drain holes, and gaskets should not leak in normal Odisha monsoon. Leaks usually trace to blocked drainage channels, missing outer sealant, or rollers that prevent the sash from sitting fully closed. After Fani and subsequent cyclones, we see more problems on budget installs that skipped end caps and sill flashing. Maintenance twice a year prevents most issues.",
            ),
            (
                "How smooth should sliding operation feel?",
                "A properly adjusted panel should move with moderate finger pressure without grinding or jumping off track. Heavy resistance often means dirty tracks, worn rollers, or building settlement shifting the frame. In coastal areas, salt buildup on tracks needs cleaning every few months. Replace rollers every 8–12 years depending on use — they are wear items, not defects.",
            ),
            (
                "Can sliding windows be locked securely?",
                "Yes — look for multi-point or at least dual-point locking with anti-lift blocks. Standard single latch locks are weak against forced entry. For ground-floor apartments, add laminated glass and restrict panel lift. Sliding is not less secure than casement if hardware is specified correctly — insecurity usually comes from cheap locks, not the sliding mechanism itself.",
            ),
            (
                "What is the maximum width for one sliding panel?",
                "Residential panels commonly run 3–4 ft wide; beyond that, roller load and user effort increase. Very wide openings use two or three track systems with multiple panels. Your fabricator should confirm steel reinforcement for spans over 6 ft total width. Do not force oversized single panels to save money — they fail early.",
            ),
            (
                "Should I choose two-track or three-track sliding?",
                "Two-track gives one operable panel and one fixed — simpler and better sealed. Three-track allows two operable panels meeting in the centre, opening half the width for ventilation. Three-track has more gasket length and more potential leak paths; use it when ventilation width justifies the complexity. For balconies primarily used for view, two-track is often enough.",
            ),
        ],
    },
    {
        "slug": "casement-windows",
        "title": "Casement Window FAQs",
        "tags": ["casement", "windows", "ventilation", "sealing"],
        "audience": "homeowner",
        "summary": "Questions about casement UPVC windows for bedrooms and kitchens.",
        "faqs": [
            (
                "When should I choose casement over sliding?",
                "Choose casement when maximum seal against noise, dust, and rain matters — typical for bedrooms, study rooms, and road-facing openings. The sash presses against the frame on all sides when locked, unlike sliding panels that slide parallel with a overlap seal. Casement also allows full opening for cleaning the outer glass from inside on upper floors with safe reach. Avoid casement where inward swing hits beds, curtains, or kitchen counters.",
            ),
            (
                "Inward or outward opening casement — which suits Odisha?",
                "Outward opening saves interior space and is common in Europe, but most Indian residential UPVC casements open inward for safety on upper floors and easier hardware maintenance. Inward suits Bhubaneswar apartments where balcony projection limits outward swing. Outward can work on ground-floor villa windows if local wind loads and hinge strength are verified.",
            ),
            (
                "Do casement windows catch more rain when open during monsoon?",
                "Yes — if you leave them open during driving rain, water can enter. Use partial tilt or open only during light rain with adequate overhang. Many homeowners pair casement with a fixed top ventilator or use mesh shutters for monsoon ventilation without full sash opening. This is user behaviour, not a product flaw — sliders have the same issue if left wide open in a storm.",
            ),
            (
                "How many hinges and locking points are needed?",
                "Standard residential casements use two to three hinges and a multi-point lock with at least two locking pins. Larger sashes need four hinges and reinforced frames. Insist on branded hardware — cheap hinges sag after two monsoons and the sash no longer seals. Multi-point locking is non-negotiable for road-facing bedrooms.",
            ),
            (
                "Are casement windows good for cross-ventilation?",
                "Excellent when placed on opposite walls — the open sash acts like a scoop catching breeze. In row-house layouts in Cuttack or duplex stairwells, casement pairs drive natural airflow better than fixed glass. Orient openings to prevailing wind where possible; even light breeze helps during humid pre-monsoon months.",
            ),
            (
                "Can casement windows use mosquito mesh?",
                "Yes — fixed mesh on the outer frame or hinged mesh shutters are common. Integral sliding mesh cassettes work on larger openings. Mesh reduces airflow slightly but is essential in Bhubaneswar evenings when mosquito activity peaks. Specify mesh type during order — retrofitting is possible but costlier.",
            ),
        ],
    },
    {
        "slug": "fixed-windows",
        "title": "Fixed Window FAQs",
        "tags": ["fixed", "picture", "glazing", "non-operable"],
        "audience": "homeowner",
        "summary": "When and how to use fixed UPVC windows in Odisha homes.",
        "faqs": [
            (
                "Why use fixed windows if they do not open?",
                "Fixed panels maximize glass area, eliminate moving-part leaks, and cost less than operable units of the same size. They suit stairwells, highlight areas above doors, and combination windows where casement or sliding sashes flank a fixed centre. You get light and view without compromising wall space for swing or slide paths.",
            ),
            (
                "How do I ventilate a room with only fixed glass?",
                "You should not rely on fixed glass alone in habitable rooms — building bye-laws and comfort both need operable area. Combine fixed panels with adjacent casement vents, top ventilators, or door openings. Designers often use fixed lower panels with operable upper sashes for privacy plus airflow.",
            ),
            (
                "Are fixed windows more energy efficient?",
                "Slightly — no gasket wear at operable junctions and no user error leaving gaps. The bigger factor is glass specification. A fixed panel with single clear glass still performs poorly; fixed with double glazed low-E performs very well on west-facing facades.",
            ),
            (
                "Can fixed windows be cleaned from outside on high floors?",
                "Only if accessible from balcony, lift cradle, or safe external platform. Plan cleaning access during design — many Bhubaneswar towers regret large fixed panels facing the exterior with no reach. Internal removable grill designs or split fixed modules help.",
            ),
            (
                "Do fixed windows weaken cyclone resistance?",
                "Properly glazed and silicone-sealed fixed units often resist wind pressure well because they have no moving parts. Risk increases if glass is underspecified for height and exposure. Use toughened or laminated glass per span and altitude; structural silicone glazing in commercial facades follows engineer specs.",
            ),
            (
                "Fixed plus operable combinations — what ratio works?",
                "A common pattern is 60% fixed centre with 20% casement on each side for wide living room openings. Bedrooms might use one operable casement and one fixed side panel. Balance view, cost, and ventilation — all-fixed facades look modern but need alternate air paths.",
            ),
        ],
    },
    {
        "slug": "french-windows",
        "title": "French Window FAQs",
        "tags": ["french", "doors", "balcony", "opening"],
        "audience": "homeowner",
        "summary": "French window and door systems for terraces and garden access.",
        "faqs": [
            (
                "What is the difference between French windows and French doors?",
                "French windows are floor-to-ceiling or sill-height paired casements opening to balcony or garden, often with a low threshold. French doors serve main entry or room dividers with similar paired-sash look. Both use dual sashes meeting at centre with multi-point locks. In Odisha villas, French windows connect living rooms to lawn areas; apartments use them for balcony access where building rules allow full-height openings.",
            ),
            (
                "Do French windows let more heat in than sliders?",
                "Heat gain depends on glass and orientation, not the French format itself. Large glass area increases total heat load — west-facing French openings need double glazing minimum, ideally with solar control. Thermal break thresholds and bottom seals matter because heat also enters through poorly sealed sills.",
            ),
            (
                "Are French windows safe for homes with children?",
                "Use child-safe locks, restrict opening width, and specify laminated safety glass. Low sill French windows should meet apartment safety norms — grilles or limited opening stays are common requirements from builders in Bhubaneswar. Never leave fully open at height without supervision.",
            ),
            (
                "How do French windows perform in monsoon?",
                "When locked, quality French casements seal well. User error — opening both sashes during squalls — causes water ingress. Outward-opening French designs shed rain better when cracked for ventilation; inward designs need overhang protection. Threshold drainage prevents water pooling at foot level.",
            ),
            (
                "Can mosquito mesh work with French openings?",
                "Side-hinged mesh doors or pleated mesh systems pair well with French windows. Magnetic mesh is a budget option with shorter life. Plan mesh before fabrication — post-install retrofit on paired sashes is awkward and visible.",
            ),
            (
                "What hardware is critical for French systems?",
                "Heavy-duty hinges, espagnolette multi-point locks, and adjustable shoot bolts on the passive leaf. Misaligned meeting stiles cause leaks and security gaps. Floor-level traffic means bottom hardware wears faster — use stainless or coated hardware in coastal Puri projects.",
            ),
        ],
    },
    {
        "slug": "sliding-doors",
        "title": "Sliding Door FAQs",
        "tags": ["sliding", "doors", "balcony", "terrace"],
        "audience": "homeowner",
        "summary": "Large-format sliding doors for balconies and indoor-outdoor living.",
        "faqs": [
            (
                "When should I choose a sliding door instead of a window for balcony access?",
                "Use sliding doors when the opening is walk-through height and you want seamless indoor-outdoor flow — common in ground-floor villas and premium apartments with wide sit-outs. Standard windows with bottom sill at 2–3 ft height are cheaper but less convenient for moving furniture or daily balcony use.",
            ),
            (
                "Do heavy sliding doors need floor tracks?",
                "Most residential UPVC sliding doors use bottom tracks with top guide — the track carries panel weight. Keep tracks clean and level; building settlement can bind panels after years. Lift-and-slide variants exist for very heavy glass but cost more.",
            ),
            (
                "How do sliding doors handle Bhubaneswar dust storms?",
                "Brush seals and good gaskets reduce dust when closed. During pre-monsoon dust, tracks fill quickly — vacuum weekly. Sealed tracks with drain holes outperform open channels. Pair with mesh sliding panels if you ventilate with doors partially open.",
            ),
            (
                "Are sliding doors secure enough for ground floor?",
                "Specify anti-lift blocks, multi-point locks, and laminated glass. Single-point latch doors are vulnerable. Ground-floor installations in Cuttack and Bhubaneswar should treat sliding doors like entry points — not just balcony access.",
            ),
            (
                "What glass weight limits apply to sliding doors?",
                "Fabricators rate rollers for maximum sash weight — typically 80–120 kg per panel for residential systems. Oversized glass for aesthetics must stay within roller and profile limits or hardware fails in 2–3 years. Site survey should confirm panel dimensions and glass type before quoting.",
            ),
            (
                "Can sliding doors reduce AC loss?",
                "Only when fully closed and locked with intact gaskets. Partial opening for ventilation dumps conditioned air. For rooms running AC daily, consider how often doors stay open versus window ventilators for fresh air.",
            ),
        ],
    },
    {
        "slug": "balcony-enclosures",
        "title": "Balcony Enclosure FAQs",
        "tags": ["balcony", "enclosure", "weather", "monsoon"],
        "audience": "homeowner",
        "summary": "Enclosing balconies with UPVC glazing in Odisha apartments and villas.",
        "faqs": [
            (
                "Should I enclose my balcony in Bhubaneswar?",
                "Enclosure adds usable floor area, cuts dust and rain ingress, and can reduce noise from busy roads. Trade-offs include reduced open-air feel, possible builder NOC requirements in apartments, and increased heat if ventilation is poor. Many Patia and Saheed Nagar owners enclose for laundry, study nook, or extended living — it works if you plan operable panels for airflow.",
            ),
            (
                "Will balcony enclosure violate apartment bylaws?",
                "Many Bhubaneswar societies require written approval — facade uniformity and structural load are concerns. Check with your RWA before ordering. Unauthorized enclosure can lead to demolition orders during resale due diligence.",
            ),
            (
                "How do I ventilate an enclosed balcony?",
                "Include sliding or casement panels on at least two sides if possible. Fixed glass only enclosures become greenhouses in summer. Top ventilators and exhaust fans help for laundry drying. Partial enclosure leaving one side open is a compromise some architects prefer.",
            ),
            (
                "Does enclosed balcony help with monsoon laundry drying?",
                "Yes — with mesh vents and fan airflow, enclosed balconies protect clothes during sudden squalls common June–September. Without airflow, humidity traps and clothes smell musty. Design for ventilation first, enclosure second.",
            ),
            (
                "What is the cost difference versus standard balcony glazing?",
                "Full enclosure costs more due to additional framing, floor-track alignment, and larger glass area. Expect 30–50% more than a simple sliding door and window combo for the same opening. Structural sill preparation and tile finishing add civil work cost outside the UPVC quote.",
            ),
            (
                "Can I remove enclosure later if I move?",
                "Physically yes, but patch-up painting and sill repair remain. Bolt-on systems are easier to reverse than silicone-glued structural fixes. Discuss reversibility with installer if you rent or expect to resell.",
            ),
        ],
    },
    {
        "slug": "mosquito-mesh",
        "title": "Mosquito Mesh FAQs",
        "tags": ["mesh", "mosquito", "insect", "ventilation"],
        "audience": "homeowner",
        "summary": "Mosquito mesh options for UPVC windows in Odisha.",
        "faqs": [
            (
                "Which mesh type works best in Bhubaneswar?",
                "Fiberglass pleated or fixed mesh suits most homes — fine enough for mosquitoes, durable in humidity. Stainless mesh resists corrosion near Puri coast but costs more. Aluminium mesh dents easily. Avoid cheap nylon that tears in one season.",
            ),
            (
                "Does mesh block much breeze?",
                "Standard 18×16 mesh reduces airflow slightly — most users do not notice. Pollen and dust filters block more air. For maximum breeze on stagnant evenings, open mesh panels fully rather than relying on cracked glass.",
            ),
            (
                "Sliding mesh or fixed mesh — which to pick?",
                "Sliding mesh cassettes suit windows you open daily — mesh moves with the sash. Fixed outer mesh is cheaper and fine for windows that stay closed with AC most of the year. Hinged mesh shutters work on casement openings.",
            ),
            (
                "How often should mesh be cleaned?",
                "Vacuum or wash every 2–3 months — dust and pollen clog pores and reduce airflow. Monsoon mold on mesh needs mild soap wash and dry. Damaged mesh should be replaced, not patched — gaps let insects through.",
            ),
            (
                "Can mesh be added after window installation?",
                "Yes, but integrated order gives cleaner sightlines and lower cost. Retrofit magnetic strips or add-on frames work on existing UPVC. Plan mesh before fabrication for French and sliding systems.",
            ),
            (
                "Do mesh frames affect window sealing?",
                "Poorly fitted add-on mesh can prevent sashes from closing fully — causing leaks and noise gaps. Quality integrated mesh sits in dedicated tracks without interfering with main gasket compression.",
            ),
        ],
    },
    {
        "slug": "glass-selection",
        "title": "Glass Selection FAQs",
        "tags": ["glass", "glazing", "selection", "performance"],
        "audience": "homeowner",
        "summary": "Choosing the right glass type for each room and exposure in Odisha.",
        "faqs": [
            (
                "Which glass for west-facing balcony?",
                "West-facing balconies in Bhubaneswar take brutal afternoon sun March–June. Use double glazed units with solar control outer pane — tinted, reflective, or low-E coated depending on view priority. Single clear glass turns the balcony into an oven and fades furniture. If budget allows, laminated outer pane adds safety for higher floors.",
            ),
            (
                "How do I choose glass room by room?",
                "Road-facing bedrooms: laminated acoustic double glass. Kitchen and bath: toughened for safety, privacy frosted if needed. Living room view walls: double glazed clear or low tint. Stairwell fixed: toughened. Match performance to exposure and use — not one glass type for whole house.",
            ),
            (
                "Is thicker glass always better?",
                "Thicker glass helps acoustic and safety spans but adds weight and cost. Double glazing with two 4–5 mm panes often beats single 8 mm on heat and noise. Thickness must suit frame capacity and wind load — oversizing causes hinge and roller failure.",
            ),
            (
                "What is the difference between clear, tinted, and reflective glass?",
                "Clear maximizes light and view. Tinted reduces glare and heat but darkens interior. Reflective gives strong privacy day-time and heat rejection but can look commercial. In residential Bhubaneswar, light bronze or grey tint is common compromise on west facades.",
            ),
            (
                "Should bathroom glass be frosted?",
                "Frosted or patterned toughened glass gives privacy without curtains that mold in humid bathrooms. Acid-etched or sandblasted finishes last longer than stick-on films. Operable ventilator with mesh handles moisture better than fixed frosted panel alone.",
            ),
            (
                "Can I upgrade glass later without replacing frames?",
                "Sometimes, if the frame was sized for thicker double units originally. Retrofitting single to double usually requires new sashes or complete replacement. Plan glass at purchase — retrofit is expensive and rarely done well in field conditions.",
            ),
        ],
    },
    {
        "slug": "double-glazing",
        "title": "Double Glazing FAQs",
        "tags": ["double-glazing", "dgu", "insulation", "acoustic"],
        "audience": "homeowner",
        "summary": "Double glazed units for heat, noise, and comfort in Odisha.",
        "faqs": [
            (
                "Is double glazing worth it in Bhubaneswar?",
                "For west-facing rooms, road-facing bedrooms, and anyone running AC 6+ months yearly, double glazing usually pays back in comfort within the first summer and in electricity over 5–7 years. East-facing ventilated rooms with tree shade benefit less — single toughened may suffice there. It is not mandatory everywhere, but it is the single biggest performance upgrade after profile quality.",
            ),
            (
                "How much noise reduction does double glazing provide?",
                "Standard double glazed clear might give 25–30 dB reduction versus open air — modest. Laminated or asymmetric thickness acoustic DGUs improve to 35–42 dB when combined with good UPVC sealing. Expect realistic improvement, not silence — loud honking will still be audible but duller.",
            ),
            (
                "Does double glazing fog up inside?",
                "Quality units with proper spacer desiccant and seal should not fog internally for 10–15 years. Fog between panes means seal failure — unit must be replaced, not cleaned. Edge seal damage from rough handling during transport is a common early failure cause.",
            ),
            (
                "What spacer bar is best in humid climate?",
                "Warm-edge or stainless spacers perform better than plain aluminium in coastal humidity — less edge condensation. Ask fabricator what spacer system they use; cheap aluminium spacers show condensation rings sooner in Puri and Cuttack.",
            ),
            (
                "Can double glazing survive Odisha heat?",
                "Yes — millions of DGUs operate in hotter climates. Air or argon gap expansion is designed for. Use toughened panes where required by size. Dark tint outer panes get hot but heat enters less than single clear.",
            ),
            (
                "Double versus triple glazing for Odisha?",
                "Triple helps extreme noise or north India cold — less critical for Bhubaneswar heat. Triple adds weight and cost; double with good solar control is the sweet spot for most Odisha homes. Triple makes sense for airport-adjacent or highway-facing premium projects.",
            ),
        ],
    },
    {
        "slug": "toughened-glass",
        "title": "Toughened Glass FAQs",
        "tags": ["toughened", "tempered", "safety", "glass"],
        "audience": "homeowner",
        "summary": "When toughened glass is required and how it behaves in UPVC frames.",
        "faqs": [
            (
                "When is toughened glass mandatory?",
                "Indian standards and common practice require toughened glass below certain sill heights, in doors, large fixed panels, and where human impact risk exists. Any glass panel typically below 900 mm from floor or larger than defined area thresholds should be toughened. Insist on marked toughened glass with supplier certification.",
            ),
            (
                "Does toughened glass break into safe pieces?",
                "Yes — it shatters into small granular chunks rather than sharp shards, reducing injury risk. It is stronger against impact but vulnerable to edge nicks — handle carefully during installation. Once tempered, it cannot be cut — field size errors mean remaking the pane.",
            ),
            (
                "Is toughened glass required for upper-floor windows?",
                "Height alone may trigger toughening for large spans even on upper floors — wind load and fall risk matter. Balcony railing infill and full-height fixed panels almost always use toughened or laminated. Confirm with fabricator per opening size.",
            ),
            (
                "Can toughened and non-toughened mix in one window?",
                "Operable sashes often use toughened while small fixed transoms might use float — depends on size and location. Consistency simplifies replacement; many projects toughen all external glass for uniform safety policy.",
            ),
            (
                "Does toughening affect heat or noise performance?",
                "Toughening process does not materially change thermal or acoustic properties — those come from thickness, lamination, and double glazing. Do not confuse safety toughening with performance glazing upgrades.",
            ),
            (
                "What if toughened glass breaks after installation?",
                "Spontaneous breakage is rare but possible due to nickel sulphide inclusions — more common in large unlaminated toughened panels. Keep warranty terms; replacement is usually covered if not impact damage. Laminated toughened reduces fall-through risk after breakage.",
            ),
        ],
    },
    {
        "slug": "soundproofing",
        "title": "Soundproofing FAQs",
        "tags": ["sound", "noise", "acoustic", "traffic"],
        "audience": "homeowner",
        "summary": "Reducing traffic and neighbourhood noise with UPVC and glass in Odisha cities.",
        "faqs": [
            (
                "How much can UPVC windows reduce road noise?",
                "A complete system — casement profile, multi-point lock, acoustic laminated double glass — can cut perceived traffic noise by 60–70% versus old wooden or aluminium single-glazed windows. Sliding systems achieve less unless premium acoustic gaskets and glass are specified. Noise finds the weakest path — seal gaps around AC pipes and walls too.",
            ),
            (
                "Which is better for noise: casement or sliding?",
                "Casement generally seals better when locked. High-end sliding with acoustic glass can approach casement performance but costs more. For NH-facing bedrooms in Cuttack or Bhubaneswar, casement with acoustic glass is the default recommendation.",
            ),
            (
                "Does laminated glass help with noise?",
                "Yes — the PVB interlayer dampens vibration. Asymmetric double glazed units (different pane thickness) target specific frequency ranges. Specify acoustic laminated, not just safety laminated — performance differs.",
            ),
            (
                "Will curtains or films match UPVC acoustic upgrade?",
                "Heavy curtains help marginally; films barely affect low-frequency traffic rumble. Structural upgrade through frames and glass delivers real change. Curtains complement but do not replace proper glazing.",
            ),
            (
                "Can I soundproof only one bedroom?",
                "Absolutely — phased approach is common. Road-facing master bedroom first, others later. Ensure the room has minimal alternate leak paths — hollow core doors, vent holes, and AC sleeves matter.",
            ),
            (
                "How do I verify noise performance before paying?",
                "Visit a completed reference home near similar traffic if possible. Decibel readings before/after are rare in residential sales but some installers offer basic measurement. At minimum, inspect gasket compression and glass spec on sample mockup.",
            ),
        ],
    },
    {
        "slug": "heat-reduction",
        "title": "Heat Reduction FAQs",
        "tags": ["heat", "solar", "cooling", "sun"],
        "audience": "homeowner",
        "summary": "Cutting solar heat gain through windows in hot Odisha summers.",
        "faqs": [
            (
                "Will UPVC fade in Odisha heat?",
                "Quality lead-free UPVC with UV-stabilized colour lamination should not fade noticeably for 10–15 years in Bhubaneswar sun. Budget profiles without proper stabilizers yellow and chalk — especially white on west facades. Choose reputed profile brands and avoid darkest colours on maximum exposure if heat buildup inside the frame concerns you.",
            ),
            (
                "Which window orientation gets hottest in my home?",
                "West facades peak afternoon; south gets sustained sun; east gets morning heat; north is mildest. In Odisha, west and south-west cause the most AC load. Prioritize solar control glass and shading on those exposures first.",
            ),
            (
                "Do external shades or UPVC glass work better?",
                "External shading — chhajja, balcony overhang, roller shutter — blocks heat before it hits glass and works best. Good low-E or tinted double glazing is the next line when external shade is limited. Internal curtains only block already-entered heat — least effective alone.",
            ),
            (
                "How much hotter is room with single clear glass?",
                "Surface temperatures and radiant heat can make a west room 3–5°C warmer at peak versus double glazed solar control in the same envelope. Comfort difference is significant even if thermostat reads similar — radiant heat from glass feels oppressive.",
            ),
            (
                "Does white UPVC reflect heat better than brown?",
                "Slightly lower surface temperature on white frames, but glass area dominates heat gain. Colour choice is aesthetic and maintenance — dark browns hide dirt but absorb more on frame edges. Glass spec matters more than frame colour for room heat.",
            ),
            (
                "Can green building glass tint affect indoor plants?",
                "Heavy reflective coatings reduce PAR light — indoor plants near such windows may struggle. Light bronze tint usually fine. Discuss tint level if you have sunrooms or plant-heavy interiors.",
            ),
        ],
    },
    {
        "slug": "energy-saving",
        "title": "Energy Saving FAQs",
        "tags": ["energy", "ac", "bills", "efficiency"],
        "audience": "homeowner",
        "summary": "How better windows lower AC consumption in Odisha.",
        "faqs": [
            (
                "Can new UPVC windows reduce AC bills?",
                "Yes — homeowners commonly report 15–25% AC electricity reduction after replacing leaky single-glazed windows with sealed UPVC double glazing on primary exposures, assuming AC usage pattern stays similar. Savings depend on how many hours AC runs, tariff slab, and which rooms were upgraded. Biggest gains come from west-facing bedrooms and living areas that ran AC all afternoon.",
            ),
            (
                "Which upgrade saves the most energy per rupee?",
                "Sealing air leaks and upgrading glass on west/south rooms first. Full-house double glazing beats partial, but phased west-room upgrade delivers fastest payback feel. Low-E double glazed units outperform single toughened on thermal metrics.",
            ),
            (
                "Do air gaps in old windows really matter?",
                "Enormously — a 2 mm gap around a sash can waste as much cooling as several square feet of poor glass. Old windows often leak at multiple points. UPVC with new gaskets eliminates most infiltration when closed.",
            ),
            (
                "Should I keep windows open at night to save AC?",
                "During dry winter nights in Bhubaneswar, natural ventilation works. During humid pre-monsoon and monsoon, open windows increase moisture load — AC works harder dehumidifying. Use mesh ventilators for short air exchange rather than wide open all night in humid months.",
            ),
            (
                "Is star-rated glass available for residential UPVC?",
                "Performance ratings exist for IGUs — ask for U-value and SHGC numbers on quote. Lower U-value and appropriate SHGC for orientation guide selection better than marketing labels alone.",
            ),
            (
                "How long until energy savings pay back window cost?",
                "Rough payback 5–10 years on energy alone for full-home upgrade in heavy AC users — faster if replacing extremely poor existing windows. Comfort and noise benefits are immediate and often valued more than pure ROI math.",
            ),
        ],
    },
    {
        "slug": "rain-protection",
        "title": "Rain Protection FAQs",
        "tags": ["rain", "water", "sealing", "monsoon"],
        "audience": "homeowner",
        "summary": "Keeping monsoon rain out with proper UPVC design and installation.",
        "faqs": [
            (
                "How do UPVC windows stop driving rain?",
                "Multi-chamber profiles with overlapping sashes, EPDM gaskets, and sloped sills direct water to drainage channels and out through weep holes. Pressure equalization reduces water being forced inward. Installation sealant and outer drip caps complete the system — product and installation both matter.",
            ),
            (
                "What is a sill slope and why does it matter?",
                "Outer sill should slope 5–10 degrees outward so water runs off, not into the room. Flat or inward-sloping sills pool water that finds any gap. Many leakage complaints trace to civil sill condition, not the window frame itself.",
            ),
            (
                "Do I need chhajja over every window?",
                "Not mandatory but highly recommended on exposed facades without balcony overhang. Extended chhajja reduces direct rain on glass and frame joints during cyclonic squalls. Retrofit chhajja helps chronic leak openings.",
            ),
            (
                "Can rain enter through wall-window junction?",
                "Yes — if foam filling and sealant are skimped. Proper installation uses packers, PU foam, and silicone inside and out. Plaster crack near frame edge is a common secondary leak path after building movement.",
            ),
            (
                "Are pressure relief drain holes visible?",
                "Weep holes are small slots in outer track — intentionally visible for drainage. Do not seal them thinking they are defects. Keep them clear of dust and paint during finishing work.",
            ),
            (
                "How to test rain performance before monsoon?",
                "Hose test on installed windows — moderate water spray on closed sash for 5 minutes while checking inside sill. Fix issues before full monsoon. Builder handover should include this for new installs.",
            ),
        ],
    },
    {
        "slug": "monsoon-issues",
        "title": "Monsoon Window Issues FAQs",
        "tags": ["monsoon", "humidity", "leak", "maintenance"],
        "audience": "homeowner",
        "summary": "Common monsoon problems with windows and how to prevent them in Odisha.",
        "faqs": [
            (
                "Why do windows leak only during heavy monsoon?",
                "Wind-driven rain exceeds design pressure on poorly sealed or misaligned sashes. Intermittent leaks often mean marginal gasket compression — fine in light rain, fails in squalls. Blocked drainage overflows track into interior. Schedule pre-monsoon service every May.",
            ),
            (
                "Is condensation on glass normal in monsoon?",
                "Some interior surface condensation when cold AC meets humid monsoon air is normal physics — wipe and improve airflow. Condensation between double glass panes indicates seal failure. Edge condensation on frame can mean indoor humidity is very high or spacer issue.",
            ),
            (
                "Do UPVC windows swell in humidity?",
                "Quality UPVC is dimensionally stable — unlike wood. If sash binds in monsoon, check for dirt in track, building settlement, or hardware misalignment — not material swelling.",
            ),
            (
                "Should I keep windows closed all monsoon?",
                "Close during driving rain; open during dry breaks for ventilation to prevent mold on walls and curtains. Mesh ventilators allow air with less rain entry than full sash opening.",
            ),
            (
                "How does Fani and cyclone history affect window choice?",
                "Post-Fani, more Bhubaneswar owners specify stronger hardware, laminated glass, and verified anchoring. Cyclone clips and screw fixings into concrete — not just brick — matter in coastal districts. Design for 150+ km/h gusts on upper floors.",
            ),
            (
                "When is the best time to install new windows in Odisha?",
                "October–February dry season ideal — sealants cure properly, less rain disruption. Monsoon installs possible with precautions but curing and leak testing harder. Book early before pre-summer rush.",
            ),
        ],
    },
    {
        "slug": "coastal-areas",
        "title": "Coastal Area Window FAQs",
        "tags": ["coastal", "puri", "salt", "corrosion"],
        "audience": "homeowner",
        "summary": "UPVC window considerations for Puri, Konark, and Odisha coast.",
        "faqs": [
            (
                "What is different for sea-facing homes near Puri?",
                "Salt air accelerates metal corrosion — specify stainless steel or coastal-grade hardware, rinse tracks monthly, and use laminated glass for windborne debris resistance. UPVC profiles themselves resist salt but hinges and screws fail first if wrong grade. Extra drainage capacity handles monsoon plus sea spray combined.",
            ),
            (
                "How far inland does coastal specification matter?",
                "Within roughly 5 km of high tide line, treat as coastal. Bhubaneswar city is inland enough for standard hardware though humidity still high. Paradeep, Gopalpur, and beachfront Puri need coastal pack without exception.",
            ),
            (
                "Will salt stain my white UPVC frames?",
                "Salt deposits wash off with fresh water — neglect lets abrasion and staining build. Rinse exterior frames monthly in coastal homes. Avoid abrasive cleaners that scratch lamination.",
            ),
            (
                "Are sliding doors safe in cyclone-prone beach villas?",
                "With laminated glass, anti-lift locks, and proper anchoring, yes — but owners should shutter or board extremely exposed openings when cyclone warning issued. No operable window survives direct debris impact from cyclone — manage expectations.",
            ),
            (
                "Does marine plywood subframe work near coast?",
                "Avoid wood subframes near coast — use UPVC direct fix or aluminium subframe with isolation. Termite and rot risk plus salt on any metal fasteners.",
            ),
            (
                "How often to service coastal installations?",
                "Quarterly track clean and hardware lube versus twice yearly inland. Post-monsoon full inspection mandatory. Replace any rusted screws immediately — they spread failure to frame alignment.",
            ),
        ],
    },
    {
        "slug": "cyclone-safety",
        "title": "Cyclone Safety FAQs",
        "tags": ["cyclone", "fani", "wind", "safety"],
        "audience": "homeowner",
        "summary": "Window performance and safety during Odisha cyclones.",
        "faqs": [
            (
                "Can UPVC windows withstand Odisha cyclones?",
                "Quality installed UPVC with correct glass, steel reinforcement, and anchor fixings withstands typical cyclonic wind pressures in Bhubaneswar and Cuttack when windows are closed and locked. Extreme Category 4+ direct hits may cause damage from flying debris — laminated glass reduces shatter risk. Weak installs fail regardless of material — anchoring into structural concrete is critical.",
            ),
            (
                "Should I tape windows during cyclone warning?",
                "Tape does not stop breakage — it may reduce shard scatter slightly. Better to close shutters, use plywood boards on ground floor, and keep away from glass during peak winds. Laminated glass holds together if broken.",
            ),
            (
                "What failed most during Cyclone Fani in Bhubaneswar?",
                "Large unsupported fixed glass without toughening, poorly anchored frames, and aluminium without maintenance topped failure lists. Sliding doors without anti-lift blew inward in some cases. Post-Fani replacements emphasized laminated glass and screw fixings.",
            ),
            (
                "Are openable windows safer closed or cracked during cyclone?",
                "Fully closed and locked — cracked openings allow pressure changes and water ingress. Pressure equalization is designed into profile drainage, not user-opened vents during storm.",
            ),
            (
                "Do high-rise windows face higher wind load?",
                "Yes — wind speed increases with height. Upper floors in Bhubaneswar towers need wind-load calculation for glass thickness and fixings. Do not copy ground-floor spec to penthouse without engineering review.",
            ),
            (
                "Insurance and cyclone damage to windows?",
                "Home insurance may cover cyclone damage depending on policy — document pre-storm condition and use licensed installers for claims support. Warranty typically excludes act-of-god but manufacturing defects still covered if separable.",
            ),
        ],
    },
    {
        "slug": "security",
        "title": "Window Security FAQs",
        "tags": ["security", "lock", "theft", "safety"],
        "audience": "homeowner",
        "summary": "Securing UPVC windows against break-in in urban Odisha.",
        "faqs": [
            (
                "Are UPVC windows easy to break into?",
                "No more than aluminium if hardware is quality — less than old wooden latched windows. Weak single-point locks and non-laminated glass are the vulnerability. Multi-point locks, anti-lift blocks on sliders, and laminated glass raise difficulty substantially.",
            ),
            (
                "Ground floor apartment — minimum security spec?",
                "Multi-point lock casement or secured slider, laminated glass on accessible openings, restrict ventilator opening width. Grills are personal choice — some societies ban external grills; internal bars or lockable restrictors alternative.",
            ),
            (
                "Do security grills clash with UPVC aesthetics?",
                "External grills cover frame beauty — popular in Cuttack independent houses, less in gated Bhubaneswar apartments. Internal collapsible grills or laminated glass with strong locks are compromises.",
            ),
            (
                "Can smart locks integrate with UPVC?",
                "Select hardware brands offer compatible smart handles — verify before order. Retrofit smart locks limited; plan integration during fabrication for clean fit.",
            ),
            (
                "Is laminated glass worth it for security alone?",
                "Laminated resists repeated impact better than toughened alone — harder to punch through quietly. Combined acoustic and security benefit makes it worthwhile on vulnerable openings even if noise is not primary concern.",
            ),
            (
                "What about glass on bathroom ventilator — security risk?",
                "Small high ventilators are low priority; ground-floor bath vents may use frosted toughened. Mesh outside reduces climb incentive.",
            ),
        ],
    },
    {
        "slug": "child-safety",
        "title": "Child Safety FAQs",
        "tags": ["child", "safety", "fall", "lock"],
        "audience": "homeowner",
        "summary": "Keeping children safe around windows and balcony doors.",
        "faqs": [
            (
                "How to prevent children falling from apartment windows?",
                "Use opening restrictors limiting sash to 100 mm, child-safe locks adults can override, and never rely on mesh as fall barrier. Move furniture away from windows children could climb. Building codes and RWAs increasingly require restrictors on high floors.",
            ),
            (
                "Are restrictors available on sliding windows?",
                "Yes — lockable stoppers and key-operated restrictors exist for sliders and casements. Specify at order; retrofit kits available but less elegant.",
            ),
            (
                "Is low sill French window safe with toddlers?",
                "Additional caution — consider temporary barriers until children older. Laminated glass reduces injury if impact occurs but prevention beats stronger glass.",
            ),
            (
                "Can children operate multi-point locks?",
                "Keyed handles on bedrooms prevent young children opening windows unsupervised. Teach older children balcony safety without relying on product alone.",
            ),
            (
                "Do mosquito mesh windows stop falls?",
                "No — standard mesh is not load-bearing. Children leaning on mesh have fallen through. Use proper grills or restrictors.",
            ),
            (
                "Balcony door child lock options?",
                "Secondary floor bolts, chain locks, and handle covers delay child access. Keep keys out of reach for lockable restrictors.",
            ),
        ],
    },
    {
        "slug": "maintenance",
        "title": "UPVC Window Maintenance FAQs",
        "tags": ["maintenance", "care", "service", "longevity"],
        "audience": "homeowner",
        "summary": "Routine maintenance for UPVC windows in Odisha climate.",
        "faqs": [
            (
                "How often should UPVC windows be serviced?",
                "Basic homeowner care monthly — wipe tracks, check drainage. Professional hardware adjustment every 2–3 years or if operation stiffens. Coastal and road-dust areas benefit from quarterly track cleaning.",
            ),
            (
                "What lubricant for hinges and locks?",
                "Light silicone spray or manufacturer-recommended lubricant — avoid heavy grease that attracts dust. WD-40 occasionally okay on hinges; not ideal long-term. Wipe excess to prevent dust buildup in Bhubaneswar pollen season.",
            ),
            (
                "Can I adjust misaligned casement myself?",
                "Minor hinge adjustment possible with hex key on many systems — follow manufacturer guide. Major misalignment from settlement needs installer visit. Forcing stiff sash damages hinges.",
            ),
            (
                "When to replace gaskets?",
                "If daylight visible when closed or water misting through — gaskets may be compressed or torn. Replacement every 10–15 years normal; coastal UV may shorten. Not DIY friendly on some systems.",
            ),
            (
                "Does UPVC need repainting?",
                "No — lamination colour is integral. Scratches on foil may be touched up with colour-matched pen; deep damage rare on quality profiles. Avoid abrasive cleaners.",
            ),
            (
                "Should I cover windows during exterior painting?",
                "Yes — paint splatter on glass and silicone ruins aesthetics. Mask frames during civil work. PU foam overspray during careless install causes permanent marks — supervise finishing trades.",
            ),
        ],
    },
    {
        "slug": "cleaning",
        "title": "Window Cleaning FAQs",
        "tags": ["cleaning", "care", "glass", "frames"],
        "audience": "homeowner",
        "summary": "Safe cleaning methods for UPVC frames and glass in Odisha.",
        "faqs": [
            (
                "What cleaner is safe for UPVC frames?",
                "Mild soap and water with soft cloth — same as daily household cleaning. Avoid acetone, thinners, and abrasive scouring pads that scratch lamination. Monsoon mold spots respond to diluted vinegar then rinse.",
            ),
            (
                "How to clean tracks without damaging drainage?",
                "Vacuum loose dirt first, then damp cloth. Use soft brush for corners — not metal tools blocking weep holes. Dry tracks after cleaning prevent rust on steel reinforcement exposure if scratched.",
            ),
            (
                "Best way to clean double glazed exterior on upper floors?",
                "Professional rope access or balcony reach. Hinged casements that tilt for cleaning reduce need. Fixed high glass needs scheduled building maintenance — plan at install.",
            ),
            (
                "Hard water stains on glass near Bhubaneswar?",
                "Mineral deposits from bore water splash — white vinegar or commercial glass descaler on cool glass, not hot sun. Prevent with prompt drying after hose wash.",
            ),
            (
                "How often to clean coastal homes?",
                "Rinse salt monthly from frames and hardware in Puri area. Standard inland monthly frame wipe, weekly glass if road dust heavy.",
            ),
            (
                "Can pressure washer clean UPVC windows?",
                "Avoid high pressure on tracks and gasket areas — forces water inward and damages seals. Low rinse on glass and outer frame okay if angled away from joints.",
            ),
        ],
    },
    {
        "slug": "hardware-faq",
        "title": "Window Hardware FAQs",
        "tags": ["hardware", "hinges", "locks", "rollers"],
        "audience": "homeowner",
        "summary": "Locks, hinges, handles, and rollers for UPVC systems.",
        "faqs": [
            (
                "Which hardware brands hold up in Odisha humidity?",
                "European-origin systems like Roto, Siegenia, Maco, and Kinlong coastal grades perform well when genuine. Cheap unbranded copies fail within 2–3 monsoons. Verify brand on quote, not just 'imported hardware'.",
            ),
            (
                "What is multi-point locking?",
                "Handle operation drives multiple locking pins around sash perimeter — better seal and security than single cam lock. Essential for casement bedrooms and entry doors. Check how many points engage on your quote.",
            ),
            (
                "How long do rollers last on sliding windows?",
                "Typical residential use 8–12 years before replacement needed. Heavy doors and coastal salt may shorten. Replacement is routine service, not sign of bad window if profile still sound.",
            ),
            (
                "Can handles be changed to different colour later?",
                "Often yes if same backset and spindle — order matching finish from hardware supplier. White versus chrome is common upgrade for interior design refresh.",
            ),
            (
                "What is friction stay on casement?",
                "Hinged arm holding sash open at set angles — quality stays allow micro-ventilation positions. Cheap stays slip in wind — dangerous on upper floors. Use branded stays rated for sash weight.",
            ),
            (
                "Are cylinder locks needed on windows?",
                "Keyed cylinders on ground-floor or child-safety applications. Most bedroom windows use handle lock without key — convenience versus security trade-off.",
            ),
        ],
    },
    {
        "slug": "warranty-faq",
        "title": "Warranty FAQs",
        "tags": ["warranty", "claim", "coverage", "guarantee"],
        "audience": "homeowner",
        "summary": "Understanding UPVC window warranty terms and claims.",
        "faqs": [
            (
                "What does a typical UPVC window warranty cover?",
                "Profile discoloration beyond normal, hardware failure under normal use, and manufacturing defects in fabrication — typically 5–10 years on profile, 1–3 years on hardware depending on brand. Glass usually follows separate manufacturer warranty. Installation workmanship often 1 year — leaks from poor install should be installer responsibility.",
            ),
            (
                "What is usually excluded from warranty?",
                "Act of god cyclone damage, user misuse, unauthorized modifications, failure to maintain drainage, and impact breakage. Normal gasket wear after years may be excluded. Read exclusions before signing.",
            ),
            (
                "How do I register a warranty claim?",
                "Keep invoice, contract, and serial or batch references. Photo document issue, contact installer with written description. Avoid DIY disassembly that voids coverage. Response time varies — escalate with manufacturer if dealer unresponsive.",
            ),
            (
                "Does warranty transfer to new owner on resale?",
                "Often yes if documented transfer within policy period — confirm with original supplier. Helps resale value in Bhubaneswar gated communities.",
            ),
            (
                "Is extended warranty worth buying?",
                "Only if it covers hardware and labour beyond standard — compare cost to expected roller and gasket service. Profile failures rare on good brands; hardware is wear item.",
            ),
            (
                "Glass fog between panes — warranty or replacement?",
                "Seal failure in DGU — glass unit manufacturer or window supplier should replace if within glass warranty period. Not repairable in field.",
            ),
        ],
    },
    {
        "slug": "installation-faq",
        "title": "Installation Process FAQs",
        "tags": ["installation", "site-survey", "timeline", "process"],
        "audience": "homeowner",
        "summary": "What happens from site survey to handover for UPVC windows.",
        "faqs": [
            (
                "How long from measurement to installation?",
                "Typically 2–4 weeks after confirmed measurements and advance — depends on opening count and glass lead time. Peak season March–May may extend. Custom colours add time.",
            ),
            (
                "What happens during site survey?",
                "Technician measures each opening width/height at multiple points, checks lintel and sill condition, notes wall material, exposure, and client preferences. Photos document context. Accurate survey prevents fabrication errors — never skip for remote quote only.",
            ),
            (
                "How messy is window replacement?",
                "Old frame removal creates dust and debris — cover furniture, expect 1–2 days disruption per room batch. Install team should remove old frames and seal new ones same day where possible. Civil patch work may follow.",
            ),
            (
                "Can windows be installed while I live in the home?",
                "Yes — room-by-room sequence minimizes exposure. Night security temporary board if opening left open — reputable teams avoid overnight gaps.",
            ),
            (
                "Who handles painting after install?",
                "Usually homeowner's painter patches reveal gaps between frame and plaster. Clarify in contract — some installers include basic silicone and foam only.",
            ),
            (
                "What should I check at handover?",
                "Smooth operation all sashes, locks engaging, no daylight gaps, drainage holes clear, glass undamaged, labels removed, cleaning done. Written completion sign-off with warranty documents.",
            ),
        ],
    },
    {
        "slug": "repairs",
        "title": "Window Repair FAQs",
        "tags": ["repair", "fix", "service", "broken"],
        "audience": "homeowner",
        "summary": "When UPVC windows can be repaired versus replaced.",
        "faqs": [
            (
                "Can a cracked glass pane be replaced without new frame?",
                "Yes — glazier removes beads, swaps glass unit, reseals. Match glass type and thickness. Toughened must be remade to size. Schedule before monsoon if opening exposed.",
            ),
            (
                "Stiff handle or broken lock — repairable?",
                "Usually replace lock body or handle set — standard service call. Match hardware brand for fit. Forcing broken handle damages gearbox — stop using and call service.",
            ),
            (
                "Can warped sash be straightened?",
                "Minor alignment via hinge adjustment; severe warp from cheap profile or heat damage may need sash replacement. Full frame warp is rare in UPVC — investigate cause.",
            ),
            (
                "Is silicone resealing enough for leaks?",
                "If leak is at wall junction, resealing helps. If gasket compression failed or sill slope wrong, silicone is band-aid — needs proper fix.",
            ),
            (
                "Repair old windows or replace all?",
                "If profile is chalking, yellowed, or multiple panes fogging — replace. Single hardware or glass issue on 5-year-old quality install — repair economical.",
            ),
            (
                "Emergency board-up after breakage?",
                "Plywood or coroplast temporary — many installers offer emergency service in Bhubaneswar monsoon season. Laminated glass may stay intact until scheduled replacement.",
            ),
        ],
    },
    {
        "slug": "leakage-problems",
        "title": "Water Leakage FAQs",
        "tags": ["leak", "water", "monsoon", "troubleshoot"],
        "audience": "homeowner",
        "summary": "Diagnosing and fixing UPVC window water leakage in Odisha.",
        "faqs": [
            (
                "What are the common water leakage causes?",
                "Blocked drainage weep holes, missing or hardened gaskets, incorrect sill slope, poor outer sealant, sash misalignment from worn rollers, and water tracking from wall cracks above window — not the frame itself. Identify source by wet pattern: sill front suggests drainage; frame joint suggests gasket; top suggests wall or chhajja failure.",
            ),
            (
                "Why does my sliding window leak at the meeting rail?",
                "Worn rollers let sash sit low — meeting rail no longer aligns for water shed. Clean drainage, adjust rollers, replace if flattened. Monsoon wind drives rain horizontally into misaligned rails.",
            ),
            (
                "Leak appeared one year after install — why?",
                "Building settlement shifted frame, sealant cracked, or foam compressed. Warranty claim likely if within workmanship period. Settlement common in new Bhubaneswar apartments first monsoon.",
            ),
            (
                "Can interior silicone stop leaks?",
                "Interior seal traps water in wall — wrong approach. Fix exterior path of water entry. Interior silicone hides problem until wall damage grows.",
            ),
            (
                "Who fixes leak — builder or window company?",
                "If leak at frame-wall junction from install — window company. If from roof or chhajja above — builder or civil contractor. Document with video for responsibility clarity.",
            ),
            (
                "Preventive steps before next monsoon?",
                "Clear weep holes, lubricate and adjust hardware, inspect outer silicone, hose test in April. Fix tile sill gaps outside — common overlooked leak path.",
            ),
        ],
    },
    {
        "slug": "cost-pricing",
        "title": "Cost and Pricing FAQs",
        "tags": ["cost", "price", "budget", "quote"],
        "audience": "homeowner",
        "summary": "Understanding UPVC window pricing in Bhubaneswar and Odisha.",
        "faqs": [
            (
                "What is the typical cost per window in Bhubaneswar?",
                "Standard bedroom casement 4×4 ft with double glazing roughly ₹14,000–22,000 installed in 2026 market — varies by brand, glass, and hardware. Large balcony slider 8×7 ft can run ₹35,000–55,000. Always per-opening quote after survey, not per sq ft alone.",
            ),
            (
                "Why do quotes vary so much between dealers?",
                "Profile brand, hardware genuineness, glass spec, installation quality, and warranty terms differ. Lowest quote often drops hardware grade or installation steps. Compare line-item specs, not lump sum only.",
            ),
            (
                "Is per square foot pricing reliable?",
                "Rough budgeting only — odd sizes, small ventilators, and doors distort sq ft math. Insist on itemized opening list after survey.",
            ),
            (
                "What hidden costs should I ask about?",
                "Scaffolding, old frame disposal, civil sill repair, mesh, restrictors, colour surcharge, GST, and travel for outstation sites. Clarify before advance payment.",
            ),
            (
                "Does monsoon season affect pricing?",
                "Install difficulty may add cost; some dealers discount slow season monsoon for faster slot fill — varies. Material prices fluctuate with resin and glass market.",
            ),
            (
                "Payment schedule best practice?",
                "Common pattern: small booking advance, balance on delivery or completion. Avoid 100% upfront without delivery timeline in contract. Staged payment tied to milestones protects both parties.",
            ),
        ],
    },
    {
        "slug": "apartment-projects",
        "title": "Apartment Window FAQs",
        "tags": ["apartment", "flat", "high-rise", "bhubaneswar"],
        "audience": "homeowner",
        "summary": "UPVC windows for Bhubaneswar apartments and flats.",
        "faqs": [
            (
                "Can I replace windows in a gated apartment without builder approval?",
                "Most societies require NOC — facade colour and structural rules apply. Unauthorized change causes resale complications. Submit profile sample and colour to RWA before order.",
            ),
            (
                "Are sliding windows default for apartments?",
                "Common for balcony but bedrooms often benefit from casement upgrade if society allows. Builder-grade install at possession is often minimum spec — owners upgrade for noise and heat.",
            ),
            (
                "High-rise wind — special considerations?",
                "Upper floors need wind-load appropriate glass and fixings. Install team must use rope safety compliance. Some societies restrict work hours for exterior install.",
            ),
            (
                "Noise from neighbouring flat AC units?",
                "Acoustic glass on shared-wall adjacent windows helps marginally — most noise enters own balcony opening. Seal balcony slider well.",
            ),
            (
                "Replacing all windows while living in flat — feasible?",
                "Room-wise over 2–3 weekends common. Coordinate with society for material lift and debris removal. Dust containment sheets used by professional teams.",
            ),
            (
                "Do apartments use white or coloured UPVC?",
                "White and off-white dominate for facade uniformity. Woodgrain laminates growing in premium towers for interior-facing style with white exterior as per RWA.",
            ),
        ],
    },
    {
        "slug": "villas",
        "title": "Villa Window FAQs",
        "tags": ["villa", "independent", "duplex", "premium"],
        "audience": "homeowner",
        "summary": "Window solutions for independent houses and villas in Odisha.",
        "faqs": [
            (
                "What window mix suits a typical Bhubaneswar villa?",
                "Ground floor living: large sliding or French to garden; bedrooms: casement acoustic; stairwell: fixed toughened; kitchen: casement with mesh. Independent house freedom allows mix without RWA colour lock — still plan facade harmony.",
            ),
            (
                "Double-height living room glazing — options?",
                "Fixed toughened upper with operable lower casement or sliding — full double-height operable expensive and hard to maintain. Structural support for lintel critical — engineer input for wide spans.",
            ),
            (
                "Villa security without looking like a fortress?",
                "Laminated glass, multi-point locks, sensor-ready locks. Internal mesh shutters less visible than external bars. Landscape lighting deters better than ugly bars alone.",
            ),
            (
                "Independent house timeline versus apartment?",
                "Often faster NOC-wise but larger opening count extends fabrication. Villa projects 15–40 openings common — phased install by floor works.",
            ),
            (
                "Matching windows to traditional villa architecture?",
                "Woodgrain UPVC, divided lite grids (dummy or true), and arched fixed toppers available — cost premium. Balance authenticity with maintenance reality.",
            ),
            (
                "Garden-facing French doors — drainage on tile floor?",
                "Threshold drain and slight exterior slope prevent water pooling at indoor-outdoor transition. Tile level flush with threshold needs careful detail — common leak point in villa installs.",
            ),
        ],
    },
    {
        "slug": "commercial-buildings",
        "title": "Commercial Building FAQs",
        "tags": ["commercial", "office", "retail", "facade"],
        "audience": "sales",
        "summary": "UPVC and glazing for offices, shops, and commercial facades in Odisha.",
        "faqs": [
            (
                "Is UPVC suitable for ground-floor retail shops?",
                "Yes for operable sections — sliders for display ventilation, fixed for signage zones. Heavy foot traffic needs durable hardware and laminated safety glass. Aluminium may be specified for very large storefront spans.",
            ),
            (
                "Office AC efficiency and glazing?",
                "Low-E double glazing on sun-facing curtain wall sections reduces chiller load — important for Bhubaneswar IT offices running AC all day. Payback faster than residential on commercial tariffs.",
            ),
            (
                "Fire exit door requirements?",
                "Follow NBC and local fire norms — UPVC may not suit all fire-rated exit requirements. Consult fire consultant for escape routes; UPVC for general office windows separate from rated doors.",
            ),
            (
                "Maintenance contract for commercial installs?",
                "Annual service contract recommended for 20+ opening offices — rollers, locks, and gaskets at scale. Document PM schedule for facility managers.",
            ),
            (
                "Noise from road-facing showrooms?",
                "Acoustic laminated double glazing when display windows must be large single panes — limited operable area. Combined with entrance air curtain for AC retention.",
            ),
            (
                "Lead time for 50+ opening commercial project?",
                "4–8 weeks fabrication plus phased install — coordinate with fit-out schedule. Mock-up window on one opening for approval before batch production.",
            ),
        ],
    },
    {
        "slug": "schools",
        "title": "School Window FAQs",
        "tags": ["school", "education", "safety", "ventilation"],
        "audience": "sales",
        "summary": "Window specifications for schools and educational buildings in Odisha.",
        "faqs": [
            (
                "What safety glass for classroom windows?",
                "Toughened or laminated mandatory for lower sill heights and door glazing — child impact risk. Avoid non-toughened large low panels.",
            ),
            (
                "Ventilation versus AC in classrooms?",
                "Operable casement with mesh for natural vent schools; sealed double glaze for AC labs and computer rooms. Hybrid building uses both by room function.",
            ),
            (
                "Durability for high-use school environment?",
                "Heavy-duty hinges, anti-tamper handles, and impact-resistant laminates. Expect vandalism and ball impact — budget replaceable glass units.",
            ),
            (
                "Sound from playground — acoustic needs?",
                "Road-facing admin blocks benefit acoustic glass; internal courtyard classrooms less critical. Openable area for cross-vent during power cuts still matters in Odisha.",
            ),
            (
                "Maintenance during summer break?",
                "Schedule roller and lock service May–June when schools empty — minimal disruption. Align with annual painting cycle.",
            ),
            (
                "Colour and aesthetics for schools?",
                "White or light grey standard — minimises heat. Custom school colours possible on large orders with lead time.",
            ),
        ],
    },
    {
        "slug": "hospitals",
        "title": "Hospital Window FAQs",
        "tags": ["hospital", "healthcare", "hygiene", "acoustic"],
        "audience": "sales",
        "summary": "Glazing considerations for hospitals and clinics in Odisha.",
        "faqs": [
            (
                "Hygiene cleaning compatibility with UPVC?",
                "Smooth UPVC surfaces tolerate hospital-grade disinfectants better than painted wood — avoid abrasive solvents. Sealed gaskets reduce dust traps versus old steel windows.",
            ),
            (
                "Patient room noise control?",
                "Acoustic laminated double glazing on ward windows facing equipment or roads. Operable portion for fresh air with mesh — balance infection control ventilation policy.",
            ),
            (
                "ICU and controlled areas — operable windows?",
                "Often fixed sealed units with mechanical HVAC — no casual operable windows. Spec driven by infection control consultant.",
            ),
            (
                "Privacy glazing for ground-floor clinics?",
                "Frosted or switchable privacy where budget allows. One-way vision films less durable in harsh cleaning regimes.",
            ),
            (
                "Emergency replacement service expectations?",
                "Hospitals need 24–48 hr glass replacement SLA for broken units — agree in maintenance contract upfront.",
            ),
            (
                "Fire and smoke compartmentation?",
                "UPVC windows are not fire-rated barriers — fire strategy uses rated walls and doors. Window role is secondary — follow hospital fire plan.",
            ),
        ],
    },
    {
        "slug": "architects",
        "title": "Architect and Designer FAQs",
        "tags": ["architect", "specification", "design", "technical"],
        "audience": "sales",
        "summary": "Technical information architects need for UPVC window specifications.",
        "faqs": [
            (
                "What should architects specify in tender documents?",
                "Profile series and brand, hardware brand and grade, glass U-value and SHGC, wind load class, installation method, sealing specification, and warranty terms. Vague 'UPVC window' invites lowest bidder degradation.",
            ),
            (
                "CAD details and sections available?",
                "Reputable fabricators provide typical details — jamb, sill, head, restraint fixing. Project-specific sections for non-standard wall build-ups on request.",
            ),
            (
                "Integration with RCC frame versus brick reveal?",
                "Different packer and fix strategies — specify anchor type and frequency. Post-construction reveal tolerance ±5 mm typical expectation.",
            ),
            (
                "Thermal bridging at sill?",
                "UPVC thermally outperforms aluminium without break; still detail sill insulation and avoid aluminium sub-sill in cold-sensitive designs — less critical in Odisha but affects condensation.",
            ),
            (
                "Custom RAL colours on large projects?",
                "Lamination colour matching possible with MOQ and extended lead — confirm before facade sign-off. Sample panel approval standard practice.",
            ),
            (
                "Performance mock-up testing?",
                "Large commercial may warrant water spray and operability mock-up before bulk — residential rare unless ultra-premium or litigation-sensitive.",
            ),
        ],
    },
    {
        "slug": "builders",
        "title": "Builder and Developer FAQs",
        "tags": ["builder", "developer", "project", "bulk"],
        "audience": "sales",
        "summary": "UPVC window supply for residential and commercial builders in Odisha.",
        "faqs": [
            (
                "Bulk pricing versus retail homeowner rates?",
                "20–35% lower on 50+ identical openings possible — depends on spec standardization and payment terms. Builder grade may use simpler hardware — disclose to buyers.",
            ),
            (
                "Phased delivery to construction site?",
                "Floor-wise delivery reduces theft and damage — coordinate tower crane lift. Storage on site needs covered area — direct sun on stacked frames warps gaskets.",
            ),
            (
                "Builder warranty versus manufacturer warranty?",
                "Pass-through manufacturer warranty plus builder workmanship period — clarify in buyer agreement who to call for leak in year one.",
            ),
            (
                "Standardizing openings across project?",
                "Fewer unique sizes lowers cost and speed — architectural coordination early saves fabrication waste. Module sizes matching brick course helps.",
            ),
            (
                "Replacement of defective units during construction?",
                "Batch defect rate should be under 2% — replacement SLA in supply contract. Do not install known defective unit 'to save time'.",
            ),
            (
                "GST and invoicing for builder contracts?",
                "Material versus works contract tax treatment differs — builder finance team should align with fabricator billing structure.",
            ),
        ],
    },
    {
        "slug": "service-requests",
        "title": "Service Request FAQs",
        "tags": ["service", "support", "complaint", "contact"],
        "audience": "homeowner",
        "summary": "How to request service, support, and follow-up for LIPU windows.",
        "faqs": [
            (
                "How do I log a service request after installation?",
                "Use the support form with invoice number, opening photos, and issue description. Include video of leak path if water issue — speeds diagnosis. Response typically 24–48 business hours in Bhubaneswar area.",
            ),
            (
                "What information speeds up service visit?",
                "Installation date, product type per room, when problem started, and monsoon correlation. Serial labels on frame if visible.",
            ),
            (
                "Is service chargeable under warranty?",
                "Manufacturing defect repair free — travel may apply for outstation. User damage, post-warranty wear, or civil-related leaks may be chargeable — quote before work.",
            ),
            (
                "Can I request annual maintenance visit?",
                "Yes — annual PM visit adjusts hardware, clears drainage, inspects gaskets. Cheaper than emergency monsoon leak call.",
            ),
            (
                "Escalation if first visit does not fix leak?",
                "Request senior technician revisit with different diagnosis approach. Document each visit in writing for warranty escalation chain.",
            ),
            (
                "Service coverage outside Bhubaneswar?",
                "Cuttack and Puri regular coverage; deeper Odisha districts by appointment — may add travel day. Coastal sites schedule around weather.",
            ),
        ],
    },
]

# ---------------------------------------------------------------------------
# Catalog products (10)
# ---------------------------------------------------------------------------

CATALOG_PRODUCTS: list[dict] = [
    {
        "slug": "sliding-windows",
        "title": "UPVC Sliding Windows",
        "tags": ["sliding", "window", "apartment", "balcony"],
        "products": ["horizon-sliding"],
        "audience": "homeowner",
        "summary": "Multi-track sliding UPVC windows for balconies and wide openings.",
        "sections": {
            "Description": (
                "UPVC sliding windows use horizontal sashes on rollers within a frame track. "
                "They dominate Bhubaneswar apartment balconies because they save interior space and "
                "offer wide glass spans. Typical profiles are 70 mm multi-chamber with steel reinforcement."
            ),
            "Best use cases": (
                "Balcony openings, living-to-sit-out connections, rooms where outward or inward swing "
                "is impractical, and any opening wider than 5 ft where casement would need multiple sashes."
            ),
            "Advantages": (
                "Unobstructed views, smooth operation when rollers are quality, no swing clearance needed, "
                "good for furniture-heavy rooms. Two-track systems seal adequately for most inland apartments."
            ),
            "Limitations": (
                "Acoustic seal inferior to casement unless premium gaskets and glass specified. "
                "Tracks collect dust — needs cleaning. Single-point locks on budget systems are weak."
            ),
            "Recommended glass": (
                "Double glazed for west and road exposure; laminated acoustic for NH-facing bedrooms converted to slider. "
                "Toughened mandatory per size rules."
            ),
            "Recommended hardware": (
                "Stainless or coastal-grade rollers, anti-lift blocks, dual-point lock minimum, branded roller carriers rated for sash weight."
            ),
            "Maintenance": (
                "Vacuum tracks monthly, clear weep holes before monsoon, replace rollers every 8–12 years. "
                "Silicone spray on lock mechanism annually."
            ),
            "Odisha suitability": (
                "Excellent for Patia, Nayapalli, and Khandagiri towers when drainage is maintained. "
                "Coastal Puri installs need monthly salt rinse and upgraded hardware pack."
            ),
        },
    },
    {
        "slug": "casement-windows",
        "title": "UPVC Casement Windows",
        "tags": ["casement", "window", "bedroom", "sealing"],
        "products": ["atelier-casement"],
        "audience": "homeowner",
        "summary": "Side-hinged casement windows for maximum seal and ventilation control.",
        "sections": {
            "Description": (
                "Casement windows hinge at side and open inward (typical in India) or outward. "
                "The sash compresses against frame gaskets when locked, making them the preferred choice "
                "for noise-sensitive and AC-cooled rooms in Odisha."
            ),
            "Best use cases": (
                "Bedrooms, study rooms, road-facing openings, kitchens needing strong seal when AC runs, "
                "and any room where full sash opening aids cross-ventilation."
            ),
            "Advantages": (
                "Best air and water seal among operable types, excellent with multi-point locks, "
                "full opening for cleaning inner and outer glass on reachable floors, strong acoustic performance with right glass."
            ),
            "Limitations": (
                "Inward swing needs clearance — conflicts with beds and curtains. "
                "Not ideal for very wide single sashes without heavy hinges. User error leaving open in squalls causes ingress."
            ),
            "Recommended glass": (
                "Laminated acoustic double glazed for traffic-facing; standard double glazed elsewhere; "
                "frosted toughened for bathrooms."
            ),
            "Recommended hardware": (
                "Espagnolette multi-point lock, branded friction stay, three hinges on tall sashes, "
                "optional restrictor for child safety."
            ),
            "Maintenance": (
                "Hinge adjustment every few years, check lock point alignment, clean gasket contact faces. "
                "Replace friction stay if sash drops or slips in wind."
            ),
            "Odisha suitability": (
                "Ideal for Cuttack lane-facing homes and Bhubaneswar bedrooms near busy roads. "
                "Handles humidity well; avoid cheap hinges that corrode in coastal belt."
            ),
        },
    },
    {
        "slug": "fixed-windows",
        "title": "UPVC Fixed Windows",
        "tags": ["fixed", "picture", "non-operable", "glazing"],
        "products": ["skyline-fixed"],
        "audience": "homeowner",
        "summary": "Non-operable fixed UPVC glazing for light, view, and combination windows.",
        "sections": {
            "Description": (
                "Fixed windows have no operable sash — glass is permanently glazed into the frame. "
                "They appear in stairwells, highlight clerestories, and as centre panels in combination assemblies."
            ),
            "Best use cases": (
                "Areas needing light without ventilation, large view walls with separate ventilators, "
                "top lights above doors, and cost-sensitive spans where operable function is not needed."
            ),
            "Advantages": (
                "Lowest cost per sq ft of glazing, no moving-part failure, best theoretical seal, "
                "clean sightlines for modern facades."
            ),
            "Limitations": (
                "No ventilation, exterior cleaning needs access, cannot retrofit operation without replacement. "
                "Large fixed panes need correct glass spec for wind load."
            ),
            "Recommended glass": (
                "Toughened or laminated per span and height; double glazed on exposed facades; "
                "solar control on west-facing fixed panels."
            ),
            "Recommended hardware": (
                "Glazing beads and structural silicone where engineered; no operable hardware except adjacent units."
            ),
            "Maintenance": (
                "Glass cleaning only — inspect sealant joints every 3–5 years on large commercial fixed panels."
            ),
            "Odisha suitability": (
                "Common in Bhubaneswar duplex stairwells and villa double-height zones. "
                "Ensure cyclone-rated glass thickness on upper-floor large spans."
            ),
        },
    },
    {
        "slug": "combination-windows",
        "title": "UPVC Combination Windows",
        "tags": ["combination", "mixed", "fixed", "casement"],
        "products": ["horizon-sliding", "atelier-casement"],
        "audience": "homeowner",
        "summary": "Mixed fixed and operable UPVC assemblies for wide openings.",
        "sections": {
            "Description": (
                "Combination windows merge fixed and operable panels — typically fixed centre with casement or sliding flanks, "
                "or fixed transom over operable sash. One frame system gives unified appearance."
            ),
            "Best use cases": (
                "Wide living room openings, master bedroom views with side ventilation, "
                "facades needing large glass with minimal operable percentage."
            ),
            "Advantages": (
                "Balances view, cost, and ventilation; single colour and profile match; "
                "designer flexibility without multiple separate frames."
            ),
            "Limitations": (
                "More complex fabrication — alignment critical at junctions. "
                "Leak risk at meeting mullions if not fabricated precisely."
            ),
            "Recommended glass": (
                "Match performance to each panel exposure — do not use single glass on fixed west panel "
                "while operable has double; thermal mismatch causes condensation patterns."
            ),
            "Recommended hardware": (
                "Operable sections get full multi-point spec; mullion reinforcement steel per span table."
            ),
            "Maintenance": (
                "Service operable portions on schedule; inspect mullion silicone joints at pre-monsoon check."
            ),
            "Odisha suitability": (
                "Popular in Nayapalli and Chandrasekharpur villas and large apartments. "
                "Design operable percentage for cross-vent during humid months."
            ),
        },
    },
    {
        "slug": "french-windows",
        "title": "UPVC French Windows",
        "tags": ["french", "window", "balcony", "paired"],
        "products": ["garden-portal"],
        "audience": "homeowner",
        "summary": "Paired casement French windows for garden and balcony access.",
        "sections": {
            "Description": (
                "French windows are paired casement sashes, often full or near-full height, opening to balcony or garden. "
                "Both sashes may be operable or one active with one passive leaf."
            ),
            "Best use cases": (
                "Ground-floor villa living to lawn, first-floor terrace access where allowed, "
                "premium apartments wanting door-like opening without full sliding door cost."
            ),
            "Advantages": (
                "Elegant symmetrical look, strong sealing when multi-point locked, good for natural light and occasional full opening."
            ),
            "Limitations": (
                "Meeting stile alignment sensitive; sill detail critical for water; "
                "low sill needs child safety measures; both sashes open into room on inward design."
            ),
            "Recommended glass": (
                "Laminated double glazed for safety and comfort; solar control on west-facing pairs."
            ),
            "Recommended hardware": (
                "Full espagnolette on active leaf, shoot bolts on passive, heavy hinges, threshold drain."
            ),
            "Maintenance": (
                "Adjust meeting stile annually; lubricate locking points; check threshold drain before monsoon."
            ),
            "Odisha suitability": (
                "Common in Bhubaneswar villa townships and Puri holiday homes. "
                "Coastal installs need stainless meeting stile hardware."
            ),
        },
    },
    {
        "slug": "sliding-doors",
        "title": "UPVC Sliding Doors",
        "tags": ["sliding", "door", "balcony", "terrace"],
        "products": ["horizon-sliding"],
        "audience": "homeowner",
        "summary": "Walk-through sliding doors for balconies and indoor-outdoor living.",
        "sections": {
            "Description": (
                "Sliding doors use full-height panels on heavy-duty tracks for human traffic to balconies and terraces. "
                "Panel weights exceed windows — roller and profile specification must match."
            ),
            "Best use cases": (
                "Main balcony access from living room, ground-floor villa patio doors, "
                "wide openings where swing doors are impractical."
            ),
            "Advantages": (
                "Wide clear opening, no swing radius, modern aesthetic, pairs with fixed sidelights."
            ),
            "Limitations": (
                "Heavier operation than windows; track must stay clean; security needs anti-lift and good locks; "
                "thermal seal slightly below casement door."
            ),
            "Recommended glass": (
                "Toughened double glazed minimum; laminated for ground floor and large spans."
            ),
            "Recommended hardware": (
                "Heavy-duty rollers, multi-point lock, anti-lift, optional soft-close on premium systems."
            ),
            "Maintenance": (
                "Weekly track vacuum if dusty location; roller replacement planned at year 10; "
                "check lock engagement after monsoon."
            ),
            "Odisha suitability": (
                "Standard in Bhubaneswar premium apartments; ensure sill slope and drain for monsoon squalls."
            ),
        },
    },
    {
        "slug": "french-doors",
        "title": "UPVC French Doors",
        "tags": ["french", "door", "entrance", "paired"],
        "products": ["grand-entrance"],
        "audience": "homeowner",
        "summary": "Double French doors for terrace, garden, and premium room exits.",
        "sections": {
            "Description": (
                "French doors are paired hinged doors meeting at centre — distinct from French windows mainly by "
                "traffic-rated threshold and heavier duty hardware for frequent walk-through use."
            ),
            "Best use cases": (
                "Villa living to patio, master bedroom to private terrace, internal room dividers with glass visibility."
            ),
            "Advantages": (
                "Classic appearance, tight seal when locked, full opening width when both leaves open."
            ),
            "Limitations": (
                "Swing space needed; meeting stile maintenance; not for highest-traffic commercial entries without robust spec."
            ),
            "Recommended glass": (
                "Laminated toughened double glazed for safety and impact resistance."
            ),
            "Recommended hardware": (
                "Commercial-grade multi-point, three hinges per leaf on tall doors, adjustable threshold."
            ),
            "Maintenance": (
                "Floor-level threshold cleaning; hinge and lock adjustment under heavy use annually."
            ),
            "Odisha suitability": (
                "Villa and farmhouse projects around Bhubaneswar outskirts; threshold drainage essential in monsoon."
            ),
        },
    },
    {
        "slug": "lift-and-slide-doors",
        "title": "Lift and Slide Doors",
        "tags": ["lift-slide", "door", "premium", "large-span"],
        "products": ["horizon-sliding"],
        "audience": "homeowner",
        "summary": "Premium lift-and-slide systems for heavy panels and superior sealing.",
        "sections": {
            "Description": (
                "Lift-and-slide doors raise the panel slightly before rolling, reducing friction and improving seal compression when lowered. "
                "Used for large heavy glass panels in premium villas."
            ),
            "Best use cases": (
                "Large villa openings 10 ft+, heavy triple or laminated glass panels, "
                "homeowners wanting slider aesthetics with near-casement seal."
            ),
            "Advantages": (
                "Smooth operation on heavy panels, better weather seal than standard slider, "
                "suitable for wider spans with less effort."
            ),
            "Limitations": (
                "Higher cost, specialist hardware, user must operate handle sequence correctly — forced sliding damages mechanism."
            ),
            "Recommended glass": (
                "Double or triple laminated per span engineering; low-E on sun-facing facades."
            ),
            "Recommended hardware": (
                "System-specific lift-slide carriage, multi-point lock, premium rollers — must stay within system weight limits."
            ),
            "Maintenance": (
                "Annual professional adjustment; keep track pristine; do not force panel if lift mechanism fails."
            ),
            "Odisha suitability": (
                "Niche premium market in Bhubaneswar and Puri villa segment; justify cost with large west-facing openings."
            ),
        },
    },
    {
        "slug": "balcony-enclosures",
        "title": "UPVC Balcony Enclosures",
        "tags": ["balcony", "enclosure", "weather", "extended-living"],
        "products": ["horizon-sliding"],
        "audience": "homeowner",
        "summary": "Full or partial balcony glazing systems for extra usable space.",
        "sections": {
            "Description": (
                "Balcony enclosures wrap the balcony with UPVC framing and glass — sliding, fixed, or combination — "
                "creating semi-interior space protected from rain and dust."
            ),
            "Best use cases": (
                "Apartment utility extension, home office nook, monsoon-safe drying area, "
                "noise buffer on road-facing balconies."
            ),
            "Advantages": (
                "Extra usable sq ft, cleaner balcony, reduced dust on adjacent rooms, optional acoustic benefit."
            ),
            "Limitations": (
                "RWA approval often required; heat buildup if poorly ventilated; not a structural room — load limits apply."
            ),
            "Recommended glass": (
                "Operable sections with clear double glazed; fixed with solar control if one side fully exposed."
            ),
            "Recommended hardware": (
                "Sliding door grade rollers on access panel; mesh vent panels recommended."
            ),
            "Maintenance": (
                "Ventilate regularly; clean tracks; check floor track level after building settlement."
            ),
            "Odisha suitability": (
                "High demand in Bhubaneswar apartments; plan cross-vent to handle April–June heat before monsoon."
            ),
        },
    },
    {
        "slug": "ventilators",
        "title": "UPVC Ventilators",
        "tags": ["ventilator", "top-hung", "bathroom", "kitchen"],
        "products": ["atelier-casement"],
        "audience": "homeowner",
        "summary": "Small top-hung and side ventilators for airflow in wet and service areas.",
        "sections": {
            "Description": (
                "Ventilators are small operable units — top-hung, bottom-hung, or side-hung — for bathrooms, kitchens, "
                "and above larger fixed panels. They provide code-compliant ventilation without full-size window cost."
            ),
            "Best use cases": (
                "Bathroom exhaust complement, kitchen steam relief, fixed window topping, "
                "stairwell high vent, toilet in apartment core without external wall window."
            ),
            "Advantages": (
                "Low cost, rain-safe top-hung opening angle, pairs with exhaust fan, reduces mold risk in humid Odisha bathrooms."
            ),
            "Limitations": (
                "Limited airflow volume; not substitute for full window in habitable bedroom; "
                "top-hung cleaning needs reach."
            ),
            "Recommended glass": (
                "Frosted toughened for privacy; clear for high clerestory; small size keeps cost low."
            ),
            "Recommended hardware": (
                "Top-hung friction stay with limit stops, small multi-point or cam lock, optional mesh."
            ),
            "Maintenance": (
                "Minimal — hinge lubrication, gasket check, fan coordination for moisture control."
            ),
            "Odisha suitability": (
                "Essential in Bhubaneswar apartments where bathrooms lack direct window — combine with exhaust for monsoon humidity."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# Odisha climate docs (7)
# ---------------------------------------------------------------------------

ODISHA_CLIMATE: list[dict] = [
    {
        "slug": "summer-heat",
        "title": "UPVC Windows and Odisha Summer Heat",
        "tags": ["summer", "heat", "solar", "cooling"],
        "audience": "homeowner",
        "summary": "Managing extreme summer heat through glazing and frame choices in Bhubaneswar.",
        "sections": {
            "Overview": (
                "Odisha summers from March through June push daytime temperatures above 40°C in Bhubaneswar with intense west-facing solar gain. "
                "Windows are the weakest thermal envelope element — more heat enters through glass than walls per square foot."
            ),
            "Frame considerations": (
                "UPVC multi-chamber profiles resist heat conduction better than plain aluminium. White and light colours reduce frame surface temperature slightly. "
                "Quality profiles use UV stabilizers to prevent degradation — critical for west facades."
            ),
            "Glazing strategy": (
                "Double glazed units with solar control outer pane — tinted, reflective, or low-E — cut radiant heat. "
                "Prioritize west and south-west rooms first. External shading where architecturally possible beats any glass-only solution."
            ),
            "Practical tips": (
                "Close reflective curtains during peak sun even with good glass. Run AC with windows sealed — cracked open window destroys efficiency. "
                "Ventilate early morning before heat builds, then seal for the day."
            ),
        },
    },
    {
        "slug": "humidity",
        "title": "Humidity and UPVC Performance in Odisha",
        "tags": ["humidity", "condensation", "mold", "monsoon"],
        "audience": "homeowner",
        "summary": "How coastal humidity affects windows and indoor comfort year-round.",
        "sections": {
            "Overview": (
                "Bhubaneswar and Cuttack maintain high humidity especially pre-monsoon and during monsoon. "
                "UPVC does not rot like wood, but humidity affects condensation, mold on curtains, and hardware corrosion if wrong grade."
            ),
            "Condensation management": (
                "Interior glass condensation when cold AC meets humid air is common — wipe surfaces, increase airflow briefly, "
                "or adjust AC temperature slightly. Between-pane fog means failed DGU seal — replace unit."
            ),
            "Ventilation balance": (
                "Sealed homes need controlled vent periods — mesh ventilators help without full rain entry. "
                "Bathrooms need exhaust fans plus ventilator — UPVC alone does not remove moisture."
            ),
            "Hardware in humidity": (
                "Use stainless or coated hardware; lubricate hinges lightly; avoid water pooling in tracks that breeds mold and corrodes reinforcement."
            ),
        },
    },
    {
        "slug": "monsoon",
        "title": "Monsoon Performance Guide for UPVC Windows",
        "tags": ["monsoon", "rain", "drainage", "sealing"],
        "audience": "homeowner",
        "summary": "Design and maintenance for Odisha monsoon June through September.",
        "sections": {
            "Overview": (
                "Odisha monsoon brings sustained rain and squalls with wind-driven water. "
                "Proper UPVC systems manage water through designed drainage paths — not by hoping seals block all water indefinitely."
            ),
            "Design essentials": (
                "Sloped sills, weep holes, overlapping profiles, and pressure-equalized tracks. "
                "Casement compression seals; slider drainage channels cleared monthly in monsoon."
            ),
            "Installation factors": (
                "External sealant continuity, foam fill without voids, and no blocked weep holes during painting. "
                "Many leaks are installation and civil sill issues, not profile brand failure."
            ),
            "Homeowner checklist": (
                "May: clear drains, test with hose, adjust rollers. During monsoon: keep closed in squalls, open in dry breaks. "
                "After monsoon: inspect gaskets and silicone, schedule service if any stain marks appeared on inner sill."
            ),
        },
    },
    {
        "slug": "cyclone-resistance",
        "title": "Cyclone Resistance for UPVC Installations",
        "tags": ["cyclone", "wind", "fani", "safety"],
        "audience": "homeowner",
        "summary": "Wind load, anchoring, and glass choice for cyclone-prone Odisha.",
        "sections": {
            "Overview": (
                "Odisha's cyclone history — including Fani's impact on Bhubaneswar — changed buyer expectations. "
                "Windows must stay closed and locked during storms; design for pressure and debris risk."
            ),
            "Anchoring": (
                "Fix frames into structural RCC with appropriate screw frequency — not brittle brick alone. "
                "Cyclone clips where specified. Large openings need engineered fix patterns."
            ),
            "Glass selection": (
                "Laminated glass reduces fall-through if broken by debris. Toughened required by size. "
                "Do not use non-toughened large fixed panels on upper floors."
            ),
            "User protocol": (
                "Close and lock all openings when cyclone warning issued. Remove loose balcony items. "
                "Temporary plywood boarding for ground floor extreme exposure. No window survives direct major debris impact — plan accordingly."
            ),
        },
    },
    {
        "slug": "coastal-salt-air",
        "title": "Coastal Salt Air and UPVC Systems",
        "tags": ["coastal", "salt", "puri", "corrosion"],
        "audience": "homeowner",
        "summary": "Protecting windows in Puri, Konark, Paradeep, and sea-facing properties.",
        "sections": {
            "Overview": (
                "Salt aerosol within kilometres of Odisha coast accelerates metal corrosion on hinges, screws, and rollers. "
                "UPVC profiles resist salt; hardware is the failure point on budget installs."
            ),
            "Specification": (
                "Coastal hardware grade stainless fasteners, rinsed tracks monthly, laminated glass for windborne sand and debris. "
                "Extra drainage capacity for combined rain and spray."
            ),
            "Maintenance schedule": (
                "Monthly fresh water rinse exterior, quarterly deep clean and lube, post-monsoon inspection mandatory. "
                "Replace any rusted screw immediately — rust spreads misalignment."
            ),
            "Inland note": (
                "Bhubaneswar city is inland enough for standard hardware though humidity still high. "
                "Do not downgrade coastal spec if property is within 5 km of high tide line."
            ),
        },
    },
    {
        "slug": "energy-efficiency",
        "title": "Energy Efficiency in Odisha Homes",
        "tags": ["energy", "ac", "u-value", "efficiency"],
        "audience": "homeowner",
        "summary": "Reducing cooling energy through window upgrades in hot-humid climate.",
        "sections": {
            "Overview": (
                "Cooling dominates residential energy in Odisha. Windows affect both heat gain and air infiltration — "
                "leaky old windows can add 20%+ to AC load on affected rooms."
            ),
            "Metrics": (
                "Look for U-value (lower better) and SHGC matched to orientation — low SHGC on west, moderate on north. "
                "Double glazing baseline for AC-cooled rooms."
            ),
            "Upgrade path": (
                "Phase one: west and road-facing rooms. Phase two: remaining bedrooms. "
                "Seal AC room doors and windows together — weak point anywhere wastes upgrade."
            ),
            "Payback": (
                "Heavy AC users see 5–10 year energy payback on full upgrade; comfort and noise benefits immediate. "
                "Commercial tariffs pay back faster than residential slab rates."
            ),
        },
    },
    {
        "slug": "soundproofing",
        "title": "Soundproofing in Urban Odisha",
        "tags": ["noise", "acoustic", "traffic", "urban"],
        "audience": "homeowner",
        "summary": "Traffic and urban noise mitigation for Bhubaneswar and Cuttack homes.",
        "sections": {
            "Overview": (
                "Growing traffic on NH-16, city arterial roads, and dense lane housing in Old Bhubaneswar and Cuttack "
                "drives demand for acoustic upgrades beyond basic double glazing."
            ),
            "System approach": (
                "Casement with multi-point lock plus laminated acoustic double glass beats slider with standard DGU. "
                "Seal wall penetrations and doors — window is only one path."
            ),
            "Realistic expectations": (
                "60–70% reduction in perceived traffic noise is achievable; silence is not. "
                "Horns and construction still audible at lower volume."
            ),
            "Measurement": (
                "Before-after dB readings help set expectations; visit reference installs near similar roads when possible."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# Pricing guide (4)
# ---------------------------------------------------------------------------

PRICING_GUIDE: list[dict] = [
    {
        "slug": "budget-tier",
        "title": "Budget Tier UPVC Windows",
        "tags": ["budget", "economy", "pricing", "value"],
        "audience": "homeowner",
        "summary": "What to expect from budget-tier UPVC windows in Odisha.",
        "sections": {
            "Typical scope": (
                "Standard 60–70 mm profiles, single or basic double glass, generic hardware, white colour only. "
                "Suitable for rental properties, rear-facing openings, or phased project cost control."
            ),
            "Price range": (
                "Bedroom casement 4×4 ft approximately ₹10,000–15,000 installed (2026 indicative). "
                "Basic slider slightly higher per sq ft for same size."
            ),
            "Trade-offs": (
                "Shorter hardware life, less acoustic performance, limited colour, may lack multi-point lock. "
                "Acceptable for low-exposure openings if installation quality remains good."
            ),
            "When to avoid": (
                "Road-facing bedrooms, west facades, coastal properties, and upper-floor cyclone exposure — "
                "false economy if failure within 3–5 years."
            ),
        },
    },
    {
        "slug": "mid-range-tier",
        "title": "Mid-Range UPVC Windows",
        "tags": ["mid-range", "standard", "pricing", "recommended"],
        "audience": "homeowner",
        "summary": "The recommended tier for most Bhubaneswar homeowners.",
        "sections": {
            "Typical scope": (
                "70 mm branded profile, double glazed standard, branded multi-point hardware, white and woodgrain options, "
                "proper drainage and installation protocol."
            ),
            "Price range": (
                "Bedroom casement 4×4 ft approximately ₹15,000–22,000; balcony slider 6×7 ft ₹25,000–40,000 installed."
            ),
            "Value proposition": (
                "Best balance of comfort, longevity, and cost for typical 3 BHK apartment or villa. "
                "Handles monsoon and AC load well when glass matched to exposure."
            ),
            "Upgrade hooks": (
                "Add acoustic laminated glass on road side, mesh, restrictors — incremental at order time."
            ),
        },
    },
    {
        "slug": "premium-tier",
        "title": "Premium UPVC Windows",
        "tags": ["premium", "luxury", "pricing", "high-end"],
        "audience": "homeowner",
        "summary": "Premium systems for villas, penthouse, and demanding exposures.",
        "sections": {
            "Typical scope": (
                "Premium profile series, acoustic or triple glazing options, lift-slide doors, imported hardware, "
                "custom colours, enhanced wind-load specification."
            ),
            "Price range": (
                "Casement with acoustic laminated DGU ₹22,000–35,000 per opening; large lift-slide ₹80,000–150,000+ depending on span."
            ),
            "When justified": (
                "NH-facing villa, Puri coastal frontage, home theatre room, penthouse wind load, architect-specified facade uniformity."
            ),
            "Expectations": (
                "Premium product with poor install fails like budget — insist on same installation team quality and written spec compliance."
            ),
        },
    },
    {
        "slug": "cost-factors",
        "title": "UPVC Window Cost Factors",
        "tags": ["cost", "factors", "quote", "pricing"],
        "audience": "homeowner",
        "summary": "What drives UPVC window pricing up or down.",
        "sections": {
            "Size and type": (
                "Larger openings cost more per unit but less per sq ft sometimes. Doors cost more than windows. "
                "Irregular shapes and arches add fabrication premium."
            ),
            "Glass": (
                "Single to double to laminated acoustic — glass often 30–40% of unit cost on premium spec. "
                "Tint, low-E, and thickness drive price."
            ),
            "Hardware and colour": (
                "Branded multi-point versus generic cam lock; non-white lamination MOQ and surcharge; mesh and restrictors additive."
            ),
            "Installation complexity": (
                "High-rise lift access, scaffolding, old frame removal difficulty, sill rebuild, remote site travel — all line items. "
                "Always survey before final quote."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# Hardware docs (3)
# ---------------------------------------------------------------------------

HARDWARE_DOCS: list[dict] = [
    {
        "slug": "multi-point-locking",
        "title": "Multi-Point Locking Systems",
        "tags": ["lock", "security", "multi-point", "hardware"],
        "audience": "homeowner",
        "summary": "How multi-point locks work and why they matter in Odisha.",
        "sections": {
            "Description": (
                "Multi-point locks engage several locking pins around the sash perimeter when the handle is lifted or turned. "
                "This pulls the sash evenly against gaskets — improving seal, security, and acoustic performance."
            ),
            "Benefits": (
                "Even compression reduces corner leaks common with single-point locks. "
                "Harder to force open. Essential for casement bedrooms and entry doors."
            ),
            "Maintenance": (
                "Keep locking points lubricated lightly; misaligned keeps cause handle stiffness — adjust strike plates professionally. "
                "Do not force handle if stiff — gearbox damage is expensive."
            ),
            "Specification tip": (
                "Ask how many locking points on your quote — two minimum, three or more on tall sashes. Brand name on contract."
            ),
        },
    },
    {
        "slug": "handles-hinges",
        "title": "Handles and Hinges",
        "tags": ["handles", "hinges", "hardware", "casement"],
        "audience": "homeowner",
        "summary": "Selecting and maintaining UPVC handles and hinges.",
        "sections": {
            "Handles": (
                "Inline versus crank-style; keyed versus non-keyed; colour matching profile. "
                "Handle drives lock gearbox — quality handle means smooth long operation."
            ),
            "Hinges": (
                "Two to four hinges per casement sash based on height and weight. "
                "Adjustable hinges correct minor sag; branded hinges rated for sash kg."
            ),
            "Coastal note": (
                "Stainless or special coating on coastal projects — standard zinc hinges rust and stain white frames."
            ),
            "Replacement": (
                "Handles and hinges are service parts — available long after install if brand documented."
            ),
        },
    },
    {
        "slug": "rollers-tracks",
        "title": "Rollers and Tracks for Sliding Systems",
        "tags": ["rollers", "track", "sliding", "hardware"],
        "audience": "homeowner",
        "summary": "Roller and track care for sliding windows and doors.",
        "sections": {
            "Rollers": (
                "Bear sash weight — underrated rollers flatten and cause misalignment leaks. "
                "Replace every 8–12 years as wear item."
            ),
            "Tracks": (
                "Must stay level and clean; building settlement may need roller height adjustment. "
                "Never seal weep holes in track."
            ),
            "Sliding doors versus windows": (
                "Doors use heavier roller sets — do not swap window rollers onto door panels. "
                "Lift-and-slide uses different carriage — system specific."
            ),
            "Dust and salt": (
                "Bhubaneswar road dust and Puri salt both accelerate track wear — clean monthly in exposed locations."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# Design inspiration (4)
# ---------------------------------------------------------------------------

DESIGN_INSPIRATION: list[dict] = [
    {
        "slug": "apartments",
        "title": "Window Design for Apartments",
        "tags": ["apartment", "design", "inspiration", "modern"],
        "audience": "homeowner",
        "summary": "Design ideas for UPVC windows in Bhubaneswar apartments.",
        "sections": {
            "Facade harmony": (
                "Match society exterior colour rules — usually white or beige exterior, woodgrain interior optional. "
                "Consistent sill height line across balcony improves tower appearance."
            ),
            "Living room": (
                "Sliding door plus sidelight fixed panel common; consider acoustic upgrade if road-facing. "
                "Avoid mixing too many grid patterns on one facade."
            ),
            "Bedrooms": (
                "Casement with mesh for road side; smaller ventilator in attached bath. "
                "Restrictors for upper floors with children."
            ),
            "Space tips": (
                "Sliding saves space versus casement in compact 3 BHK; use casement only where seal priority justifies swing clearance."
            ),
        },
    },
    {
        "slug": "villas",
        "title": "Window Design for Villas",
        "tags": ["villa", "design", "inspiration", "premium"],
        "audience": "homeowner",
        "summary": "Design approaches for independent houses and villa facades.",
        "sections": {
            "Indoor-outdoor": (
                "French or sliding doors to garden; consider lift-slide for premium living opening. "
                "Threshold detail merges tile indoor with landscape outdoor."
            ),
            "Double height": (
                "Fixed upper with operable lower maintains proportions; too much fixed glass overheats without shading."
            ),
            "Style mix": (
                "Woodgrain UPVC suits traditional villa; slim white profiles for contemporary cube designs. "
                "Dummy mullion grids add character without true divided lite cost."
            ),
            "Privacy": (
                "Street-facing: frosted lower fixed with clear upper; garden-facing: maximum clear glass."
            ),
        },
    },
    {
        "slug": "duplex",
        "title": "Window Design for Duplex Homes",
        "tags": ["duplex", "design", "stairwell", "multi-floor"],
        "audience": "homeowner",
        "summary": "Window planning for duplex and multi-floor independent homes.",
        "sections": {
            "Stairwell": (
                "Fixed toughened high panels bring light to centre — operable top vent for heat stack effect in summer."
            ),
            "Floor consistency": (
                "Same profile series both floors; vary operation type by room need not by floor randomly."
            ),
            "Upper floor wind": (
                "Stronger glass and fixings on top floor bedrooms; casement preferred for seal on exposed upper road face."
            ),
            "Balcony access": (
                "Upper floor balcony door with safe sill height and restrictor; ground floor may use wider French opening."
            ),
        },
    },
    {
        "slug": "commercial-facades",
        "title": "Commercial Facade Window Design",
        "tags": ["commercial", "facade", "design", "office"],
        "audience": "sales",
        "summary": "Glazing design for offices, retail, and commercial buildings in Odisha.",
        "sections": {
            "Curtain wall versus UPVC": (
                "UPVC suits operable zones and human-scale openings; aluminium curtain wall for full-height commercial spans. "
                "Hybrid facades common on Bhubaneswar office blocks."
            ),
            "Branding": (
                "Ground floor retail: maximum visibility clear glass; upper office: solar control to cut AC."
            ),
            "Maintenance access": (
                "Design operable units reachable for service; fixed-only high glass needs BMU or safe access plan."
            ),
            "Energy code alignment": (
                "Specify SHGC and U-value in tender — post-occupancy AC cost reflects glazing choices for 20 years."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# Service support (4)
# ---------------------------------------------------------------------------

SERVICE_SUPPORT: list[dict] = [
    {
        "slug": "complaint-handling",
        "title": "Complaint Handling Process",
        "tags": ["complaint", "support", "process", "service"],
        "audience": "homeowner",
        "summary": "How customer complaints are logged and resolved.",
        "sections": {
            "Logging": (
                "Submit support form with photos, video, invoice reference, and room location. "
                "Categorize as leak, operation, glass, or hardware for routing."
            ),
            "Response timeline": (
                "Acknowledgment within 24–48 business hours; site visit scheduled based on severity — active leak prioritized in monsoon."
            ),
            "Resolution": (
                "First visit diagnosis; parts ordered if needed; follow-up visit confirmed in writing. "
                "Warranty vs chargeable work explained before repair."
            ),
            "Escalation": (
                "Unresolved after two visits escalates to senior technician and management review."
            ),
        },
    },
    {
        "slug": "leakage-service",
        "title": "Leakage Investigation and Repair Service",
        "tags": ["leak", "repair", "service", "monsoon"],
        "audience": "homeowner",
        "summary": "Professional approach to diagnosing window water leaks.",
        "sections": {
            "Diagnosis": (
                "Technician traces water path — sill, meeting rail, wall junction, or overhead chhajja. "
                "Hose test reproduces leak when intermittent."
            ),
            "Common fixes": (
                "Roller adjustment, gasket replacement, external silicone renewal, drainage clearing, wall crack referral. "
                "Interior silicone alone rarely correct fix."
            ),
            "Warranty": (
                "Install-related leaks within workmanship period covered; civil or user-caused exclusions apply."
            ),
            "Prevention visit": (
                "Annual pre-monsoon check cheaper than emergency August leak call."
            ),
        },
    },
    {
        "slug": "hardware-service",
        "title": "Hardware Repair and Replacement Service",
        "tags": ["hardware", "repair", "rollers", "locks"],
        "audience": "homeowner",
        "summary": "Servicing locks, hinges, handles, and rollers.",
        "sections": {
            "Wear items": (
                "Rollers, handles, and lock cylinders have finite life — replacement normal at 8–15 years, not defect."
            ),
            "Brand matching": (
                "Best repair uses same hardware brand for gearbox compatibility. "
                "Mixed brands may fit poorly."
            ),
            "On-site capability": (
                "Most hardware swapped on site; glass unit replacement may need remeasure factory order."
            ),
            "Coastal": (
                "Puri and coastal clients should schedule hardware inspection quarterly — salt accelerates wear."
            ),
        },
    },
    {
        "slug": "post-installation-care",
        "title": "Post-Installation Care Guide",
        "tags": ["care", "maintenance", "handover", "support"],
        "audience": "homeowner",
        "summary": "Care instructions after UPVC window installation.",
        "sections": {
            "First 30 days": (
                "Normal slight settling may occur — report stiff operation promptly while warranty active. "
                "Do not paint over frames or seal weep holes during home finishing."
            ),
            "Cleaning": (
                "Mild soap, soft cloth, vacuum tracks. No abrasives or thinners on lamination."
            ),
            "Seasonal": (
                "May pre-monsoon service; post-monsoon inspection; coastal monthly rinse."
            ),
            "Documentation": (
                "Keep warranty card, invoice, and hardware brand record for future service orders."
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# Additional glass docs (3)
# ---------------------------------------------------------------------------

GLASS_DOCS: list[dict] = [
    {
        "slug": "toughened-safety",
        "title": "Toughened Safety Glass Guide",
        "tags": ["toughened", "safety", "tempered", "glass"],
        "audience": "homeowner",
        "summary": "When and why toughened glass is used in UPVC windows.",
        "sections": {
            "Requirements": (
                "Human impact risk areas, door glazing, low sill heights, and large panels require toughened glass per standards. "
                "Markings on glass verify tempering."
            ),
            "Behaviour": (
                "Breaks into small cubes reducing cut injury; stronger against impact but weak on edge chip. "
                "Cannot be field-cut after tempering."
            ),
            "With double glazing": (
                "One or both panes may be toughened in DGU — outer toughened common for large spans."
            ),
            "Odisha note": (
                "Cyclone debris risk makes laminated toughened preferable to plain toughened on exposed upper floors."
            ),
        },
    },
    {
        "slug": "reflective-and-tinted",
        "title": "Reflective and Tinted Glass for Heat Control",
        "tags": ["reflective", "tinted", "solar", "glass"],
        "audience": "homeowner",
        "summary": "Solar control glass options for west-facing Odisha homes.",
        "sections": {
            "Tinted glass": (
                "Bronze, grey, or green tint absorbs and reflects some solar energy; reduces glare. "
                "Moderate view change; good residential compromise."
            ),
            "Reflective glass": (
                "Strong mirror exterior daytime privacy and heat rejection; can look commercial if overused. "
                "Common on west facades of apartments."
            ),
            "Selection": (
                "Balance SHGC reduction with desired light level; sample viewing in showroom daylight helps decision."
            ),
            "Pairing": (
                "Tint or reflective outer pane with clear inner in DGU standard configuration."
            ),
        },
    },
    {
        "slug": "acoustic-laminated",
        "title": "Acoustic Laminated Glass",
        "tags": ["acoustic", "laminated", "noise", "glass"],
        "audience": "homeowner",
        "summary": "Laminated glass for traffic noise reduction in urban Odisha.",
        "sections": {
            "How it works": (
                "PVB interlayer dampens sound vibration between glass layers. "
                "Acoustic grade PVB performs better than standard safety laminate for noise."
            ),
            "Applications": (
                "Road-facing bedrooms in Bhubaneswar and Cuttack; NH-adjacent properties; home offices."
            ),
            "Combined systems": (
                "Best results with casement UPVC, multi-point lock, and asymmetric DGU — thicker outer, laminated inner."
            ),
            "Expectations": (
                "Significant reduction, not elimination — low frequency traffic rumble partially remains."
            ),
        },
    },
]


def generate_faqs() -> tuple[int, int]:
    file_count = 0
    question_count = 0
    for cat in FAQ_CATEGORIES:
        meta = {
            "title": cat["title"],
            "tags": cat["tags"],
            "audience": cat["audience"],
            "summary": cat["summary"],
        }
        if cat.get("products"):
            meta["products"] = cat["products"]
        body = faq_body(cat["title"], cat["faqs"])
        write_doc("faq", cat["slug"], meta, body)
        file_count += 1
        question_count += len(cat["faqs"])
    return file_count, question_count


def generate_catalog() -> int:
    count = 0
    for prod in CATALOG_PRODUCTS:
        meta = {
            "title": prod["title"],
            "tags": prod["tags"],
            "audience": prod["audience"],
            "summary": prod["summary"],
        }
        if prod.get("products"):
            meta["products"] = prod["products"]
        body = section_doc(prod["title"], prod["sections"])
        write_doc("catalog", prod["slug"], meta, body)
        count += 1
    return count


def generate_odisha_climate() -> int:
    count = 0
    for doc in ODISHA_CLIMATE:
        meta = {
            "title": doc["title"],
            "tags": doc["tags"],
            "audience": doc["audience"],
            "summary": doc["summary"],
        }
        body = section_doc(doc["title"], doc["sections"])
        write_doc("odisha-climate", doc["slug"], meta, body)
        count += 1
    return count


def generate_pricing_guide() -> int:
    count = 0
    for doc in PRICING_GUIDE:
        meta = {
            "title": doc["title"],
            "tags": doc["tags"],
            "audience": doc["audience"],
            "summary": doc["summary"],
        }
        body = section_doc(doc["title"], doc["sections"])
        write_doc("pricing-guide", doc["slug"], meta, body)
        count += 1
    return count


def generate_hardware() -> int:
    count = 0
    for doc in HARDWARE_DOCS:
        meta = {
            "title": doc["title"],
            "tags": doc["tags"],
            "audience": doc["audience"],
            "summary": doc["summary"],
        }
        body = section_doc(doc["title"], doc["sections"])
        write_doc("hardware", doc["slug"], meta, body)
        count += 1
    return count


def generate_design_inspiration() -> int:
    count = 0
    for doc in DESIGN_INSPIRATION:
        meta = {
            "title": doc["title"],
            "tags": doc["tags"],
            "audience": doc["audience"],
            "summary": doc["summary"],
        }
        body = section_doc(doc["title"], doc["sections"])
        write_doc("design-inspiration", doc["slug"], meta, body)
        count += 1
    return count


def generate_service_support() -> int:
    count = 0
    for doc in SERVICE_SUPPORT:
        meta = {
            "title": doc["title"],
            "tags": doc["tags"],
            "audience": doc["audience"],
            "summary": doc["summary"],
        }
        body = section_doc(doc["title"], doc["sections"])
        write_doc("service-support", doc["slug"], meta, body)
        count += 1
    return count


def generate_glass() -> int:
    count = 0
    for doc in GLASS_DOCS:
        meta = {
            "title": doc["title"],
            "tags": doc["tags"],
            "audience": doc["audience"],
            "summary": doc["summary"],
        }
        body = section_doc(doc["title"], doc["sections"])
        write_doc("glass", doc["slug"], meta, body)
        count += 1
    return count


def ensure_subfolders() -> None:
    for name in SUBFOLDERS:
        (BASE_DIR / name).mkdir(parents=True, exist_ok=True)


def main() -> None:
    ensure_subfolders()

    faq_files, faq_questions = generate_faqs()
    catalog_count = generate_catalog()
    climate_count = generate_odisha_climate()
    pricing_count = generate_pricing_guide()
    hardware_count = generate_hardware()
    design_count = generate_design_inspiration()
    service_count = generate_service_support()
    glass_count = generate_glass()

    total_files = (
        faq_files
        + catalog_count
        + climate_count
        + pricing_count
        + hardware_count
        + design_count
        + service_count
        + glass_count
    )

    print("LIPU Knowledge Base Generator")
    print("=" * 40)
    print(f"Output directory: {BASE_DIR}")
    print(f"FAQ files:        {faq_files}")
    print(f"FAQ questions:    {faq_questions}")
    print(f"Catalog docs:     {catalog_count}")
    print(f"Odisha climate:   {climate_count}")
    print(f"Pricing guide:    {pricing_count}")
    print(f"Hardware docs:    {hardware_count}")
    print(f"Design insp.:     {design_count}")
    print(f"Service/support:  {service_count}")
    print(f"Glass docs:       {glass_count}")
    print(f"Total new files:  {total_files}")
    print("=" * 40)
    if faq_questions < 228:
        print(f"WARNING: FAQ count {faq_questions} is below target 228")
    else:
        print(f"OK: FAQ count {faq_questions} meets target (228+)")


if __name__ == "__main__":
    main()

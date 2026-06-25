# LIPU Knowledge Base (RAG Source Documents)

Production markdown for the AI Consultant RAG pipeline. Written for **Bhubaneswar and Odisha** homeowners, builders, architects, and commercial clients.

## Folder structure

| Folder | Content | Files |
|--------|---------|-------|
| `faq/` | **228+ FAQs** across 38 customer concern categories | 38 |
| `catalog/` | Product profiles (sliding, casement, doors, ventilators, etc.) | 10 |
| `odisha-climate/` | Heat, humidity, monsoon, cyclone, coastal salt air | 7 |
| `glass/` | Glazing selection, acoustic, toughened, tinted | 6+ |
| `hardware/` | Locks, handles, rollers | 3 |
| `pricing-guide/` | Budget / mid / premium tiers, cost factors | 4 |
| `installation/` | Survey, prep, handover | 4+ |
| `warranty/` | Coverage, exclusions, claims | 4+ |
| `design-inspiration/` | Apartments, villas, duplex, commercial | 4 |
| `service-support/` | Leakage, hardware service, complaints | 4 |

## Regenerate content

```bash
cd lipu-platform/documents
python generate_kb.py
```

Regenerates FAQ, catalog, climate, pricing, hardware, design, service, and glass docs. Preserves manually edited warranty/installation files unless added to the generator.

## Document format

YAML frontmatter + Markdown body. See `SCHEMA.md` and `manifest.yaml`.

## Ingestion

```bash
cd lipu-platform/rag
.\.venv\Scripts\activate
python ingest.py --reset
python retrieve.py "Which window for a road-facing bedroom in Bhubaneswar?"
```

Vectors persist at `rag/data/chroma/` (ChromaDB, `BAAI/bge-small-en-v1.5`).

## FAQ categories (38)

Product Selection · UPVC vs Aluminium · UPVC vs Wood · Sliding/Casement/Fixed Windows · French Windows · Sliding Doors · Balcony Enclosures · Mosquito Mesh · Glass Selection · Double Glazing · Toughened Glass · Soundproofing · Heat Reduction · Energy Saving · Rain Protection · Monsoon · Coastal · Cyclone Safety · Security · Child Safety · Maintenance · Cleaning · Hardware · Warranty · Installation · Repairs · Leakage · Cost/Pricing · Apartments · Villas · Commercial · Schools · Hospitals · Architects · Builders · Service Requests

# Document metadata schema (RAG ingestion)

Version **1.0** — used by future ingestion jobs in `apps/api/app/ai/`.

## Frontmatter contract

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique ID, format `{category}/{slug}` |
| `title` | string | yes | Display title |
| `category` | enum | yes | Must match folder: `catalog`, `faq`, `glass`, `warranty`, `installation` |
| `tags` | string[] | yes | Free-form retrieval tags |
| `products` | string[] | no | Product slugs this doc applies to |
| `regions` | string[] | no | e.g. `bhubaneswar`, `cuttack`, `puri`, `odisha` |
| `version` | integer | yes | Increment on substantive edits |
| `updated` | date | yes | ISO 8601 date (`YYYY-MM-DD`) |
| `language` | string | yes | BCP 47, default `en` |
| `audience` | enum | yes | `homeowner`, `sales`, `installer` |
| `summary` | string | no | One-line description for search snippets |
| `related` | string[] | no | Other document `id` values |
| `priority` | integer | no | 1–10, higher = prefer in retrieval tie-break |
| `status` | enum | no | `draft` (skip ingestion) or `published` (default) |

## Chunking guidelines (future)

- Split on `##` and `###` headings where possible
- Keep chunks between **200–800** words
- Attach chunk metadata: `document_id`, `section_title`, `heading_level`, `chunk_index`
- Include product and region tags from parent document on every chunk

## Qdrant payload (planned)

```json
{
  "document_id": "catalog/horizon-sliding",
  "category": "catalog",
  "title": "Horizon Sliding System",
  "tags": ["sliding", "balcony"],
  "products": ["horizon-sliding"],
  "regions": ["odisha"],
  "section": "Monsoon performance",
  "chunk_index": 2
}
```

## Validation rules

1. `id` prefix must equal `category`
2. File path should be `{category}/{slug}.md` where slug matches `id` suffix
3. Reject files without frontmatter or with unknown `category`
4. Skip files with `status: draft`

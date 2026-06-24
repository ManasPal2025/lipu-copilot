# API Contract Specification

**Document Version:** 1.0  
**Format:** OpenAPI 3.0  
**Base URL:** `https://api.lipu.com/v1`  
**Status:** API Design Phase

---

## Table of Contents

1. [Authentication & Authorization](#authentication--authorization)
2. [Response Format](#response-format)
3. [Error Handling](#error-handling)
4. [Products API](#products-api)
5. [Orders API](#orders-api)
6. [Quotes API](#quotes-api)
7. [Customers API](#customers-api)
8. [AI Services API](#ai-services-api)
9. [Inventory API](#inventory-api)
10. [Analytics API](#analytics-api)
11. [WebSocket Events](#websocket-events)

---

## Authentication & Authorization

### JWT Token Structure

```
Header: Authorization: Bearer {jwt_token}

JWT Payload:
{
  "sub": "user_id",
  "org_id": "organization_id",
  "role": "admin|sales|customer|guest",
  "permissions": ["products:read", "orders:create", ...],
  "iat": 1688000000,
  "exp": 1688086400
}
```

### OAuth 2.0 (Clerk Integration)

```
POST /auth/callback
Content-Type: application/json

{
  "code": "clerk_auth_code",
  "state": "state_token"
}

Response:
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "expires_in": 86400,
  "token_type": "Bearer"
}
```

### Rate Limiting

```
Headers:
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1688000100

Limits:
- Public endpoints: 100 req/hour
- Authenticated endpoints: 1000 req/hour
- Admin endpoints: 5000 req/hour
```

---

## Response Format

### Success Response

```json
{
  "status": "success",
  "code": 200,
  "message": "Operation completed successfully",
  "data": {
    // Actual response payload
  },
  "meta": {
    "timestamp": "2026-06-24T10:30:00Z",
    "request_id": "req_abc123",
    "version": "1.0"
  }
}
```

### Paginated Response

```json
{
  "status": "success",
  "code": 200,
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_count": 150,
    "total_pages": 8,
    "has_next": true,
    "has_previous": false,
    "next_page": 2,
    "previous_page": null
  }
}
```

---

## Error Handling

### Error Response

```json
{
  "status": "error",
  "code": 400,
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Invalid request payload",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "timestamp": "2026-06-24T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### Error Codes

```
200: OK
201: Created
204: No Content
400: Bad Request
401: Unauthorized
403: Forbidden
404: Not Found
409: Conflict
429: Too Many Requests
500: Internal Server Error
503: Service Unavailable
```

---

## Products API

### GET /products

Retrieve product catalog with filtering.

```
GET /products?category=windows&search=sliding&page=1&limit=20&sort=name:asc

Query Parameters:
- category: string (optional) - Category slug
- search: string (optional) - Full-text search
- min_price: number (optional)
- max_price: number (optional)
- sort: string (optional) - Field and direction (name:asc, price:desc)
- page: integer (default: 1)
- limit: integer (default: 20, max: 100)

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "sku": "WND-SLIDE-001",
      "name": "Sliding Window - Premium",
      "slug": "sliding-window-premium",
      "description": "High-performance sliding window",
      "category": {
        "id": "uuid",
        "name": "Sliding Windows",
        "slug": "sliding-windows"
      },
      "pricing": {
        "base_price": 15000,
        "installation_cost": 2000,
        "currency": "INR"
      },
      "variants": {
        "colors": [
          {"name": "White", "hex": "#FFFFFF", "price_modifier": 0},
          {"name": "Black", "hex": "#000000", "price_modifier": 500}
        ],
        "glass": [
          {"name": "Clear", "price_modifier": 0},
          {"name": "Tinted", "price_modifier": 1000}
        ]
      },
      "specifications": {
        "default_width": 1200,
        "default_height": 800,
        "warranty_months": 60
      },
      "media": {
        "featured_image": "https://cdn.lipu.com/products/...",
        "gallery": [...],
        "video_url": "https://vimeo.com/..."
      },
      "seo": {
        "title": "Premium Sliding UPVC Window",
        "description": "...",
        "keywords": "..."
      },
      "is_bestseller": true,
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-06-24T10:30:00Z"
    }
  ],
  "pagination": {...}
}
```

### GET /products/:id

Get single product details.

```
GET /products/uuid

Response:
{
  "status": "success",
  "data": {
    // Product object with all details
    "related_products": [...]
  }
}
```

### GET /products/:id/quotes

Get quotes related to a product.

```
GET /products/uuid/quotes?days=30

Query Parameters:
- days: integer - Last N days

Response:
{
  "status": "success",
  "data": {
    "total_quotes": 45,
    "quotes_this_month": 12,
    "trend": "up"
  }
}
```

### POST /products (Admin Only)

Create new product.

```
POST /products
Content-Type: application/json

{
  "sku": "WND-CASE-001",
  "name": "Casement Window",
  "category_id": "uuid",
  "description": "...",
  "base_price": 12000,
  "installation_cost": 1500,
  "default_width": 1000,
  "default_height": 1200,
  "warranty_months": 60,
  "featured_image": "url",
  "gallery_images": ["url1", "url2"],
  "seo_title": "...",
  "seo_description": "...",
  "seo_keywords": "..."
}

Response: 201 Created
{
  "status": "success",
  "code": 201,
  "data": {
    "id": "uuid",
    ...
  }
}
```

### PUT /products/:id (Admin Only)

Update product.

```
PUT /products/uuid
Content-Type: application/json

{
  "name": "Updated name",
  "base_price": 13000,
  ...
}

Response:
{
  "status": "success",
  "data": {
    "id": "uuid",
    ...
  }
}
```

### DELETE /products/:id (Admin Only)

Soft delete product.

```
DELETE /products/uuid

Response: 204 No Content
```

### POST /products/:id/variants

Add product variant.

```
POST /products/uuid/variants
Content-Type: application/json

{
  "variant_type": "color",
  "variant_name": "Deep Black",
  "variant_value": "deep_black",
  "color_hex": "#1a1a1a",
  "price_modifier": 750,
  "image_url": "https://..."
}

Response: 201 Created
```

---

## Orders API

### POST /orders

Create new order.

```
POST /orders
Content-Type: application/json
Authorization: Bearer {token}

{
  "items": [
    {
      "product_id": "uuid",
      "quantity": 5,
      "selected_variants": {
        "color": "white",
        "glass": "tinted"
      },
      "custom_width": 1200,
      "custom_height": 1000
    }
  ],
  "billing_address": {
    "street": "123 Main St",
    "city": "Mumbai",
    "state": "MH",
    "zip": "400001",
    "country": "IN"
  },
  "shipping_address": {
    ...
  },
  "customer_notes": "Please deliver on weekends",
  "payment_method": "online"
}

Response: 201 Created
{
  "status": "success",
  "code": 201,
  "data": {
    "id": "uuid",
    "order_number": "ORD-2026-000123",
    "status": "pending",
    "items": [...],
    "subtotal": 60000,
    "tax_amount": 10800,
    "shipping_cost": 1000,
    "total_amount": 71800,
    "created_at": "2026-06-24T10:30:00Z"
  }
}
```

### GET /orders

Retrieve customer's orders.

```
GET /orders?status=confirmed&sort=created_at:desc&page=1&limit=10

Query Parameters:
- status: string (optional)
- product_id: uuid (optional) - Filter by product
- date_from: date (optional)
- date_to: date (optional)
- sort: string (default: created_at:desc)
- page: integer
- limit: integer

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "order_number": "ORD-2026-000123",
      "status": "confirmed",
      "total_amount": 71800,
      "items_count": 1,
      "estimated_completion_date": "2026-07-15",
      "created_at": "2026-06-24T10:30:00Z"
    }
  ],
  "pagination": {...}
}
```

### GET /orders/:id

Get order details.

```
GET /orders/uuid

Response:
{
  "status": "success",
  "data": {
    "id": "uuid",
    "order_number": "ORD-2026-000123",
    "status": "confirmed",
    "items": [
      {
        "id": "uuid",
        "product": {
          "id": "uuid",
          "name": "Sliding Window",
          "image": "..."
        },
        "quantity": 5,
        "unit_price": 15000,
        "total_price": 75000,
        "selected_variants": {...}
      }
    ],
    "billing_address": {...},
    "shipping_address": {...},
    "payment": {
      "method": "online",
      "status": "paid",
      "reference": "TXN-2026-123"
    },
    "tracking": {
      "number": "TRACK-123456",
      "courier": "FedEx",
      "status": "in_transit",
      "last_update": "2026-06-24T10:30:00Z"
    },
    "created_at": "2026-06-24T10:30:00Z"
  }
}
```

### PUT /orders/:id (Admin Only)

Update order status.

```
PUT /orders/uuid
Content-Type: application/json

{
  "status": "processing",
  "admin_notes": "Ready for dispatch"
}

Response:
{
  "status": "success",
  "data": {...}
}
```

### POST /orders/:id/cancel

Cancel order.

```
POST /orders/uuid/cancel
Content-Type: application/json

{
  "reason": "Customer request"
}

Response:
{
  "status": "success",
  "message": "Order cancelled successfully"
}
```

### POST /orders/:id/invoice

Generate invoice.

```
POST /orders/uuid/invoice

Response:
{
  "status": "success",
  "data": {
    "invoice_url": "https://...",
    "invoice_number": "INV-2026-123",
    "generated_at": "2026-06-24T10:30:00Z"
  }
}
```

---

## Quotes API

### POST /quotes

Request a quote.

```
POST /quotes
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Window and Door Quote - Mumbai Residence",
  "description": "Residential project at Bandra",
  "items": [
    {
      "product_id": "uuid",
      "quantity": 10,
      "selected_variants": {
        "color": "white",
        "glass": "tinted"
      }
    }
  ],
  "project_id": "uuid" (optional),
  "notes": "Need customization"
}

Response: 201 Created
{
  "status": "success",
  "code": 201,
  "data": {
    "id": "uuid",
    "quote_number": "QT-2026-000045",
    "status": "draft",
    "created_at": "2026-06-24T10:30:00Z"
  }
}
```

### GET /quotes

Retrieve customer's quotes.

```
GET /quotes?status=sent&sort=created_at:desc

Query Parameters:
- status: string (optional) - draft, sent, accepted, rejected, expired
- sort: string
- page: integer
- limit: integer

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "quote_number": "QT-2026-000045",
      "title": "Window and Door Quote",
      "status": "sent",
      "total_amount": 150000,
      "items_count": 10,
      "valid_until": "2026-07-24",
      "created_at": "2026-06-24T10:30:00Z"
    }
  ],
  "pagination": {...}
}
```

### GET /quotes/:id

Get quote details.

```
GET /quotes/uuid

Response:
{
  "status": "success",
  "data": {
    "id": "uuid",
    "quote_number": "QT-2026-000045",
    "title": "Window and Door Quote",
    "status": "sent",
    "items": [
      {
        "id": "uuid",
        "product": {...},
        "quantity": 10,
        "unit_price": 15000,
        "total_price": 150000
      }
    ],
    "subtotal": 150000,
    "tax": 27000,
    "total_amount": 177000,
    "valid_until": "2026-07-24",
    "terms_and_conditions": "...",
    "notes": "...",
    "created_at": "2026-06-24T10:30:00Z",
    "sent_at": "2026-06-24T11:00:00Z"
  }
}
```

### PUT /quotes/:id

Update quote (Admin only).

```
PUT /quotes/uuid
Content-Type: application/json

{
  "status": "accepted",
  "notes": "Approved by customer"
}
```

### POST /quotes/:id/accept

Customer accepts quote.

```
POST /quotes/uuid/accept
Content-Type: application/json

{
  "agreed_terms": true
}

Response:
{
  "status": "success",
  "message": "Quote accepted",
  "data": {
    "converted_to_order_id": "uuid",
    "order_number": "ORD-2026-000123"
  }
}
```

### POST /quotes/:id/send

Send quote to customer (Admin).

```
POST /quotes/uuid/send
Content-Type: application/json

{
  "email_message": "Please review the attached quote"
}

Response:
{
  "status": "success",
  "message": "Quote sent successfully"
}
```

---

## Customers API

### POST /customers

Register as customer or create new customer (Admin).

```
POST /customers
Content-Type: application/json
Authorization: Bearer {token}

{
  "user_id": "uuid" (only for admin),
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+91-9876543210",
  "customer_type": "residential",
  "company_name": "Doe Constructions" (if commercial),
  "primary_address": {
    "street": "123 Main St",
    "city": "Mumbai",
    "state": "MH",
    "zip": "400001",
    "country": "IN"
  },
  "communication_preference": "email",
  "source_of_lead": "website"
}

Response: 201 Created
```

### GET /customers

Get customer profile.

```
GET /customers/me

Response:
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user": {
      "id": "uuid",
      "email": "john@example.com",
      "name": "John Doe"
    },
    "customer_type": "residential",
    "phone": "+91-9876543210",
    "primary_address": {...},
    "status": "customer",
    "lifetime_value": 250000,
    "total_orders": 3,
    "last_interaction": "2026-06-20T10:30:00Z",
    "created_at": "2026-01-15T00:00:00Z"
  }
}
```

### PUT /customers/:id

Update customer profile.

```
PUT /customers/uuid
Content-Type: application/json

{
  "phone": "+91-9876543211",
  "communication_preference": "whatsapp",
  "primary_address": {...}
}
```

### GET /customers/:id/projects

Get customer's projects.

```
GET /customers/uuid/projects

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "project_name": "Bandra Residence",
      "location": "Mumbai, MH",
      "status": "in_progress",
      "estimated_windows": 12,
      "estimated_doors": 4,
      "estimated_value": 350000,
      "start_date": "2026-06-01",
      "estimated_completion": "2026-08-15"
    }
  ]
}
```

---

## AI Services API

### POST /ai/chat

Send message to AI assistant.

```
POST /ai/chat
Content-Type: application/json
Authorization: Bearer {token}

{
  "conversation_id": "uuid" (optional - for continuing conversation),
  "message": "What window would be best for a coastal area?",
  "conversation_context": {
    "topic": "sales_inquiry",
    "products_viewed": ["uuid1", "uuid2"]
  }
}

Response: 200 OK (with streaming)
{
  "status": "success",
  "data": {
    "conversation_id": "uuid",
    "assistant_message": "For coastal areas, I recommend our high-performance UPVC windows...",
    "references": [
      {
        "document_id": "uuid",
        "document_name": "Coastal Weather Installation Guide",
        "relevance": 0.95
      }
    ],
    "suggested_products": ["uuid1", "uuid2"],
    "processing_time_ms": 2350
  }
}
```

### WebSocket: /ai/chat/stream

Real-time streaming chat.

```
WebSocket wss://api.lipu.com/v1/ai/chat/stream

Message format:
{
  "type": "message",
  "conversation_id": "uuid",
  "message": "Your question here"
}

Stream response:
{
  "type": "stream",
  "chunk": "For coastal areas..."
}

{
  "type": "complete",
  "assistant_message": "...",
  "references": [...],
  "processing_time_ms": 2350
}
```

### POST /ai/quote-generator

Generate AI-powered quote.

```
POST /ai/quote-generator
Content-Type: application/json

{
  "window_width": 1200,
  "window_height": 1000,
  "window_type": "sliding",
  "glass_type": "tinted",
  "frame_color": "white",
  "quantity": 5,
  "location": "Mumbai",
  "project_type": "residential"
}

Response:
{
  "status": "success",
  "data": {
    "material_cost": 15000,
    "labour_cost": 3000,
    "installation_cost": 2000,
    "total_cost": 20000,
    "estimated_timeline_days": 7,
    "breakdown": {
      "frame": 8000,
      "glass": 5000,
      "hardware": 2000
    },
    "confidence_score": 0.92
  }
}
```

### POST /ai/house-visualization

Generate AI visualization of house with new windows.

```
POST /ai/house-visualization
Content-Type: multipart/form-data

- house_image: File (JPEG/PNG)
- product_id: uuid
- color: string
- glass_type: string
- style: string (sliding, casement, french)
- model: string (dall-e-3, flux, controlnet) [optional]

Response: 202 Accepted
{
  "status": "success",
  "code": 202,
  "data": {
    "generation_id": "uuid",
    "status": "processing",
    "estimated_completion_seconds": 30
  }
}
```

### GET /ai/house-visualization/:id

Poll for visualization result.

```
GET /ai/house-visualization/uuid

Response:
{
  "status": "success",
  "data": {
    "generation_id": "uuid",
    "status": "completed",
    "generated_images": [
      "https://cdn.lipu.com/visualizations/...",
      "https://cdn.lipu.com/visualizations/..."
    ],
    "processing_time_ms": 28500
  }
}
```

### POST /ai/design-consultant

Get AI design recommendations.

```
POST /ai/design-consultant
Content-Type: multipart/form-data

- house_image: File
- project_type: string (residential, commercial)
- location: string
- budget: number [optional]

Response:
{
  "status": "success",
  "data": {
    "recommended_styles": [
      {
        "style": "Modern",
        "reasoning": "Your minimalist interior design pairs well with clean lines...",
        "matching_products": ["uuid1", "uuid2"],
        "confidence": 0.95
      },
      {
        "style": "European",
        "reasoning": "...",
        "matching_products": [],
        "confidence": 0.78
      }
    ],
    "overall_recommendation": "Modern style (95% confidence)"
  }
}
```

### GET /ai/conversations

Get user's AI conversation history.

```
GET /ai/conversations?archived=false&limit=20&sort=created_at:desc

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "topic": "sales_inquiry",
      "preview": "What window would be best for coastal...",
      "message_count": 8,
      "created_at": "2026-06-24T10:30:00Z",
      "last_message_at": "2026-06-24T12:00:00Z"
    }
  ]
}
```

### GET /ai/conversations/:id

Get conversation messages.

```
GET /ai/conversations/uuid

Response:
{
  "status": "success",
  "data": {
    "id": "uuid",
    "messages": [
      {
        "id": "uuid",
        "role": "user",
        "content": "...",
        "timestamp": "2026-06-24T10:30:00Z"
      },
      {
        "id": "uuid",
        "role": "assistant",
        "content": "...",
        "references": [...],
        "timestamp": "2026-06-24T10:30:05Z"
      }
    ]
  }
}
```

---

## Inventory API

### GET /inventory

Get inventory summary (Admin).

```
GET /inventory?warehouse=warehouse1&sort=stock_status:desc&limit=50

Query Parameters:
- warehouse: string (optional)
- product_id: uuid (optional)
- status: string (optional) - in_stock, low_stock, out_of_stock
- sort: string
- page: integer
- limit: integer

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "product": {
        "id": "uuid",
        "name": "Sliding Window",
        "sku": "WND-SLIDE-001"
      },
      "warehouse": "Warehouse-1",
      "bin": "B-12-A",
      "quantity_on_hand": 150,
      "quantity_reserved": 30,
      "quantity_available": 120,
      "minimum_stock_level": 20,
      "stock_status": "in_stock",
      "reorder_quantity": 50,
      "last_received": "2026-06-20T00:00:00Z"
    }
  ],
  "pagination": {...}
}
```

### POST /inventory/adjust

Adjust inventory (Admin).

```
POST /inventory/adjust
Content-Type: application/json

{
  "inventory_stock_id": "uuid",
  "quantity_change": 10,
  "transaction_type": "correction",
  "reason": "Stock count correction",
  "reference_id": "uuid" (optional)
}

Response: 201 Created
```

### GET /inventory/low-stock

Get low stock alerts (Admin).

```
GET /inventory/low-stock

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "product": {...},
      "current_stock": 15,
      "minimum_level": 20,
      "reorder_quantity": 50,
      "days_until_stockout": 3,
      "suggested_action": "Reorder immediately"
    }
  ]
}
```

---

## Analytics API

### GET /analytics/dashboard

Admin analytics dashboard (Admin).

```
GET /analytics/dashboard?date_from=2026-06-01&date_to=2026-06-30

Response:
{
  "status": "success",
  "data": {
    "sales": {
      "total_revenue": 1500000,
      "order_count": 45,
      "average_order_value": 33333,
      "revenue_trend": "up 15%"
    },
    "leads": {
      "total_leads": 230,
      "new_leads": 45,
      "conversion_rate": 19.6,
      "lead_sources": {
        "website": 120,
        "referral": 60,
        "phone": 30,
        "event": 20
      }
    },
    "products": {
      "top_products": [
        {
          "id": "uuid",
          "name": "Sliding Window",
          "quantity_sold": 150,
          "revenue": 450000
        }
      ]
    },
    "customers": {
      "total_customers": 280,
      "repeat_customers": 85,
      "new_customers": 15,
      "average_lifetime_value": 58000
    },
    "ai_usage": {
      "total_conversations": 1250,
      "avg_messages_per_conversation": 4.2,
      "most_asked_topics": ["product_selection", "pricing", "warranty"]
    }
  }
}
```

### GET /analytics/leads

Lead analytics (Admin).

```
GET /analytics/leads?status=converted&source=website

Response:
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "source": "website",
      "interaction_type": "form_submit",
      "conversion_status": "converted",
      "time_to_conversion_hours": 48,
      "associated_customer": "uuid"
    }
  ]
}
```

### GET /analytics/sales

Sales analytics (Admin).

```
GET /analytics/sales?granularity=daily&date_from=2026-06-01&date_to=2026-06-30

Response:
{
  "status": "success",
  "data": {
    "daily_sales": [
      {
        "date": "2026-06-01",
        "revenue": 45000,
        "order_count": 3,
        "average_order_value": 15000
      }
    ],
    "charts": {
      "revenue_trend": "chart_data",
      "order_volume": "chart_data"
    }
  }
}
```

---

## WebSocket Events

### Connection

```
wss://api.lipu.com/v1/events

Headers:
Authorization: Bearer {jwt_token}
```

### Real-time Notifications

```
Event: order_status_updated
{
  "type": "order_status_updated",
  "order_id": "uuid",
  "old_status": "pending",
  "new_status": "confirmed",
  "timestamp": "2026-06-24T10:30:00Z"
}

Event: inventory_low_stock
{
  "type": "inventory_low_stock",
  "product_id": "uuid",
  "product_name": "Sliding Window",
  "current_stock": 15,
  "minimum_level": 20
}

Event: quote_created
{
  "type": "quote_created",
  "quote_id": "uuid",
  "customer_id": "uuid",
  "total_amount": 150000
}

Event: ai_visualization_ready
{
  "type": "ai_visualization_ready",
  "generation_id": "uuid",
  "images": ["url1", "url2"]
}
```

---

## Rate Limiting

### Quotas by Role

```
Guest (No Auth):
- 100 requests/hour
- Max 10 requests/minute

Customer:
- 1000 requests/hour
- Max 50 requests/minute

Admin/Sales:
- 5000 requests/hour
- Max 200 requests/minute

AI Services:
- 10000 tokens/day for standard users
- Unlimited for admin
```

---

## Versioning

### Current Version: v1

Breaking changes trigger new major version.
- `/v1/products`
- `/v2/products` (future)

### Deprecation Policy

- Deprecation notice: 60 days advance notification
- Support window: 6 months
- Removal: After 6 months

---

## Testing Endpoints

### Sandbox Mode

```
Headers:
X-Sandbox-Mode: true

Behavior:
- No charges
- No real email sending
- In-memory data
- Resets daily
```

---

## Next Steps

- [ ] Add request/response examples for each endpoint
- [ ] Create OpenAPI/Swagger YAML file
- [ ] Generate API documentation portal
- [ ] Create SDK/Client libraries (JavaScript, Python)
- [ ] Set up API testing framework (Postman, Insomnia)

---

**Document Status:** Ready for implementation  
**Last Updated:** 2026-06-24

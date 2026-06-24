# Database Schema Design

**Document Version:** 1.0  
**Database:** PostgreSQL 15+  
**ORM:** SQLAlchemy  
**Status:** Schema Design Phase

---

## Table of Contents

1. [Core Entities](#core-entities)
2. [Product Management](#product-management)
3. [Order Management](#order-management)
4. [Customer Management](#customer-management)
5. [Inventory Management](#inventory-management)
6. [AI & Documents](#ai--documents)
7. [Analytics & Audit](#analytics--audit)
8. [Indexing Strategy](#indexing-strategy)
9. [Constraints & Relationships](#constraints--relationships)
10. [Partitioning Strategy](#partitioning-strategy)

---

## Core Entities

### 1. Organizations (Multi-tenant ready)

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    logo_url VARCHAR(500),
    website_url VARCHAR(500),
    phone VARCHAR(20),
    email VARCHAR(255),
    address JSONB, -- {street, city, state, zip, country}
    founded_year INTEGER,
    industry VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, suspended
    settings JSONB DEFAULT '{}', -- Pricing rules, tax config, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_organizations_status ON organizations(status);
```

### 2. Users (Via Clerk, but stored locally)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    clerk_id VARCHAR(255) NOT NULL UNIQUE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(500),
    phone VARCHAR(20),
    role VARCHAR(50) NOT NULL, -- admin, sales, customer, guest
    permissions JSONB DEFAULT '[]', -- Specific permissions beyond role
    profile JSONB DEFAULT '{}', -- Additional user data
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, suspended
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE UNIQUE INDEX idx_users_clerk_email ON users(clerk_id, email);
CREATE INDEX idx_users_organization_role ON users(organization_id, role);
CREATE INDEX idx_users_status ON users(status);
```

---

## Product Management

### 3. Product Categories

```sql
CREATE TABLE product_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    parent_category_id UUID REFERENCES product_categories(id),
    icon_url VARCHAR(500),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    seo_title VARCHAR(255),
    seo_description VARCHAR(500),
    seo_keywords VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, slug)
);

CREATE INDEX idx_product_categories_parent ON product_categories(parent_category_id);
CREATE INDEX idx_product_categories_active ON product_categories(is_active);
```

### 4. Products (Main catalog)

```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    category_id UUID NOT NULL REFERENCES product_categories(id),
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    long_description TEXT,
    short_description VARCHAR(500),
    
    -- Pricing
    base_price DECIMAL(12, 2) NOT NULL,
    installation_cost DECIMAL(12, 2) DEFAULT 0,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    cost_price DECIMAL(12, 2), -- For admin visibility
    
    -- Physical properties
    default_width DECIMAL(10, 2), -- mm
    default_height DECIMAL(10, 2), -- mm
    default_depth DECIMAL(10, 2), -- mm
    weight_per_unit DECIMAL(10, 2), -- kg
    unit_of_measure VARCHAR(20) DEFAULT 'piece',
    
    -- Media & SEO
    featured_image_url VARCHAR(500),
    gallery_images JSONB DEFAULT '[]', -- Array of image URLs
    video_url VARCHAR(500),
    brochure_url VARCHAR(500),
    
    seo_title VARCHAR(255),
    seo_description VARCHAR(500),
    seo_keywords VARCHAR(500),
    search_text TSVECTOR, -- For full-text search
    
    -- Status & visibility
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, discontinued
    visibility VARCHAR(50) DEFAULT 'public', -- public, private, draft
    warranty_months INTEGER DEFAULT 60,
    is_bestseller BOOLEAN DEFAULT FALSE,
    display_order INTEGER DEFAULT 0,
    
    -- Metadata
    metadata JSONB DEFAULT '{}', -- Custom fields
    specifications JSONB DEFAULT '{}', -- Detailed specs
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    UNIQUE(organization_id, sku),
    UNIQUE(organization_id, slug)
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_status_visibility ON products(status, visibility);
CREATE INDEX idx_products_search ON products USING GIN (search_text);
```

### 5. Product Variants (Colors, Glass types, Hardware)

```sql
CREATE TABLE product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_type VARCHAR(50) NOT NULL, -- color, glass, hardware, size
    variant_name VARCHAR(255) NOT NULL,
    variant_value VARCHAR(255) NOT NULL,
    
    -- Pricing override
    price_modifier DECIMAL(12, 2) DEFAULT 0, -- Addition to base price
    
    -- Media
    image_url VARCHAR(500),
    color_hex VARCHAR(7), -- For color variants
    
    -- Availability
    stock_quantity INTEGER DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(product_id, variant_type, variant_value)
);

CREATE INDEX idx_product_variants_product ON product_variants(product_id);
CREATE INDEX idx_product_variants_type ON product_variants(variant_type);
```

### 6. Product Pricing (Time-based pricing)

```sql
CREATE TABLE product_pricing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    customer_segment VARCHAR(50), -- retail, wholesale, bulk, corporate
    price DECIMAL(12, 2) NOT NULL,
    installation_cost DECIMAL(12, 2) DEFAULT 0,
    minimum_quantity INTEGER DEFAULT 1,
    maximum_quantity INTEGER,
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_pricing_product ON product_pricing(product_id);
CREATE INDEX idx_product_pricing_active_dates ON product_pricing(valid_from, valid_to) WHERE is_active;
```

---

## Order Management

### 7. Orders

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    customer_id UUID NOT NULL REFERENCES users(id),
    
    -- Order info
    order_number VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(50) DEFAULT 'pending', 
    -- pending, confirmed, processing, ready, shipped, delivered, cancelled
    payment_status VARCHAR(50) DEFAULT 'unpaid',
    -- unpaid, partial, paid, refunded
    
    -- Pricing
    subtotal DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(12, 2) DEFAULT 0,
    shipping_cost DECIMAL(12, 2) DEFAULT 0,
    discount_amount DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    
    -- Dates
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_completion_date DATE,
    actual_completion_date DATE,
    
    -- Customer info
    billing_address JSONB NOT NULL,
    shipping_address JSONB NOT NULL,
    customer_notes TEXT,
    admin_notes TEXT,
    
    -- Tracking
    tracking_number VARCHAR(100),
    courier_name VARCHAR(100),
    
    -- Payment
    payment_method VARCHAR(50),
    payment_reference VARCHAR(100),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);
CREATE INDEX idx_orders_date ON orders(order_date DESC);
CREATE INDEX idx_orders_number ON orders(order_number);
```

### 8. Order Items

```sql
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    
    -- Item details
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    
    -- Selected variants
    selected_variants JSONB NOT NULL, -- {color: "white", glass: "tinted", etc}
    
    -- Custom dimensions (if applicable)
    custom_width DECIMAL(10, 2),
    custom_height DECIMAL(10, 2),
    custom_depth DECIMAL(10, 2),
    
    -- Status
    item_status VARCHAR(50) DEFAULT 'pending', -- pending, in_production, ready, shipped, delivered
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

### 9. Quotes (Quote requests)

```sql
CREATE TABLE quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    customer_id UUID NOT NULL REFERENCES users(id),
    
    -- Quote details
    quote_number VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Pricing
    subtotal DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    
    -- Status
    status VARCHAR(50) DEFAULT 'draft',
    -- draft, sent, accepted, rejected, expired, converted_to_order
    
    -- Dates
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_date TIMESTAMP,
    valid_until DATE,
    accepted_date TIMESTAMP,
    
    -- Notes
    terms_and_conditions TEXT,
    notes TEXT,
    
    -- Conversion
    converted_to_order_id UUID REFERENCES orders(id),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_quotes_customer ON quotes(customer_id);
CREATE INDEX idx_quotes_status ON quotes(status);
CREATE INDEX idx_quotes_number ON quotes(quote_number);
CREATE INDEX idx_quotes_valid_until ON quotes(valid_until) WHERE status IN ('sent', 'draft');
```

### 10. Quote Items

```sql
CREATE TABLE quote_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_id UUID NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    
    selected_variants JSONB NOT NULL,
    custom_width DECIMAL(10, 2),
    custom_height DECIMAL(10, 2),
    custom_depth DECIMAL(10, 2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quote_items_quote ON quote_items(quote_id);
```

---

## Customer Management

### 11. Customers (Extended user info)

```sql
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    
    -- Classification
    customer_type VARCHAR(50), -- residential, commercial, builder, contractor
    segment VARCHAR(50), -- premium, standard, value, trial
    
    -- Contact
    primary_phone VARCHAR(20),
    alternate_phone VARCHAR(20),
    primary_address JSONB,
    alternate_address JSONB,
    
    -- Business info (if B2B)
    company_name VARCHAR(255),
    company_registration_number VARCHAR(100),
    tax_identification_number VARCHAR(100),
    industry VARCHAR(100),
    employee_count INTEGER,
    
    -- Relationship
    sales_rep_id UUID REFERENCES users(id),
    source_of_lead VARCHAR(100), -- website, referral, sales_call, event, etc.
    
    -- Status
    status VARCHAR(50) DEFAULT 'prospect', -- prospect, lead, customer, inactive, blocked
    
    -- Preferences
    communication_preference VARCHAR(50), -- email, sms, call, whatsapp
    language VARCHAR(10) DEFAULT 'en',
    
    -- Metrics
    lifetime_value DECIMAL(12, 2) DEFAULT 0,
    total_orders INTEGER DEFAULT 0,
    total_quotes_requested INTEGER DEFAULT 0,
    last_interaction_date TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_organization ON customers(organization_id);
CREATE INDEX idx_customers_user ON customers(user_id);
CREATE INDEX idx_customers_status ON customers(status);
CREATE INDEX idx_customers_segment ON customers(segment);
CREATE INDEX idx_customers_sales_rep ON customers(sales_rep_id);
```

### 12. Customer Projects

```sql
CREATE TABLE customer_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    customer_id UUID NOT NULL REFERENCES customers(id),
    
    -- Project info
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50), -- residential, commercial, renovation, new_construction
    
    -- Location
    site_address JSONB NOT NULL,
    coordinates GEOMETRY(POINT, 4326), -- GPS coordinates
    
    -- Dates
    start_date DATE,
    estimated_completion_date DATE,
    actual_completion_date DATE,
    
    -- Status
    status VARCHAR(50) DEFAULT 'planning',
    -- planning, quote_sent, approved, in_progress, completed, on_hold, cancelled
    
    -- Scope
    estimated_windows INTEGER,
    estimated_doors INTEGER,
    estimated_glass_area DECIMAL(10, 2), -- sqft/sqm
    project_value DECIMAL(12, 2),
    
    -- Site visit
    site_visit_date TIMESTAMP,
    site_visit_notes TEXT,
    site_images JSONB DEFAULT '[]',
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customer_projects_customer ON customer_projects(customer_id);
CREATE INDEX idx_customer_projects_status ON customer_projects(status);
```

---

## Inventory Management

### 13. Inventory Stock

```sql
CREATE TABLE inventory_stock (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    product_id UUID NOT NULL REFERENCES products(id),
    variant_id UUID REFERENCES product_variants(id),
    
    -- Warehouse location
    warehouse_id VARCHAR(50) NOT NULL,
    bin_location VARCHAR(50),
    
    -- Stock levels
    quantity_on_hand INTEGER NOT NULL DEFAULT 0,
    quantity_reserved INTEGER NOT NULL DEFAULT 0,
    quantity_available INTEGER GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved) STORED,
    
    -- Thresholds
    minimum_stock_level INTEGER DEFAULT 10,
    reorder_point INTEGER DEFAULT 20,
    reorder_quantity INTEGER DEFAULT 50,
    maximum_stock_level INTEGER DEFAULT 500,
    
    -- Supplier
    supplier_id VARCHAR(100),
    supplier_sku VARCHAR(100),
    lead_time_days INTEGER,
    
    -- Dates
    last_received_date TIMESTAMP,
    last_counted_date TIMESTAMP,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, obsolete
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(product_id, variant_id, warehouse_id, bin_location)
);

CREATE INDEX idx_inventory_stock_product ON inventory_stock(product_id);
CREATE INDEX idx_inventory_stock_warehouse ON inventory_stock(warehouse_id);
CREATE INDEX idx_inventory_stock_low_stock ON inventory_stock(quantity_available) 
    WHERE quantity_available <= minimum_stock_level;
```

### 14. Inventory Transactions

```sql
CREATE TABLE inventory_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    inventory_stock_id UUID NOT NULL REFERENCES inventory_stock(id),
    
    transaction_type VARCHAR(50) NOT NULL,
    -- in: purchase_receipt, return_from_customer, correction
    -- out: order_fulfillment, damaged, lost, correction
    
    quantity_change INTEGER NOT NULL,
    
    -- Reference
    reference_id UUID, -- order_id or quote_id
    reference_type VARCHAR(50),
    
    -- Details
    notes TEXT,
    created_by_user_id UUID REFERENCES users(id),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inventory_transactions_stock ON inventory_transactions(inventory_stock_id);
CREATE INDEX idx_inventory_transactions_date ON inventory_transactions(created_at DESC);
```

---

## AI & Documents

### 15. Documents (For RAG system)

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    
    -- Document metadata
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    -- product_brochure, installation_manual, warranty, certification, policy, faq, blog
    
    document_url VARCHAR(500) NOT NULL,
    file_size_bytes INTEGER,
    file_extension VARCHAR(10),
    
    -- Content
    raw_text TEXT,
    is_indexed BOOLEAN DEFAULT FALSE,
    
    -- Source
    source_product_id UUID REFERENCES products(id),
    related_products JSONB DEFAULT '[]', -- Array of product IDs
    
    -- Metadata
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_by_user_id UUID REFERENCES users(id),
    
    status VARCHAR(50) DEFAULT 'active', -- active, archived, deleted
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_organization ON documents(organization_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_product ON documents(source_product_id);
```

### 16. Document Chunks (For RAG embeddings)

```sql
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    
    -- Chunk info
    chunk_number INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_tokens INTEGER, -- Token count for billing/optimization
    
    -- Embedding (stored as vector in Qdrant, but reference kept here)
    embedding_id VARCHAR(100), -- Reference to Qdrant vector ID
    embedding_model VARCHAR(50) DEFAULT 'text-embedding-3-small',
    
    -- Metadata for retrieval
    metadata JSONB DEFAULT '{}'  , -- Page number, section, etc.
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_document_chunks_document ON document_chunks(document_id);
```

### 17. AI Conversations

```sql
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    user_id UUID REFERENCES users(id), -- NULL for anonymous
    
    -- Conversation details
    conversation_topic VARCHAR(100),
    -- sales_inquiry, product_question, quote_request, design_consultation, general
    
    ai_model VARCHAR(50) DEFAULT 'gpt-4',
    temperature DECIMAL(3, 2) DEFAULT 0.7,
    
    -- Status
    is_archived BOOLEAN DEFAULT FALSE,
    sentiment VARCHAR(50), -- positive, neutral, negative
    
    -- Metadata
    ip_address VARCHAR(45), -- IPv4 or IPv6
    user_agent TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_conversations_user ON ai_conversations(user_id);
CREATE INDEX idx_ai_conversations_date ON ai_conversations(created_at DESC);
```

### 18. AI Messages (Chat history)

```sql
CREATE TABLE ai_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES ai_conversations(id) ON DELETE CASCADE,
    
    -- Message content
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    
    -- Tokens & cost
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    estimated_cost DECIMAL(8, 4),
    
    -- Context
    documents_used JSONB DEFAULT '[]', -- Array of document IDs used for RAG
    
    -- Metadata
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_messages_conversation ON ai_messages(conversation_id);
CREATE INDEX idx_ai_messages_role ON ai_messages(role);
```

### 19. AI Generated Images

```sql
CREATE TABLE ai_generated_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    
    -- Source
    source_image_url VARCHAR(500),
    original_image_url VARCHAR(500),
    
    -- Generation details
    generation_model VARCHAR(50),
    -- dall-e-3, flux, stable-diffusion, controlnet
    
    prompt TEXT,
    processing_status VARCHAR(50), -- processing, completed, failed
    
    -- Results
    generated_image_urls JSONB DEFAULT '[]', -- Array of URLs
    thumbnail_url VARCHAR(500),
    
    -- Parameters
    generation_params JSONB DEFAULT '{}',
    -- width, height, style, quality, variations, etc.
    
    -- Cost tracking
    tokens_used INTEGER,
    estimated_cost DECIMAL(8, 4),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_generated_images_user ON ai_generated_images(user_id);
CREATE INDEX idx_ai_generated_images_status ON ai_generated_images(processing_status);
```

---

## Analytics & Audit

### 20. Lead Analytics

```sql
CREATE TABLE lead_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    customer_id UUID REFERENCES customers(id),
    
    -- Lead source
    source VARCHAR(100), -- website_form, ai_chat, phone, email, referral, event, social
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    utm_content VARCHAR(255),
    
    -- Interaction
    interaction_type VARCHAR(50), -- page_visit, form_submit, chat_started, quote_requested
    page_url VARCHAR(500),
    
    -- Status
    conversion_status VARCHAR(50), -- converted, in_progress, abandoned, lost
    
    -- Metrics
    time_on_site_seconds INTEGER,
    pages_visited INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lead_analytics_organization ON lead_analytics(organization_id);
CREATE INDEX idx_lead_analytics_source ON lead_analytics(source);
CREATE INDEX idx_lead_analytics_conversion ON lead_analytics(conversion_status);
```

### 21. Audit Logs

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    
    -- Action details
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL, -- product, order, customer, etc.
    entity_id VARCHAR(100) NOT NULL,
    
    -- Changes
    old_values JSONB,
    new_values JSONB,
    
    -- Context
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Status
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_audit_logs_user (user_id),
    INDEX idx_audit_logs_entity (entity_type, entity_id),
    INDEX idx_audit_logs_date (created_at DESC)
);
```

---

## Indexing Strategy

### Performance-Critical Indexes

```sql
-- Products & Variants
CREATE INDEX idx_products_org_status ON products(organization_id, status, visibility);
CREATE INDEX idx_product_variants_availability ON product_variants(product_id, is_available);

-- Orders & Quotes
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date DESC);
CREATE INDEX idx_quotes_customer_status ON quotes(customer_id, status);

-- Inventory
CREATE INDEX idx_inventory_low_stock_alert ON inventory_stock(organization_id, quantity_available) 
    WHERE quantity_available <= minimum_stock_level;

-- Analytics
CREATE INDEX idx_lead_analytics_date ON lead_analytics(created_at DESC);
CREATE INDEX idx_ai_conversations_recent ON ai_conversations(created_at DESC) 
    WHERE is_archived = FALSE;
```

### Full-Text Search Index

```sql
-- Product search
CREATE INDEX idx_products_fts ON products USING GIN(search_text);

-- Update trigger for full-text search
CREATE OR REPLACE FUNCTION update_product_search_text()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_text := to_tsvector('english', 
        COALESCE(NEW.name, '') || ' ' ||
        COALESCE(NEW.description, '') || ' ' ||
        COALESCE(NEW.seo_keywords, '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_product_search_text
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_product_search_text();
```

---

## Constraints & Relationships

### Foreign Key Relationships

```sql
-- Referential Integrity
ALTER TABLE products ADD CONSTRAINT fk_products_org 
    FOREIGN KEY (organization_id) REFERENCES organizations(id);

ALTER TABLE product_variants ADD CONSTRAINT fk_variants_product 
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE;

ALTER TABLE orders ADD CONSTRAINT fk_orders_customer 
    FOREIGN KEY (customer_id) REFERENCES users(id);

ALTER TABLE order_items ADD CONSTRAINT fk_order_items_order 
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE;

-- All user_id FKs reference users table
-- All organization_id FKs reference organizations table
```

### Check Constraints

```sql
-- Pricing validations
ALTER TABLE products ADD CONSTRAINT check_prices 
    CHECK (base_price >= 0 AND installation_cost >= 0);

ALTER TABLE orders ADD CONSTRAINT check_order_amounts 
    CHECK (total_amount >= subtotal AND total_amount >= 0);

-- Stock validations
ALTER TABLE inventory_stock ADD CONSTRAINT check_stock_levels 
    CHECK (quantity_on_hand >= 0 AND quantity_reserved >= 0);

-- Date validations
ALTER TABLE quotes ADD CONSTRAINT check_quote_dates 
    CHECK (valid_until >= DATE(created_at));
```

---

## Partitioning Strategy

### Time-based Partitioning

For high-volume tables, implement partitioning:

```sql
-- Orders table by month
CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- AI Messages by month
CREATE TABLE ai_messages_2024_06 PARTITION OF ai_messages
    FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
```

### Archive Strategy

```sql
-- Archive old orders (> 2 years) to separate schema
CREATE SCHEMA archived;
CREATE TABLE archived.orders_2022 AS 
    SELECT * FROM orders WHERE YEAR(order_date) = 2022;
```

---

## Views for Analytics

### Useful Views

```sql
-- Customer sales summary
CREATE VIEW v_customer_sales_summary AS
SELECT 
    c.id,
    c.user_id,
    COUNT(DISTINCT o.id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    MAX(o.order_date) as last_order_date,
    AVG(o.total_amount) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.user_id = o.customer_id
GROUP BY c.id, c.user_id;

-- Product performance
CREATE VIEW v_product_performance AS
SELECT 
    p.id,
    p.name,
    COUNT(oi.id) as times_ordered,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(oi.unit_price) as avg_selling_price
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.status != 'cancelled'
GROUP BY p.id, p.name;

-- Inventory status
CREATE VIEW v_inventory_status AS
SELECT 
    p.name,
    ps.warehouse_id,
    ps.quantity_on_hand,
    ps.quantity_reserved,
    ps.quantity_available,
    ps.minimum_stock_level,
    ps.reorder_point,
    CASE 
        WHEN ps.quantity_available = 0 THEN 'Out of Stock'
        WHEN ps.quantity_available <= ps.minimum_stock_level THEN 'Low Stock'
        WHEN ps.quantity_available <= ps.reorder_point THEN 'Reorder Required'
        ELSE 'In Stock'
    END as stock_status
FROM inventory_stock ps
JOIN products p ON ps.product_id = p.id;
```

---

## Migration & Versioning

### Schema Versions

- **v1.0**: Initial schema (this document)
- Future: Add versioning to track schema changes

### Migrations Using Alembic (SQLAlchemy)

```
migrations/
├── env.py
├── script.py.mako
└── versions/
    ├── 001_initial_schema.py
    ├── 002_add_audit_logs.py
    └── 003_add_vector_extension.py
```

---

## Performance Optimization

### Query Optimization Techniques

1. **Denormalization** (carefully):
   - Store `total_amount` in orders (instead of calculating from order_items)
   - Store `quantity_available` in inventory_stock (GENERATED column)

2. **Materialized Views**:
   - Daily sales summary
   - Monthly revenue report
   - Product performance metrics

3. **Connection Pooling**:
   - SQLAlchemy with psycopg2 connection pool
   - PgBouncer for application-level pooling

---

## Next Steps

- [ ] Add CREATE statements to Alembic migration
- [ ] Implement SQLAlchemy ORM models
- [ ] Create database indexes optimization report
- [ ] Plan backup and recovery strategy
- [ ] Set up monitoring and alerting for slow queries

---

**Schema Status:** Ready for ORM modeling  
**Last Updated:** 2026-06-24  
**Next Review:** After API contract design

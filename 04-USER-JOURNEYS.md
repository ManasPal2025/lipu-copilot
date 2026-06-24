# User Journeys & Workflows

**Document Version:** 1.0  
**Status:** User Experience Design Phase

---

## Table of Contents

1. [User Personas](#user-personas)
2. [Journey Map: First-Time Visitor](#journey-map-first-time-visitor)
3. [Journey Map: Customer - Product Purchase](#journey-map-customer-product-purchase)
4. [Journey Map: Customer - Custom Quote](#journey-map-customer-custom-quote)
5. [Journey Map: Customer - House Visualization](#journey-map-customer-house-visualization)
6. [Journey Map: Sales Agent](#journey-map-sales-agent)
7. [Journey Map: Admin - Inventory Management](#journey-map-admin-inventory-management)
8. [Journey Map: Admin - Analytics Review](#journey-map-admin-analytics-review)
9. [Pain Points & Solutions](#pain-points--solutions)

---

## User Personas

### 1. Homeowner (Residential Customer)

**Name:** Priya Sharma  
**Age:** 35  
**Occupation:** Software Engineer  
**Location:** Mumbai, Maharashtra

**Goals:**
- Find high-quality UPVC windows for home renovation
- Understand product options (colors, glass types, warranty)
- Get accurate quotes without pushy sales calls
- Visualize how windows look on their home before ordering
- Compare prices and read reviews

**Pain Points:**
- Overwhelmed by too many options
- Don't want to visit physical showrooms
- Need professional guidance
- Concerned about installation quality

**Tech Proficiency:** High (comfortable with online platforms)

---

### 2. Architect/Builder

**Name:** Rajesh Patel  
**Age:** 45  
**Occupation:** Architect  
**Location:** Bangalore, Karnataka

**Goals:**
- Source UPVC materials for multiple projects
- Get bulk pricing and project-based quotes
- Track project specifications and requirements
- Collaborate with contractors and clients
- Access technical documentation and certifications

**Pain Points:**
- Need competitive pricing for bulk orders
- Complex specification tracking
- Multiple stakeholders to coordinate
- Tight project timelines

**Tech Proficiency:** Medium-High

---

### 3. Interior Designer

**Name:** Anjali Desai  
**Age:** 32  
**Occupation:** Interior Designer  
**Location:** Delhi, NCR

**Goals:**
- Access premium design options
- Match windows to overall interior aesthetic
- Provide client visualizations
- Get professional discount
- Quick quote turnaround

**Pain Points:**
- Need immediate responses
- Want design inspiration
- Client expectations management
- Coordination with installers

**Tech Proficiency:** Medium-High

---

### 4. Sales Representative (Company)

**Name:** Amit Kumar  
**Age:** 40  
**Occupation:** Sales Manager  
**Location:** Head Office, Mumbai

**Goals:**
- Track leads and conversion funnels
- Manage customer interactions
- Generate sales reports and analytics
- Track inventory levels
- Manage team performance

**Pain Points:**
- Manual CRM updates
- Hard to track lead source ROI
- Difficulty forecasting
- Too many tools to manage

**Tech Proficiency:** Medium

---

### 5. System Administrator

**Name:** Shreya Nair  
**Age:** 28  
**Occupation:** Operations Manager  
**Location:** Head Office, Mumbai

**Goals:**
- Maintain inventory accuracy
- Process orders efficiently
- Manage user access and permissions
- Monitor system health
- Generate compliance reports

**Pain Points:**
- Manual data entry errors
- Inventory discrepancies
- Difficult permission management
- Limited real-time visibility

**Tech Proficiency:** High

---

## Journey Map: First-Time Visitor

### Scenario
Priya (homeowner) discovers the website via Google search for "UPVC windows Mumbai"

### Steps

**1. Landing (0-30 seconds)**
```
User Action:
├── Lands on homepage from Google search
├── Views hero section with product showcase
├── Observes luxury, modern design
└── Sees clear navigation

Touchpoint: Homepage
Design Goals:
├── Professional, premium first impression
├── Clear value proposition
├── Easy navigation visible
└── Trust signals (awards, certifications)

Success Metric: User scrolls below fold
```

**2. Exploration (1-5 minutes)**
```
User Action:
├── Scrolls through hero section
├── Reads product categories
├── Views featured products
├── Sees testimonials and case studies
└── Notices "Free AI Consultation" CTA

Touchpoint: Homepage Sections
├── Hero section
├── Product showcase
├── Testimonials
├── Case studies/Gallery

Decision Point:
├── IF interested in specific product → Click product
├── IF wants to explore more → Browse catalog
├── IF wants consultation → Start AI Chat
└── IF wants contact → Fill inquiry form
```

**3. Product Discovery (5-15 minutes)**
```
User Action:
├── Clicks on "Sliding Windows" category
├── Sees product listings with images
├── Reads product descriptions
├── Filters by color/glass type
├── Reads customer reviews

Touchpoint: Product Catalog Page
├── Product cards with images
├── Filters (category, color, glass, price)
├── Ratings and reviews
├── "Add to Compare" button
└── "Request Quote" CTA

Data Collected:
├── Product interest
├── Time spent on product
├── Filters applied
└── Search queries

AI Agent Interaction:
"I see you're interested in sliding windows. 
Would you like to know about the best glass 
type for coastal areas, or shall I show you 
color options?"
```

**4. AI Consultation (Optional - 5-10 minutes)**
```
User Action:
├── Clicks "Chat with AI Assistant"
├── Asks question: "What's best for coastal weather?"
├── Receives answer with product recommendations
├── Views visualizations
└── Gets preliminary quote

Touchpoint: AI Chat Interface
├── Streaming responses
├── Quick reply suggestions
├── Product recommendations
├── Quote preview
└── "Book Site Visit" button

Engagement Metrics:
├── Questions asked
├── Products recommended
├── Average response satisfaction
└── Lead quality score
```

**5. Quote Request (10-20 minutes)**
```
User Action:
├── Clicks "Request Quote"
├── Fills in project details:
│   ├── Project location
│   ├── Window/Door count
│   ├── Preferred style
│   └── Budget range
├── Selects products
├── Provides contact info
└── Submits

Touchpoint: Quote Request Form
├── Multi-step form (UX progressive disclosure)
├── Pre-filled with browsed products
├── Location auto-complete
├── Image upload option
└── Email/SMS consent

Confirmation:
├── Email with quote number
├── SMS notification
├── "Track Your Quote" link
├── Next steps communication

Handoff to Sales:
├── Sales rep assigned
├── Lead score calculated
├── Follow-up scheduled
└── Notification to sales team
```

**6. Email Follow-up (24-72 hours)**
```
Touchpoint: Email
├── Welcome email with brand story
├── Quote details and summary
├── "Book Free Site Visit" link
├── Payment options
├── FAQ link
├── Support contact

Action Items:
├── Click to review quote details
├── Click to book site visit
├── Or contact sales team
```

---

## Journey Map: Customer - Product Purchase

### Scenario
Priya is ready to order 5 sliding windows for her home

### Steps

**1. Product Selection**
```
Current State:
└── Customer has approved quote

User Action:
├── Logs into customer portal
├── Navigates to "My Quotes"
├── Clicks "Accept Quote" on approved quote
├── Reviews selected products with variants:
│   ├── Color: White
│   ├── Glass: Tinted
│   └── Hardware: Premium handles
├── Confirms specifications
└── Agrees to terms

Touchpoint: Customer Portal → Quote Detail
├── Quote summary
├── Product breakdown
├── Selected variants with images
├── Warranty info
├── Terms and conditions checkbox
└── "Proceed to Order" button

System Actions:
├── Update quote status to "accepted"
├── Create order draft
├── Reserve inventory
├── Send notification to sales team
└── Trigger order confirmation process
```

**2. Delivery & Billing Address**
```
User Action:
├── Reviews billing address (auto-filled from profile)
├── Confirms shipping address
├── Selects delivery time slot
├── Chooses delivery option:
│   ├── Standard Delivery (7-10 days)
│   ├── Express Delivery (3-5 days)
│   └── Site Pickup
└── Adds special instructions for delivery

Touchpoint: Order Form - Address Step
├── Saved addresses from profile
├── "Add New Address" option
├── Delivery slot calendar
├── Delivery option comparison
└── Special instructions field
```

**3. Payment**
```
User Action:
├── Reviews order summary:
│   ├── Product total: ₹75,000
│   ├── Installation: ₹5,000
│   ├── Delivery: ₹1,000
│   ├── Tax: ₹14,400
│   └── Total: ₹95,400
├── Selects payment method:
│   ├── Credit/Debit Card
│   ├── Net Banking
│   ├── UPI
│   ├── EMI Options
│   └── Download Invoice (before payment)
└── Completes payment

Touchpoint: Payment Page
├── Order summary
├── Payment gateway (Razorpay/Stripe)
├── Multiple payment options
├── Invoice preview/download
├── Security badges
└── "Secure Payment" button

Success Handling:
├── Payment confirmation
├── Order confirmation email
├── Order number generated (ORD-2026-000456)
├── Invoice generated and sent
├── Installation scheduler notified
└── Redirect to order tracking
```

**4. Order Confirmation**
```
Touchpoint: Confirmation Page + Email
Display:
├── Order number
├── Items and quantities
├── Total amount paid
├── Estimated delivery date
├── Installation date (if applicable)
├── Next steps
└── Support contact info

Email Content:
├── Order summary
├── Invoice attachment
├── Tracking link
├── Installation timeline
├── Warranty certificate link
├── Customer support ticket creation
└── Estimated invoice delivery

System Actions:
├── Create order in system
├── Allocate inventory
├── Create installation work order
├── Schedule site visit
├── Send notification to warehouse
├── Send notification to logistics partner
└── Create customer support ticket
```

**5. Order Tracking (During Fulfillment)**
```
Touchpoint: Order Details Page
Customer can see:
├── Order status timeline:
│   ├── ✓ Order Confirmed
│   ├── ⟳ Processing (estimated 2 days)
│   ├── ⊘ Ready for Shipment (estimated 3 days)
│   ├── ⊘ Shipped (estimated date)
│   ├── ⊘ Out for Delivery
│   └── ⊘ Delivered
│
├── Real-time status updates
├── Estimated delivery date
├── Delivery tracking info
├── Chat support button
└── Cancel order option (if eligible)

Notifications:
├── Email: Order processing started
├── SMS: Ready to ship
├── Email: Shipped with tracking number
├── SMS: Out for delivery
├── Email: Delivered
└── SMS: Installation scheduled
```

**6. Delivery & Installation**
```
User Action:
├── Receives delivery notification 1 hour before
├── Prepares delivery location
├── Verifies product condition at delivery
├── Signs delivery confirmation
├── Schedules installation if applicable

Touchpoint: SMS/Email + Order Portal
└── Delivery slot countdown
└── Delivery partner contact
└── Installation scheduling
└── Site visit pre-inspection

Post-Delivery:
├── Warranty card provided
├── Installation manual
├── Maintenance tips
├── Support ticket for issues
└── Feedback/Review request

System Actions:
├── Update order status to "Delivered"
├── Send warranty registration reminder
├── Create post-delivery support ticket
├── Request product review
└── Schedule follow-up NPS survey
```

---

## Journey Map: Customer - Custom Quote

### Scenario
Rajesh (architect) needs a bulk quote for 50 windows and 20 doors for a commercial project

### Steps

**1. Quote Initiation**
```
User Action:
├── Logs into portal
├── Clicks "Request Quote"
├── Selects "Commercial Project"
├── Enters project details:
│   ├── Project name: "Commercial Complex, Bangalore"
│   ├── Location: Bangalore
│   ├── Project type: Commercial
│   ├── Timeline: 3 months
│   └── Budget: ₹25,00,000

Touchpoint: Quote Form
├── Project classification
├── Location selection
├── Project timeline
├── Budget range
└── Project description field
```

**2. Specification Entry**
```
User Action:
├── Adds 50 sliding windows:
│   ├── Type: Sliding
│   ├── Color: Aluminum Silver
│   ├── Glass: Tinted + Low-E coating
│   ├── Hardware: Commercial grade handles
│   ├── Average size: 1.5m × 1.2m
│   └── Specifications per window
│
├── Adds 20 glass doors:
│   ├── Type: Hinged Glass Doors
│   ├── Specifications
│   └── Hardware
│
├── Enters measurements table
├── Adds site images/layout drawings
├── Specifies installation requirements
└── Notes special requirements (earthquake zone, high wind area)

Touchpoint: Multi-step Quote Builder
├── Product type selector
├── Quantity inputs
├── Specification forms (size, color, glass, hardware)
├── Measurement input grid
├── File upload (drawings, layouts, images)
└── Special requirements notes

Data Collection:
├── Exact product specifications
├── Bulk quantity
├── Custom sizing
├── Installation complexity
└── Project constraints
```

**3. Preliminary Pricing**
```
System Action (AI-Powered):
├── Calculate material costs:
│   ├── 50 × ₹15,000 (windows) = ₹7,50,000
│   ├── 20 × ₹8,000 (doors) = ₹1,60,000
│   ├── Bulk discount (10% for 70+ units) = ₹1,27,000
│   └── Subtotal: ₹7,83,000
│
├── Calculate labor costs:
│   ├── Installation labor: 50 × ₹3,000 = ₹1,50,000
│   ├── Site supervision: ₹50,000
│   └── Subtotal: ₹2,00,000
│
├── Calculate total estimate: ₹9,83,000
└── Add 18% GST: ₹1,76,940
└── Final estimate: ₹11,59,940

Touchpoint: Price Preview
├── Itemized breakdown
├── Discount breakdown
├── Tax calculation
├── Payment terms options
├── Financing options
└── "Request Formal Quote" CTA
```

**4. Expert Review**
```
System Action:
├── Route to senior sales engineer
├── Send notification to sales team
├── Flag as "high-value" (bulk order)
├── Assign dedicated account manager

Sales Engineer Review:
├── Review specifications
├── Validate site requirements
├── Check warehouse availability
├── Confirm timeline feasibility
├── Prepare detailed quote
└── Schedule consultation call

Notification to Customer:
├── Email: "We're preparing your detailed quote"
├── Email: "Schedule a consultation call"
└── Portal: Call scheduling interface
```

**5. Formal Quote Generation**
```
System Action:
├── Generate formal quote document:
│   ├── Itemized breakdown (50 windows, 20 doors)
│   ├── Specifications per item
│   ├── Bulk discount details
│   ├── Tax calculation
│   ├── Payment terms:
│   │   ├── 40% advance
│   │   ├── 40% before delivery
│   │   └── 20% after installation
│   ├── Warranty terms
│   ├── Delivery timeline (45 days)
│   ├── Installation timeline (30 days)
│   ├── Terms & conditions
│   └── Authorized signature
│
├── Email formal quote
├── Update portal with quote
└── Create quote tracking

Touchpoint: Email + Portal
├── Formal quote PDF attached
├── Quotation number (QT-2026-001245)
├── Valid until date (30 days)
├── "View Full Quote" link
├── "Accept Quote" button
├── "Request Modifications" link
└── Support contact info
```

**6. Collaboration & Modification**
```
User Action (If modifications needed):
├── Clicks "Request Modifications"
├── Opens quote modification form
├── Changes specifications:
│   ├── Increases door quantity to 25
│   ├── Changes glass type to ultra-clear
│   └── Requests additional color option
│
├── Adds comment: "Need ECO certification for this project"
└── Submits modification request

Touchpoint: Quote Modification Form
├── Current quote summary
├── Specification editor
├── Reason for modification
├── Comment field
└── Submit button

System Action:
├── Notification to sales engineer
├── Recalculate pricing
├── Generate updated quote
├── Send revised quote within 24 hours
└── Track modification history

Touchpoint: Updated Quote
├── Revision history visible
├── Changes highlighted
├── New total price: ₹12,50,000 (updated)
└── "Accept Updated Quote" button
```

**7. Quote Acceptance**
```
User Action:
├── Reviews final quote
├── Clicks "Accept Quote"
├── Enters authorized signatory details
├── Accepts terms & conditions
└── Submits

System Action:
├── Mark quote as "Accepted"
├── Create sales order
├── Reserve inventory
├── Send confirmation email
├── Generate purchase order (optional)
├── Create project in system
├── Assign project manager
├── Schedule kickoff meeting
└── Notification to operations team

Confirmation:
├── Project creation confirmation
├── Project manager contact
├── Next steps email
├── Production schedule
├── Installation timeline
└── Support ticket creation
```

---

## Journey Map: Customer - House Visualization

### Scenario
Priya wants to visualize how the white sliding windows will look on her home

### Steps

**1. Upload House Photo**
```
User Action:
├── In product detail or quote page
├── Clicks "Preview on Your Home"
├── Selects photo:
│   ├── Takes new photo (camera)
│   ├── Uploads existing photo
│   └── Selects from gallery
│
├── Uploads house photo (.jpg/.png)
└── Image loads

Touchpoint: Visualization Module
├── "Preview on Your Home" CTA
├── Photo upload interface
├── Camera access (mobile)
├── Gallery selection
├── Image preview before processing
└── "Start Visualization" button

Validations:
├── Image size check (max 10MB)
├── Image quality check
├── House/building detection
├── Window detection validation
└── Error messages if issues found
```

**2. AI Processing**
```
System Action (Background):
├── Computer vision model processes image:
│   ├── Detects building/house
│   ├── Detects existing windows/doors
│   ├── Segments window areas
│   ├── Estimates camera angle
│   └── Calculates dimensions
│
├── Status updates streamed to user:
│   ├── "Analyzing image..."
│   ├── "Detecting windows..."
│   ├── "Generating visualization..."
│   └── "Almost ready!"

User Experience:
├── Progress indicator (0-100%)
├── Status messages
├── Estimated time (15-30 seconds)
└── Sample visualizations shown while waiting
```

**3. Visualization Generation**
```
System Action:
├── AI image generation model creates variations:
│   ├── White frames (original selection)
│   ├── Black frames
│   ├── Wood finish
│   ├── Different glass tint levels
│   └── Sliding + casement styles (3-5 variations)

Processing:
├── Uses Flux/ControlNet for precise replacement
├── Maintains lighting and shadows
├── Preserves surrounding building context
├── Generates 4-6 different options

Touchpoint: Visualization Results Page
├── Before photo (original)
├── After photos (variations)
├── Product selector
├── Style selector
├── Comparison slider (before/after)
└── Navigation arrows

Display Options:
├── Grid view (all variations)
├── Full screen view
├── Side-by-side comparison
├── Swipe on mobile
└── Zoom in/out
```

**4. Customization**
```
User Action:
├── Views generated visualizations
├── Can modify parameters:
│   ├── Click to change frame color
│   ├── Click to change glass type
│   ├── Click to regenerate
│   ├── Try different window style
│   └── Regenerate with different products
│
├── Selects favorite visualization
└── Shares or saves

Touchpoint: Visualization Editor
├── Generated images displayed
├── Product selector dropdown
├── Style selector dropdown
├── "Regenerate" button (regenerate with new settings)
├── Comparison tools
└── Save/Share buttons

Additional Features:
├── Side-by-side comparison of variations
├── Details visible on hover
├── Information about selected product
├── Pricing for shown product
└── "View More Colors" for that product
```

**5. Save & Share**
```
User Action:
├── Clicks "Save Visualization"
├── View is added to profile gallery
├── Can share visualization:
│   ├── Copy link to share
│   ├── Share to WhatsApp
│   ├── Email to contacts
│   ├── Share via SMS
│   └── Download as image
│
├── Adds to "Saved Designs" portfolio
└── Can compare with other designs

Touchpoint: Save/Share Modal
├── Save to "My Designs" gallery
├── Share link generation
├── Social sharing options
├── Email composition
├── SMS sharing
└── Download image button

Post-Action:
├── Email/SMS sent to recipient with link
├── Recipient can:
│   ├── View visualization
│   ├── Get product details
│   ├── Request quote for same products
│   └── Contact sales team
│
└── Analytics tracked:
    ├── Shared links clicked
    ├── Conversion from shares
    └── Popular visualization features
```

**6. Quote from Visualization**
```
User Action:
├── After viewing visualization
├── Clicks "Get Quote for This Design"
├── Quote form pre-filled with:
│   ├── Selected product
│   ├── Color
│   ├── Glass type
│   ├── Approximate dimensions from photo
│   └── Estimated quantity
│
├── Fills in project details:
│   ├── Location
│   ├── Timeline
│   ├── Budget
│   └── Contact info
│
└── Submits quote request

Result:
├── Sales team receives lead with:
│   ├── Customer info
│   ├── Chosen products & visualization
│   ├── Estimated requirements
│   └── High lead quality score
│
├── Quote generated within 24 hours
└── Customer notified via email/SMS
```

---

## Journey Map: Sales Agent

### Scenario
Amit (Sales Manager) manages his daily sales activities and leads

### Steps

**1. Dashboard Review (Start of Day - 5 minutes)**
```
User Action:
├── Logs into admin portal
├── Views dashboard:
│   ├── Key metrics (today, this week, this month)
│   ├── New leads count
│   ├── Quotes awaiting action
│   ├── Orders due for delivery
│   ├── Revenue tracker
│   ├── Conversion funnel
│   └── Team performance (if manager)

Touchpoint: Admin Dashboard
├── KPI cards (clickable for details)
├── Charts (revenue, leads, conversions)
├── To-do list
├── Notifications (5 pending items)
├── Quick action buttons
└── Team leaderboard (if applicable)

Data Visible:
├── YTD sales: ₹45 lakhs
├── This month: ₹12 lakhs
├── New leads this week: 23
├── Conversion rate: 18%
├── Average deal value: ₹2.5 lakhs
└── Days to close: 15
```

**2. Lead Management (30-60 minutes)**
```
User Action:
├── Clicks "My Leads" section
├── Views lead list filtered by status:
│   ├── New leads (5)
│   ├── Contacted (8)
│   ├── Qualified (3)
│   ├── Quote sent (2)
│   └── Negotiation (2)

Touchpoint: Leads List
├── Filtering options (status, source, date)
├── Sorting options (priority, date, value)
├── Lead cards showing:
│   ├── Lead name
│   ├── Contact info
│   ├── Project type/value
│   ├── Status
│   ├── Last interaction
│   ├── Next follow-up date
│   └── Priority flag (hot lead indicator)
│
├── Bulk actions (mark contacted, add note, assign)
└── Quick contact buttons (call, email, WhatsApp)

Lead Detail View:
├── Lead information:
│   ├── Name, contact, location
│   ├── Project details (type, value, timeline)
│   ├── Source of lead
│   ├── Products interested in
│   └── Interaction history
│
├── Action history:
│   ├── All previous calls, emails, meetings
│   ├── Notes from previous interactions
│   ├── Documents shared
│   └── Quotes generated
│
├── Next steps:
│   ├── Scheduled follow-up date
│   ├── Task reminders
│   ├── Required actions
│   └── Suggested follow-up strategy

Actions:
├── Click "Contact" → Opens call/email/chat
├── Click "Send Quote" → Generate and send
├── Click "Schedule Follow-up" → Calendar
├── Click "Add Note" → Add interaction details
└── Click "Convert to Project" → If accepted quote
```

**3. Quote Generation (30 minutes)**
```
User Action (For lead ready for quote):
├── Selects lead with project requirements
├── Clicks "Generate Quote"
├── Pre-filled form shows:
│   ├── Lead information
│   ├── Project details from lead info
│   ├── Estimated requirements
│   └── Previous quote (if any)

Touchpoint: Quote Builder
├── Lead information (auto-filled)
├── Product selector (searchable)
├── Specification form:
│   ├── Quantity
│   ├── Product variant selections
│   ├── Custom measurements
│   ├── Special requirements
│   ├── Installation cost (configurable)
│   └── Discount (configurable based on lead segment/order size)

Quoting Logic:
├── Auto-calculate pricing based on:
│   ├── Product base price
│   ├── Variant modifiers
│   ├── Bulk discounts
│   ├── Customer segment pricing
│   ├── Promotional discounts (if applicable)
│   └── Taxes
│
└── Display:
    ├── Item breakdown
    ├── Total before tax
    ├── Tax amount
    ├── Discount summary
    └── Grand total

Actions:
├── "Save as Draft" → Save to send later
├── "Generate PDF" → Download PDF quote
├── "Email Quote" → Send directly to customer
├── "Print Quote" → Print physical copy
├── "Modify & Generate" → Adjust and regenerate
└── "Convert to Order" → If customer agrees verbally
```

**4. Email Communication (5-10 minutes)**
```
User Action:
├── Clicks "Email Quote" or "Send Message"
├── Opens email composer:
│   ├── To: Auto-filled with lead email
│   ├── Subject: Pre-populated template
│   ├── Body: Email template with:
│   │   ├── Personalization (lead name)
│   │   ├── Quote summary
│   │   ├── Call-to-action button
│   │   └── Signature
│   │
│   ├── Template selector (choose from templates)
│   ├── Attachment: Quote PDF auto-attached
│   ├── Schedule send (for later)
│   └── Send button

Touchpoint: Email Composer
├── Template library
├── Personalization tokens
├── Preview before send
├── Schedule send option
└── Track email opens/clicks

Automation:
├── Email sent
├── Marked as "Quote Sent" status
├── Email tracking enabled (open/click tracking)
├── Automatic follow-up scheduled
└── Notification on customer interaction
```

**5. Order Processing (If quote accepted - 10-15 minutes)**
```
User Action (When lead accepts):
├── Receives notification:
│   ├── Quote accepted by customer
│   ├── Notification on dashboard
│   └── Email/SMS alert

Touchpoint: Quote Status Update
├── Quote detail page shows: "Accepted"
├── "Convert to Order" button appears
├── Customer information visible
├── Terms agreed shown

Actions:
├── Click "Convert to Order"
├── Review order summary:
│   ├── Products and quantities
│   ├── Pricing (confirmed)
│   ├── Delivery address
│   ├── Installation date
│   └── Payment terms
│
├── Enter payment details:
│   ├── Advance amount (usually 40%)
│   ├── Payment deadline
│   ├── Payment method
│   └── Invoice generation
│
└── Click "Create Order"

Result:
├── Order created in system
├── Order number generated
├── Inventory reserved
├── Email sent to customer
├── Notifications to operations
├── Production schedule created
└── Sales rep receives "Order Created" confirmation
```

**6. Follow-up Tracking (Throughout day - ongoing)**
```
Touchpoint: Reminders & Notifications
├── Dashboard shows pending follow-ups
├── Email reminders for scheduled calls
├── Task notifications
├── Calendar integration

User Action:
├── Reviews "Today's To-Do" list
├── Calls leads based on schedule
├── Records outcome:
│   ├── Lead interested/not interested
│   ├── Call notes
│   ├── Next action
│   ├── Schedule follow-up
│   └── Update lead status
│
├── Updates lead information
├── Logs interaction
└── Notes progress

Tracking:
├── All interactions logged
├── Call duration recorded
├── Outcome tracked
├── Conversion probability updated
└── Sales forecast updated
```

**7. Sales Analytics (Weekly - 20 minutes)**
```
User Action:
├── Reviews personal performance:
│   ├── Weekly sales total
│   ├── Conversion rate (this week vs previous)
│   ├── Average deal size
│   ├── Number of leads generated
│   ├── Number of quotes sent
│   ├── Win rate
│   └── Revenue vs target
│
├── Views sales pipeline:
│   ├── Pipeline value by stage
│   ├── Deals at each stage
│   ├── Conversion rates by stage
│   ├── Average time in each stage
│   └── Bottleneck identification

Touchpoint: Sales Analytics
├── Personal KPI dashboard
├── Pipeline visualization (funnel chart)
├── Performance trends (line chart)
├── Leaderboard (if team)
├── Forecasting model
└── Downloadable reports

Actions:
├── Filter by date range
├── Filter by product category
├── Filter by lead source
├── Download as PDF/Excel
└── Share with manager
```

---

## Journey Map: Admin - Inventory Management

### Scenario
Shreya (Operations Manager) manages daily inventory operations

### Steps

**1. Inventory Dashboard (Start of Day - 5 minutes)**
```
User Action:
├── Logs into admin portal
├── Views inventory dashboard:
│   ├── Total SKUs in system
│   ├── Stock valuation (total)
│   ├── Items in low stock (7 alerts)
│   ├── Items out of stock (2 items)
│   ├── Items to be received (incoming shipments)
│   ├── Reorder recommendations
│   └── Warehouse utilization

Touchpoint: Inventory Dashboard
├── Key metrics cards
├── Low stock alerts (red flag)
├── Stock-out alerts (critical)
├── Incoming inventory timeline
├── Warehouse capacity gauge
├── Reorder recommendations
└── Quick action buttons

Alerts:
├── "Sliding Window White - 15 units (below minimum 20)"
├── "Tinted Glass - Out of stock (0 units)"
├── "Casement Hinges - 8 units arriving tomorrow"
└── "Warehouse B utilization at 92%"
```

**2. Low Stock Management (15-30 minutes)**
```
User Action:
├── Clicks "Low Stock Items"
├── Views list of low-stock items:
│   ├── Product name
│   ├── Current quantity
│   ├── Minimum level
│   ├── Reorder quantity
│   ├── Supplier info
│   ├── Lead time
│   └── Last received date

Touchpoint: Low Stock List
├── Sortable by urgency
├── Filters (category, warehouse, days until stockout)
├── Action buttons:
│   ├── "Create Purchase Order"
│   ├── "View Supplier"
│   ├── "Check Incoming"
│   └── "Adjust Stock"

Actions for Each Item:
├── IF critical AND out of stock:
│   ├── Click "Create Emergency PO"
│   ├── System shows alternate suppliers
│   ├── Select supplier with fastest delivery
│   └── Confirm PO creation
│
├── IF below minimum BUT not critical:
│   ├── Click "Create Reorder PO"
│   ├── Pre-filled with reorder quantity
│   ├── Review supplier terms
│   └── Confirm PO

Result:
├── Purchase order created
├── Email sent to supplier
├── Expected delivery date set
├── Notification to planning team
└── Follow-up scheduled
```

**3. Receiving Inventory (When shipments arrive - 30-45 minutes)**
```
Scenario:
├── Supplier delivery arrives at warehouse
├── Goods received at dock

User Action:
├── Receives notification: "Delivery from Supplier XYZ arrived"
├── Clicks "Receive Goods" task
├── Selects corresponding purchase order
├── System shows expected items:
│   ├── 50 units Sliding Window White
│   ├── 30 units Tinted Glass
│   └── 20 units Hardware Set

Warehouse Team Action:
├── Scans items as received
├── Verifies quantity:
│   ├── Scans each pallet/box
│   ├── Counts items
│   ├── Compares to PO
│   └── Records discrepancies (if any)
│
├── Inspects quality:
│   ├── Checks for damage
│   ├── Verifies specifications
│   ├── Notes defects
│   └── Photos damaged items
│
└── Updates system

Touchpoint: Receiving Module
├── PO details shown
├── Barcode scanner integration
├── Item checklist (can check off as received)
├── Quantity input fields
├── Quality inspection form
├── Damage photo upload
├── Notes field
└── "Complete Receipt" button

System Action:
├── Verify received quantity
├── Check for variances:
│   ├── IF quantity matches:
│   │   └── Mark as received
│   ├── IF quantity less than expected:
│   │   ├── Flag as partial receipt
│   │   ├── Notify purchasing
│   │   └── Create back order
│   └── IF damage noted:
│       ├── Create quality issue ticket
│       ├── Flag for supplier claim
│       └── Update stock accordingly
│
├── Update inventory:
│   ├── Add to warehouse location
│   ├── Update stock levels
│   ├── Update inventory value
│   └── Trigger low stock checks
│
├── Notifications:
│   ├── Purchasing team (partial receipt)
│   ├── Supplier quality team (damage)
│   ├── Sales team (inventory available)
│   └── Finance team (invoice processing)
│
└── Close purchase order
```

**4. Stock Adjustments (Periodic - As needed)**
```
Scenario:
├── Physical stock count reveals discrepancy
├── Damaged goods need to be removed
├── Expired stock needs adjustment

User Action:
├── Clicks "Adjust Stock"
├── Selects item to adjust:
│   ├── Product and variant
│   ├── Warehouse location
│   └── Current quantity shown
│
├── Enters adjustment:
│   ├── New quantity (or adjustment quantity)
│   ├── Reason for adjustment:
│   │   ├── Physical count discrepancy
│   │   ├── Damage/defect
│   │   ├── Expiration
│   │   ├── Correction (previous error)
│   │   └── Write-off
│   │
│   ├── Supporting details (notes, photos)
│   └── Requires approval for significant adjustments

Touchpoint: Adjustment Form
├── Product selector
├── Warehouse/Bin selector
├── Current stock display
├── Adjustment quantity/new quantity
├── Reason selector
├── Detailed notes
├── Photo upload
├── Approval flag
└── Submit button

Approval Workflow (for significant adjustments):
├── IF adjustment > 10% of stock:
│   └── Requires manager approval
├── IF adjustment > 25% of stock:
│   └── Requires department head approval
└── IF adjustment > 50% of stock:
    └── Requires operations director approval

Result:
├── Stock adjusted
├── Inventory history recorded
├── Valuation updated
├── Audit trail created
├── Notifications sent to affected departments
└── Financial impact calculated (for P&L)
```

**5. Inventory Reports (Weekly - 20 minutes)**
```
User Action:
├── Clicks "Reports" section
├── Selects report type:
│   ├── Inventory Summary Report
│   ├── Stock Movement Report
│   ├── ABC Analysis (Pareto)
│   ├── Inventory Turnover
│   ├── Valuation Report
│   └── Custom Report

Touchpoint: Reports Interface
├── Report selector with templates
├── Date range picker
├── Filter options (product, warehouse, category)
├── Grouping options (by product, warehouse, category)
├── Preview option
└── Download/Export buttons

Sample Report View:
├── Inventory Summary Report shows:
│   ├── Total SKUs: 234
│   ├── Total units in stock: 12,450
│   ├── Total valuation: ₹1.2 crore
│   ├── Items in low stock: 7
│   ├── Items out of stock: 2
│   ├── Stock turnover ratio: 3.2x per year
│   └── Days inventory outstanding: 112 days
│
├── By Product Category:
│   ├── Sliding Windows: ₹45 lakhs (38%)
│   ├── Casement Windows: ₹32 lakhs (27%)
│   ├── Glass: ₹25 lakhs (21%)
│   ├── Hardware: ₹18 lakhs (14%)
│   └── ...
│
└── By Warehouse:
    ├── Warehouse A: ₹70 lakhs (58%)
    ├── Warehouse B: ₹52 lakhs (42%)
    └── ...

Actions:
├── View detailed breakdown (click item)
├── Export as Excel
├── Export as PDF
├── Email report
├── Schedule recurring report
└── Share with management
```

---

## Journey Map: Admin - Analytics Review

### Scenario
Weekly strategic review by Sales Manager and Operations Manager

### Steps

**1. Sales Performance Review (15-20 minutes)**
```
Touchpoint: Sales Analytics Dashboard
├── Time period selector (this week vs last week, vs target)
├── Key metrics displayed:

Sales Metrics:
├── Total Revenue:
│   ├── This week: ₹28.5 lakhs
│   ├── Last week: ₹25.2 lakhs
│   ├── % change: +13% ✓ (Target: ₹30 lakhs)
│   └── YTD: ₹2.8 crores
│
├── Order Count:
│   ├── This week: 18 orders
│   ├── Last week: 15 orders
│   └── Avg value: ₹1.58 lakhs
│
├── Conversion Rate:
│   ├── Week: 19.2% (Target: 18%)
│   ├── Trend: ↑ (Improving)
│   └── Best performing channel: AI Chat (24%)
│
├── Sales by Category:
│   ├── Sliding Windows: ₹12.5 lakhs (44%)
│   ├── Casement Windows: ₹8.2 lakhs (29%)
│   ├── Doors: ₹5.1 lakhs (18%)
│   ├── Hardware: ₹2.7 lakhs (9%)
│   └── Chart visualization
│
├── Sales Pipeline:
│   ├── Draft quotes: 23 (value: ₹65 lakhs)
│   ├── Sent quotes: 12 (value: ₹42 lakhs)
│   ├── In negotiation: 5 (value: ₹28 lakhs)
│   ├── Ready to close: 3 (value: ₹15 lakhs)
│   └── Funnel chart showing conversion rates at each stage

User Action:
├── Reviews metrics
├── Identifies areas:
│   ├── Strong performance (AI Chat channel - 24% conversion)
│   ├── Opportunities (Negotiation stage taking too long)
│   └── Concerns (Casement windows underperforming)
│
├── Drills down on areas:
│   ├── Clicks "AI Chat" to see which products high-converting
│   ├── Clicks "Negotiation" to see deals stuck
│   └── Clicks "Casement" to analyze
│
└── Takes actions:
    ├── Schedule AI training for sales team
    ├── Review negotiation practices
    └── Plan promotional campaign for Casement Windows
```

**2. Lead Source Analysis (10-15 minutes)**
```
Touchpoint: Lead Analytics
├── Lead sources displayed:
│   ├── Website forms: 45 leads (38%) - 18% conversion
│   ├── AI Chat: 32 leads (27%) - 24% conversion ⭐
│   ├── Phone: 18 leads (15%) - 22% conversion
│   ├── Referral: 12 leads (10%) - 30% conversion ⭐⭐
│   ├── Paid ads: 8 leads (8%) - 12% conversion
│   └── Events: 3 leads (2%) - 33% conversion

Cost Analysis:
├── Website cost per lead: ₹500 (organic)
├── AI Chat cost per lead: ₹200 (already paying for AI)
├── Phone cost per lead: ₹800 (sales time)
├── Referral cost per lead: ₹1,000 (referral bonus)
├── Paid ads cost per lead: ₹2,500
├── Event cost per lead: ₹5,000

ROI Analysis:
├── Website ROI: 6.8x (low cost, decent conversion)
├── AI Chat ROI: 12x (very high) ⭐⭐
├── Referral ROI: 8.2x (high quality, higher cost)
├── Paid ads ROI: 2.1x (low efficiency)

User Action:
├── Reviews source performance
├── Decision: Increase investment in AI Chat
├── Action: Allocate more budget to AI Chat marketing
├── Decision: Reduce paid ads spend (underperforming)
└── Schedule meeting to optimize lead sources
```

**3. Customer Analytics (10-15 minutes)**
```
Touchpoint: Customer Insights Dashboard
├── Total Customers: 1,245
├── New Customers (this week): 23
├── Repeat Customer Rate: 28%
├── Average Customer Lifetime Value: ₹2.8 lakhs
├── Customer Acquisition Cost: ₹1,200

Customer Segmentation:
├── By Type:
│   ├── Residential: 856 (69%)
│   ├── Commercial: 234 (19%)
│   ├── Architect/Builder: 155 (12%)
│
├── By Segment:
│   ├── Premium: 189 customers, Avg LTV: ₹8.5 lakhs
│   ├── Standard: 678 customers, Avg LTV: ₹2.1 lakhs
│   ├── Value: 378 customers, Avg LTV: ₹1.2 lakhs
│
├── Geographic:
│   ├── Mumbai: 456 customers (37%)
│   ├── Bangalore: 234 customers (19%)
│   ├── Delhi NCR: 189 customers (15%)
│   ├── Hyderabad: 145 customers (12%)
│   ├── Other: 221 customers (17%)

Customer Health:
├── Active customers: 890 (71%)
├── At risk (no activity > 90 days): 156 (13%)
├── Churned: 199 (16%)
│
├── NPS Score: 62 (Good)
├── Satisfaction Rating: 4.3/5
├── Support tickets: 45 (avg resolution: 24h)

User Action:
├── Reviews customer metrics
├── Identifies:
│   ├── Premium segment growth (highest value)
│   ├── Geographic concentration risk (Mumbai 37%)
│   ├── At-risk customers (156 need attention)
│
├── Takes action:
│   ├── Plan expansion into Pune/Hyderabad
│   ├── Create retention program for at-risk customers
│   └── Schedule premium customer events
```

**4. Product Performance (10 minutes)**
```
Touchpoint: Product Analytics
├── Top Products (by revenue):
│   ├── Sliding Window Premium: ₹8.2 lakhs (29%)
│   ├── Casement Window Standard: ₹5.1 lakhs (18%)
│   ├── French Window Luxury: ₹4.8 lakhs (17%)
│   ├── Glass Door Commercial: ₹3.5 lakhs (12%)
│   ├── Hardware Set Premium: ₹3.2 lakhs (11%)
│   └── Others: ₹2.9 lakhs (13%)

Product Insights:
├── Best Sellers (by quantity):
│   ├── Sliding Window (all variants): 156 units
│   ├── Casement Window: 98 units
│   ├── Hardware Sets: 87 units
│   ├── Glass Sheets: 76 units
│   └── Doors: 54 units
│
├── Margin Analysis:
│   ├── Highest margin: French Window (45%)
│   ├── Lowest margin: Hardware (18%)
│   ├── Average margin: 32%
│
├── Inventory Turnover:
│   ├── Sliding Window: 4.2x/year (fast-moving)
│   ├── French Window: 2.1x/year (slow-moving)
│   └── Hardware: 6.8x/year (very fast)

Recommendations:
├── Increase production of Sliding Window (high demand)
├── Discount French Window (slow-moving, high inventory)
├── Review French Window marketing (high margin but low volume)
└── Create bundle offers combining high + low movers
```

**5. AI Usage Analytics (5 minutes)**
```
Touchpoint: AI Performance Metrics
├── AI Conversations:
│   ├── Total conversations: 1,245
│   ├── Average messages per conversation: 4.2
│   ├── Avg response time: 2.1 seconds
│   ├── User satisfaction: 4.4/5 stars
│
├── Top Questions Asked:
│   ├── "Which window for coastal area?": 234 times
│   ├── "What's the price?": 189 times
│   ├── "What's the warranty?": 167 times
│   ├── "How to install?": 145 times
│   ├── "Difference between materials?": 123 times
│
├── AI Sales Impact:
│   ├── Conversations starting quote requests: 32%
│   ├── Conversations converting to orders: 8%
│   ├── Quote value from AI-influenced: ₹15.2 lakhs (avg 1.8x higher)
│   └── AI-driven revenue: ₹12.3 lakhs (this week)

Document Usage (RAG):
├── Most used documents:
│   ├── Product Brochure: 432 references
│   ├── Installation Guide: 287 references
│   ├── Warranty Document: 156 references
│   └── FAQ: 98 references

Insights:
├── AI is high-converting channel (24% → order)
├── Cost per AI conversation: ₹45
├── ROI: 273x (excellent)
└── Recommended: Expand AI capabilities
```

**6. Report Export & Sharing (5 minutes)**
```
User Action:
├── Generates executive summary
├── Selects export format:
│   ├── PDF (for printing)
│   ├── Excel (for detailed analysis)
│   ├── PowerPoint (for presentations)
│
├── Adds custom notes/insights
├── Selects recipients:
│   ├── Executive team
│   ├── Sales team
│   ├── Operations team
│
└── Schedules email delivery

Automated Delivery:
├── Email sent with embedded charts
├── Excel attachment with raw data
├── Calendar invite for discussion meeting
└── Dashboard link shared
```

---

## Pain Points & Solutions

### Current Pain Points & How Lipu Platform Solves Them

| Pain Point | Current Situation | Lipu Solution |
|-----------|------------------|--------------|
| **Lead Qualification** | Manual filtering, slow response | AI chatbot 24/7, instant qualification |
| **Quote Generation** | Time-consuming calculations | AI-powered instant quotes |
| **Product Selection** | Overwhelming choices | AI recommendations + visualization |
| **House Visualization** | Requires site visit | AI-generated visualizations instantly |
| **Order Tracking** | Frequent customer calls | Real-time portal + SMS/Email updates |
| **Inventory Management** | Manual stock counts | Real-time tracking, automated alerts |
| **Sales Pipeline** | Scattered information | Centralized CRM with AI insights |
| **Customer Communication** | Multiple channels to manage | Unified messaging (email, SMS, WhatsApp) |
| **Pricing Consistency** | Manual price entry errors | Automated pricing engine |
| **Analytics** | Manual Excel reports | Real-time dashboards with AI insights |

---

**Document Status:** Ready for wireframe design  
**Last Updated:** 2026-06-24

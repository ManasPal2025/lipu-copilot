export interface Project {
  id: string;
  slug: string;
  title: string;
  location: string;
  type: string;
  description: string;
  windows: number;
  doors: number;
  duration: string;
  architect?: string;
  imageLabel: string;
  featured?: boolean;
}

export interface GalleryItem {
  id: string;
  title: string;
  category: string;
  location: string;
  imageLabel: string;
  span?: 'tall' | 'wide' | 'default';
}

export interface BeforeAfter {
  id: string;
  title: string;
  location: string;
  beforeLabel: string;
  afterLabel: string;
  story: string;
}

export interface DesignStyle {
  id: string;
  name: string;
  description: string;
  imageLabel: string;
  tags: string[];
}

export interface Product {
  id: string;
  slug: string;
  name: string;
  category: 'Windows' | 'Doors' | 'Facades';
  description: string;
  longDescription: string;
  fromPrice: string;
  imageLabel: string;
  specs: { label: string; value: string }[];
  highlights: string[];
}

export interface Testimonial {
  id: string;
  quote: string;
  name: string;
  location: string;
  project: string;
}

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  bio: string;
}

export interface Studio {
  city: string;
  address: string;
  hours: string;
}

export const featuredProjects: Project[] = [
  {
    id: '1',
    slug: 'coastal-residence',
    title: 'Coastal Residence',
    location: 'Alibag, Maharashtra',
    type: 'Residential',
    description:
      'Floor-to-ceiling glazing frames the Arabian Sea. Every opening engineered for salt air, acoustic silence, and an uninterrupted horizon.',
    windows: 24,
    doors: 6,
    duration: '8 weeks',
    architect: 'Studio Naqsh',
    imageLabel: 'Coastal villa — panoramic glazing at golden hour',
    featured: true,
  },
  {
    id: '2',
    slug: 'skyline-penthouse',
    title: 'Skyline Penthouse',
    location: 'Bandra West, Mumbai',
    type: 'Luxury Apartment',
    description:
      'Minimal frames. Maximum city. A complete envelope redesign that turned a dated apartment into a glass sanctuary above the bay.',
    windows: 18,
    doors: 4,
    duration: '6 weeks',
    imageLabel: 'Penthouse living room — Mumbai skyline through floor-to-ceiling glass',
    featured: true,
  },
  {
    id: '3',
    slug: 'heritage-revival',
    title: 'Heritage Revival',
    location: 'Koregaon Park, Pune',
    type: 'Renovation',
    description:
      'Colonial charm preserved. Performance upgraded. Custom profiles honour the architecture while meeting contemporary thermal standards.',
    windows: 32,
    doors: 8,
    duration: '12 weeks',
    architect: 'Red Brick Atelier',
    imageLabel: 'Restored heritage facade — European proportions, modern performance',
    featured: true,
  },
  {
    id: '4',
    slug: 'lonavala-retreat',
    title: 'Lonavala Forest Retreat',
    location: 'Lonavala, Maharashtra',
    type: 'Weekend Home',
    description:
      'A hillside home opened to the forest. Sliding portals dissolve the boundary between deck and woodland.',
    windows: 14,
    doors: 5,
    duration: '7 weeks',
    imageLabel: 'Forest retreat — glazing opening to deck and valley views',
  },
  {
    id: '5',
    slug: 'goa-villa',
    title: 'Assagao Villa',
    location: 'Assagao, Goa',
    type: 'Residential',
    description:
      'Tropical modernism with monsoon-ready engineering. Cross-ventilation designed into every elevation.',
    windows: 20,
    doors: 7,
    duration: '10 weeks',
    imageLabel: 'Goa villa — tropical modern courtyard and glazing',
  },
  {
    id: '6',
    slug: 'corporate-lobby',
    title: 'Meridian Corporate Lobby',
    location: 'BKC, Mumbai',
    type: 'Commercial',
    description:
      'A statement entrance for a financial headquarters. Structural glazing that communicates transparency and permanence.',
    windows: 8,
    doors: 12,
    duration: '14 weeks',
    imageLabel: 'Corporate lobby — structural glass entrance',
  },
];

export const galleryItems: GalleryItem[] = [
  { id: 'g1', title: 'Morning Light', category: 'Residential', location: 'Mumbai', imageLabel: 'Sunlit living room — soft morning shadows', span: 'tall' },
  { id: 'g2', title: 'Garden Portal', category: 'Doors', location: 'Pune', imageLabel: 'Garden door opening to courtyard', span: 'default' },
  { id: 'g3', title: 'Urban Edge', category: 'Commercial', location: 'Bangalore', imageLabel: 'Office facade — precision glazing grid', span: 'wide' },
  { id: 'g4', title: 'Monsoon Calm', category: 'Residential', location: 'Goa', imageLabel: 'Rain on exterior glass — monsoon resilience', span: 'default' },
  { id: 'g5', title: 'Courtyard Frame', category: 'Renovation', location: 'Jaipur', imageLabel: 'Internal courtyard — arched window rhythm', span: 'tall' },
  { id: 'g6', title: 'Dusk Silhouette', category: 'Residential', location: 'Alibag', imageLabel: 'Home at dusk — warm interior glow', span: 'wide' },
  { id: 'g7', title: 'Profile Detail', category: 'Craft', location: 'Studio', imageLabel: 'UPVC profile cross-section — engineering detail', span: 'default' },
  { id: 'g8', title: 'Stairwell Light', category: 'Residential', location: 'Delhi', imageLabel: 'Stairwell landing — vertical glazing shaft', span: 'tall' },
  { id: 'g9', title: 'Sea Horizon', category: 'Residential', location: 'Alibag', imageLabel: 'Coastal bedroom — horizon line through glass', span: 'wide' },
];

export const beforeAfterStories: BeforeAfter[] = [
  {
    id: 'ba1',
    title: 'The Bandra Transformation',
    location: 'Bandra West, Mumbai',
    beforeLabel: 'Dated aluminium frames, street noise, poor insulation',
    afterLabel: 'Slim UPVC profiles, 42dB acoustic rating, sea breeze without the salt',
    story:
      'The owners wanted light without compromise. We replaced every opening in six weeks. The home now feels twice its size — and half as loud.',
  },
  {
    id: 'ba2',
    title: 'Lonavala Retreat',
    location: 'Lonavala, Maharashtra',
    beforeLabel: 'Small windows, dark interiors, energy loss',
    afterLabel: 'Expansive glazing, passive cooling, forest views from every room',
    story:
      'A weekend home reimagined as a year-round sanctuary. Transformation started with one question: what if the forest came inside?',
  },
  {
    id: 'ba3',
    title: 'Pune Heritage Home',
    location: 'Koregaon Park, Pune',
    beforeLabel: 'Original timber frames, draughts, security concerns',
    afterLabel: 'Custom heritage profiles, multi-point locking, period-accurate sightlines',
    story:
      'Preservation and performance are not opposites. This project proved both can coexist beautifully.',
  },
];

export const designStyles: DesignStyle[] = [
  {
    id: 'ds1',
    name: 'Modern Minimal',
    description: 'Clean lines. Hidden hardware. Architecture that disappears so life takes centre stage.',
    imageLabel: 'Minimal modern interior — floor-to-ceiling glass',
    tags: ['Contemporary', 'Urban', 'High-rise'],
  },
  {
    id: 'ds2',
    name: 'European Classic',
    description: 'Proportion and craft. Profiles inspired by continental traditions, engineered for Indian climates.',
    imageLabel: 'Classic European window detail — mullion rhythm',
    tags: ['Heritage', 'Colonial', 'Boutique'],
  },
  {
    id: 'ds3',
    name: 'Coastal Resilient',
    description: 'Engineered for humidity, salt, and storms. Beauty that endures where land meets sea.',
    imageLabel: 'Coastal architecture — weather-resistant glazing',
    tags: ['Coastal', 'Tropical', 'Monsoon-ready'],
  },
  {
    id: 'ds4',
    name: 'Tropical Open',
    description: 'Indoor-outdoor living with wide spans, low thresholds, and ventilation designed into every elevation.',
    imageLabel: 'Tropical villa — open plan and garden connection',
    tags: ['Goa', 'Resort', 'Weekend homes'],
  },
];

export const products: Product[] = [
  {
    id: 'p1',
    slug: 'horizon-sliding',
    name: 'Horizon Sliding',
    category: 'Windows',
    description: 'Ultra-slim sightlines for uninterrupted views.',
    longDescription:
      'Engineered for coastal and high-rise environments. The Horizon system delivers minimal frame visibility, superior weather sealing, and effortless operation at scale.',
    fromPrice: '₹18,500',
    imageLabel: 'Horizon sliding system — slim profile detail',
    specs: [
      { label: 'Frame depth', value: '70mm' },
      { label: 'Glass', value: 'Double / Triple glazed' },
      { label: 'U-value', value: '1.2 W/m²K' },
      { label: 'Acoustic', value: 'Up to 42dB' },
    ],
    highlights: ['Coastal-rated sealing', 'Concealed rollers', '10-year hardware warranty'],
  },
  {
    id: 'p2',
    slug: 'atelier-casement',
    name: 'Atelier Casement',
    category: 'Windows',
    description: 'European-inspired casement with concealed hinges.',
    longDescription:
      'Maximum ventilation with minimal visual weight. The Atelier profile pairs continental aesthetics with multi-chamber thermal performance.',
    fromPrice: '₹16,200',
    imageLabel: 'Atelier casement — concealed hinge detail',
    specs: [
      { label: 'Frame depth', value: '68mm' },
      { label: 'Opening', value: 'Inward / Outward' },
      { label: 'Security', value: 'Multi-point locking' },
      { label: 'Finish', value: '12 colour options' },
    ],
    highlights: ['Concealed hinges', 'Heritage-compatible profiles', 'Child safety restrictors'],
  },
  {
    id: 'p3',
    slug: 'grand-entrance',
    name: 'Grand Entrance',
    category: 'Doors',
    description: 'Statement doors with multi-point locking and thermal break.',
    longDescription:
      'First impressions, perfected. Grand Entrance combines structural rigidity with elegant proportions suitable for luxury residential and boutique commercial entries.',
    fromPrice: '₹42,000',
    imageLabel: 'Grand entrance door — bronze hardware detail',
    specs: [
      { label: 'Frame depth', value: '85mm' },
      { label: 'Threshold', value: 'Low-profile option' },
      { label: 'Locking', value: '7-point system' },
      { label: 'Panel', value: 'Solid / Glazed' },
    ],
    highlights: ['Thermal break core', 'RC2 security option', 'Custom panel sizes'],
  },
  {
    id: 'p4',
    slug: 'garden-portal',
    name: 'Garden Portal',
    category: 'Doors',
    description: 'Floor-to-ceiling sliding doors that dissolve interior and landscape.',
    longDescription:
      'The Garden Portal system enables wide openings with flush thresholds. Ideal for terraces, poolsides, and courtyard connections.',
    fromPrice: '₹38,500',
    imageLabel: 'Garden portal — floor-to-ceiling sliding door',
    specs: [
      { label: 'Max span', value: '6m per panel' },
      { label: 'Threshold', value: 'Flush / Standard' },
      { label: 'Panels', value: '2–6 track' },
      { label: 'Glass', value: 'Laminated option' },
    ],
    highlights: ['Soft-close available', 'Mosquito mesh integration', 'Monsoon drainage channel'],
  },
  {
    id: 'p5',
    slug: 'facade-system',
    name: 'LIPU Facade System',
    category: 'Facades',
    description: 'Structural glazing for commercial and architectural statements.',
    longDescription:
      'A complete curtain-wall compatible system for lobbies, atriums, and landmark facades. Engineered with architects, installed with precision.',
    fromPrice: 'On consultation',
    imageLabel: 'Facade system — commercial structural glazing',
    specs: [
      { label: 'Application', value: 'Commercial / Mixed-use' },
      { label: 'Integration', value: 'Curtain wall ready' },
      { label: 'Fire rating', value: 'Project-specific' },
      { label: 'Lead time', value: '8–12 weeks' },
    ],
    highlights: ['BIM-ready documentation', 'Site engineering support', 'Performance testing'],
  },
  {
    id: 'p6',
    slug: 'skyline-fixed',
    name: 'Skyline Fixed',
    category: 'Windows',
    description: 'Picture windows with the slimmest possible sightlines.',
    longDescription:
      'When the view is the architecture. Skyline Fixed maximises glass area with structural integrity for high-rise and panoramic applications.',
    fromPrice: '₹14,800',
    imageLabel: 'Skyline fixed window — panoramic city view',
    specs: [
      { label: 'Sightline', value: '38mm visible frame' },
      { label: 'Max size', value: '3.2 × 2.8m' },
      { label: 'Glass', value: 'Up to triple glazed' },
      { label: 'Application', value: 'High-rise rated' },
    ],
    highlights: ['Panoramic applications', 'Acoustic laminate option', 'Minimal maintenance'],
  },
];

export const testimonials: Testimonial[] = [
  {
    id: 't1',
    quote:
      'We did not buy windows. We bought a completely different way of living in our home. The light alone changed everything.',
    name: 'Priya & Arjun Mehta',
    location: 'Mumbai',
    project: 'Coastal Residence',
  },
  {
    id: 't2',
    quote:
      'LIPU understood that our project was about the view, not the product catalogue. That is rare in this industry.',
    name: 'Rajesh Kulkarni',
    location: 'Pune',
    project: 'Heritage Revival',
  },
  {
    id: 't3',
    quote:
      'The visualizer let us see our home before we committed. We felt confident — not sold to.',
    name: 'Anjali Shah',
    location: 'Goa',
    project: 'Assagao Villa',
  },
  {
    id: 't4',
    quote:
      'As an architect, I specify LIPU when the envelope is part of the design narrative — not an afterthought.',
    name: 'Vikram Desai',
    location: 'Mumbai',
    project: 'Skyline Penthouse',
  },
];

export const stats = [
  { value: '2,400+', label: 'Homes transformed' },
  { value: '18', label: 'Years of craft' },
  { value: '42dB', label: 'Acoustic performance' },
  { value: '15yr', label: 'Warranty standard' },
];

export const teamMembers: TeamMember[] = [
  {
    id: 'tm1',
    name: 'Aditya Rao',
    role: 'Founder & Design Director',
    bio: 'Former architectural consultant. Believes every home has a story waiting to be revealed through light.',
  },
  {
    id: 'tm2',
    name: 'Meera Iyer',
    role: 'Head of Projects',
    bio: 'Eighteen years delivering complex residential transformations across western India.',
  },
  {
    id: 'tm3',
    name: 'Rohan Patel',
    role: 'Technical Director',
    bio: 'Engineering lead. Obsessed with acoustic performance and monsoon resilience.',
  },
];

export const studios: Studio[] = [
  { city: 'Mumbai', address: '14 Turner Road, Bandra West, Mumbai 400050', hours: 'Mon–Sat, 10am–7pm' },
  { city: 'Pune', address: '8 North Main Road, Koregaon Park, Pune 411001', hours: 'Mon–Sat, 10am–6pm' },
  { city: 'Goa', address: 'Assagao Design Studio, Mapusa Road, Assagao 403507', hours: 'Tue–Sun, 11am–6pm' },
];

export const companyValues = [
  {
    title: 'Transformation first',
    description: 'We begin every project with how you want to live — not what you want to buy.',
  },
  {
    title: 'Engineering integrity',
    description: 'European standards, tested for Indian climates. Monsoon, salt, and heat considered from day one.',
  },
  {
    title: 'Honest partnership',
    description: 'No pressure. No catalogue-first selling. Consultation before specification.',
  },
];

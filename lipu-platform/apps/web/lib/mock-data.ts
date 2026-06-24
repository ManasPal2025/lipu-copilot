import { getInspirationPhoto } from './gallery-inspiration';
import { images, type ImageAsset } from './images';
import {
  getProductInspirationImage,
  inspirationGalleryItems,
  type GalleryInspirationItem,
} from './gallery-inspiration';

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
  image: ImageAsset;
  featured?: boolean;
  pullQuote?: string;
}

export type GalleryItem = GalleryInspirationItem;

export interface BeforeAfter {
  id: string;
  title: string;
  location: string;
  beforeLabel: string;
  afterLabel: string;
  story: string;
  beforeImage: ImageAsset;
  afterImage: ImageAsset;
}

export interface DesignStyle {
  id: string;
  name: string;
  description: string;
  imageLabel: string;
  image: ImageAsset;
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
  image: ImageAsset;
  detailImage?: ImageAsset;
  specs: { label: string; value: string }[];
  highlights: string[];
}

export interface Testimonial {
  id: string;
  quote: string;
  name: string;
  location: string;
  project: string;
  image: ImageAsset;
}

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  bio: string;
  image: ImageAsset;
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
    title: 'Puri Coastal Residence',
    location: 'Puri, Odisha',
    type: 'Residential',
    description:
      'Floor-to-ceiling glazing frames the Bay of Bengal. Every opening engineered for salt air, acoustic silence, and an uninterrupted horizon.',
    windows: 24,
    doors: 6,
    duration: '8 weeks',
    architect: 'Studio Naqsh',
    imageLabel: 'Puri coastal apartment — panoramic glazing at golden hour',
    image: images.projects.coastalResidence,
    featured: true,
    pullQuote: 'The horizon became part of the living room.',
  },
  {
    id: '2',
    slug: 'skyline-penthouse',
    title: 'Patia Penthouse',
    location: 'Patia, Bhubaneswar',
    type: 'Luxury Apartment',
    description:
      'Minimal frames. Maximum city. A complete envelope redesign that turned a dated apartment into a glass sanctuary above the capital.',
    windows: 18,
    doors: 4,
    duration: '6 weeks',
    imageLabel: 'Penthouse living room — Bhubaneswar skyline through floor-to-ceiling glass',
    image: images.projects.skylinePenthouse,
    featured: true,
    pullQuote: 'Silence at forty-two decibels. City lights at full volume.',
  },
  {
    id: '3',
    slug: 'heritage-revival',
    title: 'Cuttack Heritage Revival',
    location: 'Cuttack, Odisha',
    type: 'Renovation',
    description:
      'Colonial charm preserved. Performance upgraded. Custom profiles honour the architecture while meeting contemporary thermal standards.',
    windows: 32,
    doors: 8,
    duration: '12 weeks',
    architect: 'Red Brick Atelier',
    imageLabel: 'Restored heritage facade — Indian proportions, modern performance',
    image: images.projects.heritageRevival,
    featured: true,
    pullQuote: 'Heritage preserved. Performance uncompromised.',
  },
  {
    id: '4',
    slug: 'lonavala-retreat',
    title: 'Chandaka Forest Retreat',
    location: 'Chandaka, Bhubaneswar',
    type: 'Weekend Home',
    description:
      'A hillside home opened to the forest. Sliding portals dissolve the boundary between deck and woodland.',
    windows: 14,
    doors: 5,
    duration: '7 weeks',
    imageLabel: 'Odisha forest retreat — glazing opening to deck and valley views',
    image: images.projects.lonavalaRetreat,
    pullQuote: 'The forest entered through every opening.',
  },
  {
    id: '5',
    slug: 'goa-villa',
    title: 'Konark Villa',
    location: 'Konark, Odisha',
    type: 'Residential',
    description:
      'Tropical modernism with monsoon-ready engineering. Cross-ventilation designed into every elevation.',
    windows: 20,
    doors: 7,
    duration: '10 weeks',
    imageLabel: 'Odisha coastal villa — tropical modern courtyard and glazing',
    image: images.projects.goaVilla,
  },
  {
    id: '6',
    slug: 'corporate-lobby',
    title: 'Saheed Nagar Corporate Lobby',
    location: 'Saheed Nagar, Bhubaneswar',
    type: 'Commercial',
    description:
      'A statement entrance for a financial headquarters. Structural glazing that communicates transparency and permanence.',
    windows: 8,
    doors: 12,
    duration: '14 weeks',
    imageLabel: 'Corporate lobby — structural glass entrance in Bhubaneswar',
    image: images.projects.corporateLobby,
  },
];

export const galleryItems: GalleryItem[] = inspirationGalleryItems;

export const beforeAfterStories: BeforeAfter[] = [
  {
    id: 'ba1',
    title: 'The Patia Transformation',
    location: 'Patia, Bhubaneswar',
    beforeLabel: 'Dated aluminium frames, street noise, poor insulation',
    afterLabel: 'Slim UPVC profiles, 42dB acoustic rating, sea breeze without the salt',
    story:
      'The owners wanted light without compromise. We replaced every opening in six weeks. The home now feels twice its size — and half as loud.',
    beforeImage: images.beforeAfter.bandraBefore,
    afterImage: images.beforeAfter.bandraAfter,
  },
  {
    id: 'ba2',
    title: 'Chandaka Retreat',
    location: 'Chandaka, Bhubaneswar',
    beforeLabel: 'Small windows, dark interiors, energy loss',
    afterLabel: 'Expansive glazing, passive cooling, forest views from every room',
    story:
      'A weekend home reimagined as a year-round sanctuary. Transformation started with one question: what if the forest came inside?',
    beforeImage: images.beforeAfter.lonavalaBefore,
    afterImage: images.beforeAfter.lonavalaAfter,
  },
  {
    id: 'ba3',
    title: 'Cuttack Heritage Home',
    location: 'Cuttack, Odisha',
    beforeLabel: 'Original timber frames, draughts, security concerns',
    afterLabel: 'Custom heritage profiles, multi-point locking, period-accurate sightlines',
    story:
      'Preservation and performance are not opposites. This project proved both can coexist beautifully.',
    beforeImage: images.beforeAfter.puneBefore,
    afterImage: images.beforeAfter.puneAfter,
  },
];

function styleImage(categorySlug: string, index: number, fallback: ImageAsset): ImageAsset {
  return getInspirationPhoto(categorySlug, index) ?? fallback;
}

export const designStyles: DesignStyle[] = [
  {
    id: 'ds1',
    name: 'Modern Minimal',
    description: 'Clean lines. Hidden hardware. Architecture that disappears so life takes centre stage.',
    imageLabel: 'Minimal modern interior — floor-to-ceiling glass',
    image: styleImage('living-room', 8, images.designStyles.modernMinimal),
    tags: ['Contemporary', 'Urban', 'High-rise'],
  },
  {
    id: 'ds2',
    name: 'European Classic',
    description: 'Proportion and craft. Profiles inspired by continental traditions, engineered for Indian climates.',
    imageLabel: 'French doors opening to a garden terrace',
    image: styleImage('french-door', 3, images.designStyles.europeanClassic),
    tags: ['Heritage', 'Colonial', 'Boutique'],
  },
  {
    id: 'ds3',
    name: 'Coastal Resilient',
    description: 'Engineered for humidity, salt, and storms. Beauty that endures where land meets sea.',
    imageLabel: 'Coastal villa with wide glazing and natural light',
    image: styleImage('villa', 4, images.designStyles.coastalResilient),
    tags: ['Coastal', 'Tropical', 'Monsoon-ready'],
  },
  {
    id: 'ds4',
    name: 'Tropical Open',
    description: 'Indoor-outdoor living with wide spans, low thresholds, and ventilation designed into every elevation.',
    imageLabel: 'Balcony connected to indoor living through sliding glass',
    image: styleImage('balcony', 2, images.designStyles.tropicalOpen),
    tags: ['Puri', 'Coastal', 'Weekend homes'],
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
    imageLabel: 'Balcony sliding doors in a real Indian home',
    image: getProductInspirationImage('horizon-sliding'),
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
    imageLabel: 'Casement windows in a bright bedroom',
    image: getProductInspirationImage('atelier-casement'),
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
    imageLabel: 'French doors opening to a garden terrace',
    image: getProductInspirationImage('grand-entrance'),
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
    imageLabel: 'Living room connected to the garden through sliding doors',
    image: getProductInspirationImage('garden-portal'),
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
    imageLabel: 'Commercial building with structural glass facade',
    image: getProductInspirationImage('facade-system'),
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
    imageLabel: 'Apartment living room with panoramic fixed windows',
    image: getProductInspirationImage('skyline-fixed'),
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
    name: 'Priya & Arjun Das',
    location: 'Puri',
    project: 'Puri Coastal Residence',
    image: images.projects.coastalResidence,
  },
  {
    id: 't2',
    quote:
      'LIPU understood that our project was about the view, not the product catalogue. That is rare in this industry.',
    name: 'Rajesh Mohanty',
    location: 'Cuttack',
    project: 'Cuttack Heritage Revival',
    image: images.projects.heritageRevival,
  },
  {
    id: 't3',
    quote:
      'The visualizer let us see our home before we committed. We felt confident — not sold to.',
    name: 'Anjali Patnaik',
    location: 'Konark',
    project: 'Konark Villa',
    image: images.projects.goaVilla,
  },
  {
    id: 't4',
    quote:
      'As an architect, I specify LIPU when the envelope is part of the design narrative — not an afterthought.',
    name: 'Vikram Sahu',
    location: 'Bhubaneswar',
    project: 'Patia Penthouse',
    image: images.projects.skylinePenthouse,
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
    image: images.team.aditya,
  },
  {
    id: 'tm2',
    name: 'Meera Iyer',
    role: 'Head of Projects',
    bio: 'Eighteen years delivering complex residential transformations across Odisha and eastern India.',
    image: images.team.meera,
  },
  {
    id: 'tm3',
    name: 'Rohan Patel',
    role: 'Technical Director',
    bio: 'Engineering lead. Obsessed with acoustic performance and monsoon resilience.',
    image: images.team.rohan,
  },
];

export const studios: Studio[] = [
  { city: 'Bhubaneswar', address: 'Plot 14, Saheed Nagar, Bhubaneswar 751007', hours: 'Mon–Sat, 10am–7pm' },
  { city: 'Cuttack', address: '8 Buxi Bazaar, Cuttack 753001', hours: 'Mon–Sat, 10am–6pm' },
  { city: 'Puri', address: 'Marine Drive Design Studio, Puri 752001', hours: 'Tue–Sun, 11am–6pm' },
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

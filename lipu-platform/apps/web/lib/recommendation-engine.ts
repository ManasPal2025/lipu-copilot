import { getInspirationCategory, getInspirationPhoto, type InspirationCategory } from '@/lib/gallery-inspiration';
import type { ImageAsset } from '@/lib/images';
import { products, type Product } from '@/lib/mock-data';

export type PropertyType = 'apartment' | 'villa';
export type RoomType = 'living-room' | 'balcony' | 'kitchen' | 'bedroom' | 'entrance';
export type NoiseLevel = 'low' | 'medium' | 'high';
export type HeatExposure = 'low' | 'medium' | 'high';
export type BudgetRange = 'under-20k' | '20k-35k' | '35k-50k' | '50k-plus';

export interface WizardAnswers {
  propertyType: PropertyType;
  roomType: RoomType;
  noiseLevel: NoiseLevel;
  heatExposure: HeatExposure;
  budget: BudgetRange;
}

export interface WizardRecommendation {
  product: Product;
  matchScore: number;
  headline: string;
  reasons: string[];
  inspirationPhotos: ImageAsset[];
  galleryCategory: InspirationCategory | undefined;
  galleryHref: string;
}

const ROOM_GALLERY: Record<RoomType, string> = {
  'living-room': 'living-room',
  balcony: 'balcony',
  kitchen: 'kitchen',
  bedroom: 'bedroom',
  entrance: 'french-door',
};

const ROOM_PRODUCT_WEIGHTS: Record<RoomType, Partial<Record<string, number>>> = {
  'living-room': {
    'garden-portal': 4,
    'skyline-fixed': 3,
    'horizon-sliding': 2,
  },
  balcony: {
    'horizon-sliding': 5,
    'garden-portal': 2,
    'skyline-fixed': 1,
  },
  kitchen: {
    'atelier-casement': 5,
    'horizon-sliding': 2,
  },
  bedroom: {
    'atelier-casement': 4,
    'skyline-fixed': 3,
    'horizon-sliding': 2,
  },
  entrance: {
    'grand-entrance': 5,
    'garden-portal': 2,
  },
};

const PRODUCT_MIN_PRICE: Record<string, number> = {
  'skyline-fixed': 14800,
  'atelier-casement': 16200,
  'horizon-sliding': 18500,
  'garden-portal': 38500,
  'grand-entrance': 42000,
  'facade-system': 100000,
};

const BUDGET_CEILING: Record<BudgetRange, number> = {
  'under-20k': 20000,
  '20k-35k': 35000,
  '35k-50k': 50000,
  '50k-plus': Infinity,
};

function scoreProduct(slug: string, answers: WizardAnswers): number {
  let score = 0;

  score += ROOM_PRODUCT_WEIGHTS[answers.roomType][slug] ?? 0;

  if (answers.propertyType === 'apartment') {
    if (slug === 'skyline-fixed' || slug === 'horizon-sliding') score += 2;
    if (slug === 'garden-portal' || slug === 'grand-entrance') score -= 1;
  } else {
    if (slug === 'garden-portal' || slug === 'grand-entrance') score += 3;
    if (slug === 'facade-system') score += 1;
  }

  if (answers.noiseLevel === 'high') {
    if (slug === 'horizon-sliding' || slug === 'atelier-casement') score += 3;
    if (slug === 'skyline-fixed') score += 1;
  } else if (answers.noiseLevel === 'medium') {
    if (slug === 'atelier-casement' || slug === 'horizon-sliding') score += 2;
  } else if (slug === 'skyline-fixed') {
    score += 1;
  }

  if (answers.heatExposure === 'high') {
    if (slug === 'atelier-casement' || slug === 'horizon-sliding' || slug === 'garden-portal') score += 3;
    if (slug === 'grand-entrance') score += 2;
  } else if (answers.heatExposure === 'medium') {
    if (slug === 'atelier-casement' || slug === 'horizon-sliding') score += 1;
  }

  const minPrice = PRODUCT_MIN_PRICE[slug] ?? 0;
  const ceiling = BUDGET_CEILING[answers.budget];
  if (minPrice <= ceiling) {
    score += 2;
  } else {
    score -= 4;
  }

  if (answers.budget === 'under-20k' && (slug === 'skyline-fixed' || slug === 'atelier-casement')) {
    score += 2;
  }
  if (answers.budget === '50k-plus' && (slug === 'grand-entrance' || slug === 'garden-portal')) {
    score += 2;
  }

  return score;
}

function buildReasons(product: Product, answers: WizardAnswers): string[] {
  const reasons: string[] = [];

  const roomLabels: Record<RoomType, string> = {
    'living-room': 'living room',
    balcony: 'balcony',
    kitchen: 'kitchen',
    bedroom: 'bedroom',
    entrance: 'entrance',
  };

  reasons.push(`Suited for ${roomLabels[answers.roomType]} installations in Odisha homes.`);

  if (answers.propertyType === 'apartment') {
    reasons.push('Compact profiles and sliding options work well in apartment layouts.');
  } else {
    reasons.push('Wide spans and statement doors suit villa-scale openings.');
  }

  if (answers.noiseLevel === 'high') {
    reasons.push('Multi-chamber frames and acoustic glass options help cut street and neighbour noise.');
  } else if (answers.noiseLevel === 'medium') {
    reasons.push('Balanced acoustic performance for typical urban and residential noise.');
  } else {
    reasons.push('Clean sightlines and daylight without over-specifying acoustic layers.');
  }

  if (answers.heatExposure === 'high') {
    reasons.push('Double or triple glazing and thermal break profiles reduce heat gain in sunny rooms.');
  } else if (answers.heatExposure === 'medium') {
    reasons.push('Reliable thermal performance for rooms that warm up through the day.');
  } else {
    reasons.push('Efficient glazing without unnecessary cost for shaded or cooler rooms.');
  }

  reasons.push(`Fits your budget band — from ${product.fromPrice} per opening.`);

  return reasons.slice(0, 4);
}

function buildHeadline(product: Product, answers: WizardAnswers): string {
  const roomLabels: Record<RoomType, string> = {
    'living-room': 'living room',
    balcony: 'balcony',
    kitchen: 'kitchen',
    bedroom: 'bedroom',
    entrance: 'entrance',
  };

  return `${product.name} for your ${answers.propertyType === 'apartment' ? 'apartment' : 'villa'} ${roomLabels[answers.roomType]}`;
}

export function getRecommendation(answers: WizardAnswers): WizardRecommendation {
  const scored = products
    .filter((p) => p.slug !== 'facade-system')
    .map((product) => ({
      product,
      score: scoreProduct(product.slug, answers),
    }))
    .sort((a, b) => b.score - a.score);

  const top = scored[0]?.product ?? products[0];
  const gallerySlug = ROOM_GALLERY[answers.roomType];
  const galleryCategory = getInspirationCategory(gallerySlug);

  const inspirationPhotos = [1, 2, 3]
    .map((index) => getInspirationPhoto(gallerySlug, index))
    .filter((photo): photo is ImageAsset => photo !== undefined);

  return {
    product: top,
    matchScore: scored[0]?.score ?? 0,
    headline: buildHeadline(top, answers),
    reasons: buildReasons(top, answers),
    inspirationPhotos,
    galleryCategory,
    galleryHref: `/gallery#${gallerySlug}`,
  };
}

export const WIZARD_STEPS = [
  {
    id: 'propertyType',
    title: 'Apartment or villa?',
    description: 'We tailor profiles to how your home is built — tower flat or standalone villa.',
  },
  {
    id: 'roomType',
    title: 'Which room are you planning for?',
    description: 'Pick the space you want ideas for first.',
  },
  {
    id: 'noiseLevel',
    title: 'How much outside noise do you hear?',
    description: 'Road traffic, neighbours, and market noise all matter in Bhubaneswar and Cuttack.',
  },
  {
    id: 'heatExposure',
    title: 'How much sun and heat does the room get?',
    description: 'West-facing balconies and top-floor rooms need different glazing choices.',
  },
  {
    id: 'budget',
    title: 'What is your budget per opening?',
    description: 'A ballpark per window or door helps us suggest the right profile — not a final quote.',
  },
] as const;

export const WIZARD_OPTIONS = {
  propertyType: [
    { value: 'apartment' as const, label: 'Apartment', description: 'Flat or high-rise home in the city' },
    { value: 'villa' as const, label: 'Villa', description: 'Independent house, duplex, or gated villa' },
  ],
  roomType: [
    { value: 'living-room' as const, label: 'Living room', description: 'Main family space and daylight' },
    { value: 'balcony' as const, label: 'Balcony', description: 'Sliding doors and outdoor connection' },
    { value: 'kitchen' as const, label: 'Kitchen', description: 'Ventilation and practical openings' },
    { value: 'bedroom' as const, label: 'Bedroom', description: 'Quiet, comfortable sleep spaces' },
    { value: 'entrance' as const, label: 'Entrance', description: 'Front door or French door entry' },
  ],
  noiseLevel: [
    { value: 'low' as const, label: 'Quiet', description: 'Internal rooms or calm neighbourhood' },
    { value: 'medium' as const, label: 'Moderate', description: 'Some traffic or shared-wall noise' },
    { value: 'high' as const, label: 'High', description: 'Main road, market, or busy street nearby' },
  ],
  heatExposure: [
    { value: 'low' as const, label: 'Low', description: 'Shaded, north-facing, or ground floor' },
    { value: 'medium' as const, label: 'Medium', description: 'Gets warm afternoon sun sometimes' },
    { value: 'high' as const, label: 'High', description: 'West-facing, top floor, or full-day sun' },
  ],
  budget: [
    { value: 'under-20k' as const, label: 'Under ₹20,000', description: 'Essential profiles for compact spaces' },
    { value: '20k-35k' as const, label: '₹20,000 – ₹35,000', description: 'Balanced performance and finish' },
    { value: '35k-50k' as const, label: '₹35,000 – ₹50,000', description: 'Wide spans and premium sliding systems' },
    { value: '50k-plus' as const, label: '₹50,000+', description: 'Statement doors and villa-scale openings' },
  ],
} as const;

import cityStyleMap from '@/config/city-style-map.json';
import type { ImageAsset } from '@/lib/images';

export type CityId = keyof typeof cityStyleMap.cities;

export type ImageCategory = (typeof cityStyleMap.imageCategories)[number];

export type CityCopyKey = keyof CityStyle['copy'];

export interface CityColorPalette {
  primary: string;
  accent: string;
  neutral: string;
  surface: string;
}

export interface CityImageRef {
  path: string;
  alt: string;
}

export interface CityStyle {
  label: string;
  state: string;
  region: string;
  architectureType: string;
  styleKeywords: string[];
  colorPalette: CityColorPalette;
  images: Record<ImageCategory, CityImageRef>;
  copy: {
    heroEyebrow: string;
    heroSubline: string;
    visualizerTitle: string;
    visualizerDescription: string;
    ctaTitle: string;
    seoHeadline: string;
  };
}

const STORAGE_KEY = 'lipu-selected-city';

const cityEntries = Object.entries(cityStyleMap.cities) as [CityId, CityStyle][];

export function getCityStyleMap() {
  return cityStyleMap;
}

export function getDefaultCityId(): CityId {
  return cityStyleMap.defaultCity as CityId;
}

export function normalizeCityId(input: string | null | undefined): CityId {
  if (!input) return getDefaultCityId();

  const slug = input.trim().toLowerCase().replace(/\s+/g, '-');
  const aliases: Record<string, CityId> = {
    bhubaneswar: 'bhubaneswar',
    bbsr: 'bhubaneswar',
    cuttack: 'cuttack',
    puri: 'puri',
    kolkata: 'kolkata',
    calcutta: 'kolkata',
    delhi: 'delhi',
    'delhi-ncr': 'delhi',
    ncr: 'delhi',
    mumbai: 'mumbai',
    bombay: 'mumbai',
    chennai: 'chennai',
    madras: 'chennai',
    bangalore: 'bangalore',
    bengaluru: 'bangalore',
    other: 'other',
  };

  if (aliases[slug]) return aliases[slug];
  if (slug in cityStyleMap.cities) return slug as CityId;

  return getDefaultCityId();
}

export function getSupportedCities(): { id: CityId; label: string; state: string }[] {
  return cityEntries.map(([id, style]) => ({
    id,
    label: style.label,
    state: style.state,
  }));
}

export function getCityStyle(cityId?: string | null): CityStyle {
  const id = normalizeCityId(cityId);
  return cityStyleMap.cities[id];
}

export function getCityArchitectureType(cityId?: string | null): string {
  return getCityStyle(cityId).architectureType;
}

export function getCityColorPalette(cityId?: string | null): CityColorPalette {
  return getCityStyle(cityId).colorPalette;
}

export function getCityCopy(cityId: string | null | undefined, key: CityCopyKey): string {
  return getCityStyle(cityId).copy[key];
}

export function getCityImageRef(
  cityId: string | null | undefined,
  category: ImageCategory,
): CityImageRef {
  const style = getCityStyle(cityId);
  return style.images[category] ?? style.images.hero;
}

export function getCityImage(
  cityId: string | null | undefined,
  category: ImageCategory,
): ImageAsset {
  const ref = getCityImageRef(cityId, category);
  return {
    src: `/images/${ref.path}`,
    alt: ref.alt,
  };
}

export function readStoredCityId(): CityId | null {
  if (typeof window === 'undefined') return null;
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return stored ? normalizeCityId(stored) : null;
  } catch {
    return null;
  }
}

export function writeStoredCityId(cityId: CityId): void {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(STORAGE_KEY, cityId);
  } catch {
    // ignore quota / private mode
  }
}

export const CITY_STORAGE_KEY = STORAGE_KEY;

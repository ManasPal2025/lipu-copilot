import inspirationMap from '@/config/gallery-inspiration-map.json';
import type { ImageAsset } from '@/lib/images';

export interface InspirationPhoto {
  file: string;
  pexelsId: number;
  title: string;
  alt: string;
}

export interface InspirationCategory {
  slug: string;
  title: string;
  subtitle: string;
  description: string;
  photos: InspirationPhoto[];
}

export interface GalleryInspirationItem {
  id: string;
  title: string;
  category: string;
  categorySlug: string;
  categorySubtitle: string;
  location: string;
  imageLabel: string;
  image: ImageAsset;
  span: 'tall' | 'wide' | 'default';
}

const ODISHA_LOCATIONS = ['Bhubaneswar', 'Cuttack', 'Puri', 'Patia', 'Chandaka', 'Konark'] as const;

const spanPattern: GalleryInspirationItem['span'][] = ['default', 'tall', 'default', 'wide', 'default', 'tall', 'default', 'default', 'wide', 'tall'];

export const inspirationCategories: InspirationCategory[] = inspirationMap.categories;

export function inspirationImagePath(categorySlug: string, file: string): string {
  return `/images/inspiration/${categorySlug}/${file}`;
}

export function buildInspirationGalleryItems(): GalleryInspirationItem[] {
  const items: GalleryInspirationItem[] = [];
  let index = 0;

  for (const category of inspirationCategories) {
    category.photos.forEach((photo, photoIndex) => {
      items.push({
        id: `insp-${category.slug}-${photoIndex + 1}`,
        title: photo.title,
        category: category.title,
        categorySlug: category.slug,
        categorySubtitle: category.subtitle,
        location: ODISHA_LOCATIONS[index % ODISHA_LOCATIONS.length],
        imageLabel: photo.alt,
        image: {
          src: inspirationImagePath(category.slug, photo.file),
          alt: photo.alt,
        },
        span: spanPattern[photoIndex % spanPattern.length],
      });
      index += 1;
    });
  }

  return items;
}

export const inspirationGalleryItems = buildInspirationGalleryItems();

export function getInspirationCategory(slug: string): InspirationCategory | undefined {
  return inspirationCategories.find((c) => c.slug === slug);
}

export function getInspirationPhoto(categorySlug: string, fileIndex: number): ImageAsset | undefined {
  const category = getInspirationCategory(categorySlug);
  const photo = category?.photos[fileIndex - 1];
  if (!photo) return undefined;
  return {
    src: inspirationImagePath(categorySlug, photo.file),
    alt: photo.alt,
  };
}

const DEFAULT_INSPIRATION: ImageAsset = {
  src: '/images/inspiration/living-room/01.jpg',
  alt: 'Bright Indian living room with natural light through UPVC windows',
};

function inspirationPhotoOrDefault(categorySlug: string, fileIndex: number): ImageAsset {
  return getInspirationPhoto(categorySlug, fileIndex) ?? DEFAULT_INSPIRATION;
}

/** Lifestyle image for a product line — always a complete room/home, never a product macro. */
export function getProductInspirationImage(productSlug: string): ImageAsset {
  const map: Record<string, ImageAsset> = {
    'horizon-sliding': inspirationPhotoOrDefault('balcony', 1),
    'atelier-casement': inspirationPhotoOrDefault('bedroom', 1),
    'grand-entrance': inspirationPhotoOrDefault('french-door', 1),
    'garden-portal': inspirationPhotoOrDefault('living-room', 2),
    'facade-system': inspirationPhotoOrDefault('commercial', 1),
    'skyline-fixed': inspirationPhotoOrDefault('apartment', 5),
  };
  return map[productSlug] ?? DEFAULT_INSPIRATION;
}

export const TOTAL_INSPIRATION_PHOTOS = inspirationCategories.reduce(
  (sum, c) => sum + c.photos.length,
  0,
);

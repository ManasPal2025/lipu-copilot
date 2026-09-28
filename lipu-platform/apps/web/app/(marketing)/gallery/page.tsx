import type { Metadata } from 'next';

import {
  GalleryCollection,
  GalleryConsultation,
  GalleryHero,
} from '@/components/marketing/gallery-sections';

export const metadata: Metadata = {
  title: 'Gallery',
  description:
    'A curated visual collection of homes, workplaces, and outdoor spaces — from Ecotech Window Systems.',
};

export default function GalleryPage() {
  return (
    <>
      <GalleryHero />
      <GalleryCollection />
      <GalleryConsultation />
    </>
  );
}

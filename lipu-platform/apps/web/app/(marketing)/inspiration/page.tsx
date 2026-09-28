import type { Metadata } from 'next';

import {
  InspirationChapters,
  InspirationConsultation,
  InspirationEditorial,
  InspirationFeatured,
  InspirationHero,
  InspirationIntro,
  InspirationTransform,
} from '@/components/marketing/inspiration-sections';

export const metadata: Metadata = {
  title: 'Inspiration',
  description:
    'Editorial inspiration for living, sleeping, balconies, terraces, villas, and commercial spaces — from Ecotech Window Systems.',
};

export default function InspirationPage() {
  return (
    <>
      <InspirationHero />
      <InspirationIntro />
      <InspirationChapters />
      <InspirationEditorial />
      <InspirationFeatured />
      <InspirationTransform />
      <InspirationConsultation />
    </>
  );
}

import type { Metadata } from 'next';

import { HeroSection } from '@/components/marketing/hero-section';
import { HomeConsultationSection } from '@/components/marketing/home-consultation';
import { HomeInspirationSection } from '@/components/marketing/home-inspiration';
import { HomeOfferingsSection } from '@/components/marketing/home-offerings';
import { HomePossibilitiesSection } from '@/components/marketing/home-possibilities';
import { HomeProductsSection } from '@/components/marketing/home-products';
import { HomeTransformSection } from '@/components/marketing/home-transform';

export const metadata: Metadata = {
  title: 'Home',
  description:
    'Ecotech Window Systems — premium UPVC windows, doors, and architectural spaces for homes and projects across Odisha.',
};

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <HomeOfferingsSection />
      <HomePossibilitiesSection />
      <HomeProductsSection />
      <HomeInspirationSection />
      <HomeTransformSection />
      <HomeConsultationSection />
    </>
  );
}

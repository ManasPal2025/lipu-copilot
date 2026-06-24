import type { Metadata } from 'next';

import { AIVisualizerSection } from '@/components/marketing/ai-visualizer';
import { BeforeAfterSection } from '@/components/marketing/before-after';
import { DesignInspirationSection } from '@/components/marketing/design-inspiration';
import { EditorialStrip } from '@/components/marketing/editorial-strip';
import { FeaturedProjectsSection } from '@/components/marketing/featured-projects';
import { HeroSection } from '@/components/marketing/hero-section';
import { HeroStatsStrip } from '@/components/marketing/hero-stats-strip';
import { ProductDiscoverySection } from '@/components/marketing/product-discovery';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { TestimonialsSection } from '@/components/marketing/testimonials';
import { TransformationSection } from '@/components/marketing/transformation-section';

export const metadata: Metadata = {
  title: 'Home Transformation',
  description:
    'Premium UPVC windows and doors for architectural home transformation. Experience your home before you build it.',
};

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <HeroStatsStrip />
      <TransformationSection />
      <FeaturedProjectsSection />
      <EditorialStrip />
      <BeforeAfterSection />
      <DesignInspirationSection />
      <AIVisualizerSection />
      <ProductDiscoverySection />
      <TestimonialsSection />
      <QuoteCTASection />
    </>
  );
}

import type { Metadata } from 'next';
import Link from 'next/link';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { ProductsCatalog } from '@/components/marketing/products-catalog';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images } from '@/lib/images';
import { products } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Products',
  description:
    'Premium UPVC window and door systems — Horizon, Atelier, Grand Entrance, and more. Engineered for Indian climates.',
};

export default function ProductsPage() {
  return (
    <>
      <PageHero
        eyebrow="Systems & profiles"
        title="Engineered for the vision"
        description="Every profile is built for performance — thermal, acoustic, and monsoon resilience. Specification follows consultation, never the reverse."
        image={images.pageHero.products}
      />

      <Section>
        <Container>
          <FadeIn>
            <p className="mb-4 max-w-2xl text-muted-foreground editorial-prose">
              Profiles are specified after consultation — never before. Explore our systems to understand what
              becomes possible when craft meets climate.
            </p>
          </FadeIn>

          <ProductsCatalog products={products} />

          <FadeIn>
            <div className="relative mt-20 overflow-hidden rounded-sm lg:mt-28">
              <ArchitecturalImage
                src={images.products.horizonDetail.src}
                alt=""
                aspect="wide"
                className="opacity-25"
                sizes="100vw"
              />
              <div className="absolute inset-0 bg-background/88" />
              <div className="relative p-10 text-center sm:p-16 lg:p-20">
                <h2 className="font-display text-3xl sm:text-4xl">Not sure which system fits?</h2>
                <p className="mx-auto mt-4 max-w-lg text-muted-foreground editorial-prose">
                  Our consultants match profiles to your architecture, climate, and lifestyle — not a catalogue page.
                </p>
                <Button variant="accent" className="mt-8" size="lg" asChild>
                  <Link href="/contact#quote">Book a specification review</Link>
                </Button>
              </div>
            </div>
          </FadeIn>
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

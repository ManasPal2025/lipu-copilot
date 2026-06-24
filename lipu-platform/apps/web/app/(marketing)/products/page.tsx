import type { Metadata } from 'next';
import Link from 'next/link';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { ProductCard } from '@/components/marketing/product-card';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { Button } from '@/components/ui/button';
import { products } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Products',
  description:
    'Premium UPVC window and door systems — Horizon, Atelier, Grand Entrance, and more. Engineered for Indian climates.',
};

const categories = ['All', 'Windows', 'Doors', 'Facades'] as const;

export default function ProductsPage() {
  return (
    <>
      <PageHero
        eyebrow="Systems & profiles"
        title="Engineered for the vision"
        description="Every profile is built for performance — thermal, acoustic, and monsoon resilience. Specification follows consultation, never the reverse."
      />

      <Section>
        <Container>
          <FadeIn>
            <div className="mb-12 flex flex-wrap gap-3">
              {categories.map((cat) => (
                <Button key={cat} variant={cat === 'All' ? 'default' : 'outline'} size="sm">
                  {cat}
                </Button>
              ))}
            </div>
          </FadeIn>

          <div className="space-y-0">
            {products.map((product, i) => (
              <FadeIn key={product.id} delay={i * 0.05}>
                <ProductCard product={product} layout="list" />
              </FadeIn>
            ))}
          </div>

          <FadeIn>
            <div className="mt-16 rounded-sm border border-border bg-muted/40 p-8 text-center sm:p-12">
              <h2 className="font-display text-2xl sm:text-3xl">Not sure which system fits?</h2>
              <p className="mx-auto mt-3 max-w-lg text-muted-foreground">
                Our consultants match profiles to your architecture, climate, and lifestyle — not a catalogue page.
              </p>
              <Button variant="accent" className="mt-6" asChild>
                <Link href="/contact#quote">Book a specification review</Link>
              </Button>
            </div>
          </FadeIn>
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

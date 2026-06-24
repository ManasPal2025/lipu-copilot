import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ProductCard } from '@/components/marketing/product-card';
import { Button } from '@/components/ui/button';
import { products } from '@/lib/mock-data';

export function ProductDiscoverySection() {
  return (
    <Section className="bg-muted/15">
      <Container>
        <FadeIn>
          <div className="flex flex-col gap-8 sm:flex-row sm:items-end sm:justify-between">
            <SectionHeader
              eyebrow="When you are ready"
              title="See it in a real home first"
              description="Start with inspiration — then explore UPVC systems that match the rooms and styles you love."
              className="mb-0"
            />
            <Button variant="outline" asChild className="mb-12 shrink-0">
              <Link href="/products">
                Explore systems
                <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </FadeIn>

        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
          {products.slice(0, 4).map((product, i) => (
            <FadeIn key={product.id} delay={i * 0.08}>
              <ProductCard product={product} />
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ProductCard } from '@/components/marketing/product-card';
import { Button } from '@/components/ui/button';
import { products } from '@/lib/mock-data';

export function ProductDiscoverySection() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
            <SectionHeader
              eyebrow="When you are ready"
              title="Engineered for performance"
              description="Products matter — after the vision is clear. Explore our range when transformation leads the conversation."
            />
            <Button variant="outline" asChild className="shrink-0">
              <Link href="/products">
                Full catalogue
                <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </FadeIn>

        <div className="mt-4 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
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

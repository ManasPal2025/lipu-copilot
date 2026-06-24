'use client';

import { useState } from 'react';

import { FadeIn } from '@/components/motion/fade-in';
import { ProductCard } from '@/components/marketing/product-card';
import type { Product } from '@/lib/mock-data';
import { cn } from '@/lib/utils';

const categories = ['All', 'Windows', 'Doors', 'Facades'] as const;
type Category = (typeof categories)[number];

interface ProductsCatalogProps {
  products: Product[];
}

export function ProductsCatalog({ products }: ProductsCatalogProps) {
  const [active, setActive] = useState<Category>('All');

  const filtered =
    active === 'All' ? products : products.filter((p) => p.category === active);

  return (
    <>
      <FadeIn>
        <div className="mb-16 flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setActive(cat)}
              className={cn(
                'rounded-full border px-5 py-2 text-xs uppercase tracking-wider transition-colors',
                active === cat
                  ? 'border-foreground bg-foreground text-background'
                  : 'border-border text-muted-foreground hover:border-foreground/40 hover:text-foreground',
              )}
            >
              {cat}
            </button>
          ))}
        </div>
      </FadeIn>

      <div className="space-y-0">
        {filtered.map((product, i) => (
          <FadeIn key={product.id} delay={i * 0.05}>
            <ProductCard product={product} layout="showcase" />
          </FadeIn>
        ))}
      </div>
    </>
  );
}

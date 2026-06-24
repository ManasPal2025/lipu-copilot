import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { ImagePlaceholder } from '@/components/layout/section';
import { Button } from '@/components/ui/button';
import type { Product } from '@/lib/mock-data';

interface ProductCardProps {
  product: Product;
  layout?: 'grid' | 'list';
}

export function ProductCard({ product, layout = 'grid' }: ProductCardProps) {
  if (layout === 'list') {
    return (
      <article className="grid gap-6 border-t border-border py-12 first:border-t-0 first:pt-0 lg:grid-cols-2 lg:gap-16">
        <ImagePlaceholder label={product.imageLabel} aspect="portrait" />
        <div className="flex flex-col justify-center">
          <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">{product.category}</p>
          <h2 className="mt-2 font-display text-3xl sm:text-4xl">{product.name}</h2>
          <p className="mt-4 text-muted-foreground leading-relaxed">{product.longDescription}</p>
          <ul className="mt-6 space-y-2">
            {product.highlights.map((h) => (
              <li key={h} className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="h-1 w-1 rounded-full bg-accent" />
                {h}
              </li>
            ))}
          </ul>
          <div className="mt-6 grid grid-cols-2 gap-4 border-t border-border pt-6 sm:grid-cols-4">
            {product.specs.map((spec) => (
              <div key={spec.label}>
                <p className="text-xs uppercase tracking-wider text-muted-foreground">{spec.label}</p>
                <p className="mt-1 text-sm font-medium">{spec.value}</p>
              </div>
            ))}
          </div>
          <div className="mt-8 flex flex-wrap items-center gap-4">
            <p className="text-sm font-medium">From {product.fromPrice}</p>
            <Button variant="outline" asChild>
              <Link href="/contact#quote">Discuss this profile</Link>
            </Button>
          </div>
        </div>
      </article>
    );
  }

  return (
    <Link href="/products" className="group block">
      <ImagePlaceholder label={product.imageLabel} aspect="portrait" />
      <div className="mt-4">
        <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">{product.category}</p>
        <div className="mt-1 flex items-start justify-between gap-2">
          <h3 className="font-display text-xl group-hover:text-accent">{product.name}</h3>
          <ArrowUpRight className="h-4 w-4 shrink-0 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
        </div>
        <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">{product.description}</p>
        <p className="mt-3 text-sm font-medium">From {product.fromPrice}</p>
      </div>
    </Link>
  );
}

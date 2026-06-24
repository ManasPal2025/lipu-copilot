import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { ImageZoom } from '@/components/motion/image-zoom';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import type { Product } from '@/lib/mock-data';

interface ProductCardProps {
  product: Product;
  layout?: 'grid' | 'list' | 'showcase';
}

export function ProductCard({ product, layout = 'grid' }: ProductCardProps) {
  if (layout === 'list' || layout === 'showcase') {
    return (
      <article className="grid gap-10 border-t border-border py-16 first:border-t-0 first:pt-0 lg:grid-cols-12 lg:gap-16 lg:py-24">
        <div className="space-y-4 lg:col-span-7">
          <ImageZoom>
            <ArchitecturalImage
              src={product.image.src}
              alt={product.image.alt}
              aspect="wide"
              sizes="(max-width: 1024px) 100vw, 58vw"
            />
          </ImageZoom>
        </div>
        <div className="flex flex-col justify-center lg:col-span-5">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{product.category}</p>
          <h2 className="mt-3 font-display text-3xl sm:text-4xl lg:text-5xl">{product.name}</h2>
          <p className="mt-5 text-muted-foreground leading-relaxed editorial-prose">{product.longDescription}</p>
          <ul className="mt-8 space-y-3">
            {product.highlights.map((h) => (
              <li key={h} className="flex items-center gap-3 text-sm text-muted-foreground">
                <span className="h-1 w-1 shrink-0 rounded-full bg-accent" />
                {h}
              </li>
            ))}
          </ul>
          <div className="mt-8 grid grid-cols-2 gap-6 border-t border-border pt-8 sm:grid-cols-4">
            {product.specs.map((spec) => (
              <div key={spec.label}>
                <p className="text-[10px] uppercase tracking-[0.15em] text-muted-foreground">{spec.label}</p>
                <p className="mt-1.5 text-sm font-medium">{spec.value}</p>
              </div>
            ))}
          </div>
          <div className="mt-10 flex flex-wrap items-center gap-5">
            <p className="font-display text-lg">From {product.fromPrice}</p>
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
      <ImageZoom>
        <ArchitecturalImage
          src={product.image.src}
          alt={product.image.alt}
          aspect="portrait"
          sizes="(max-width: 768px) 100vw, 25vw"
        />
      </ImageZoom>
      <div className="mt-5">
        <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">{product.category}</p>
        <div className="mt-2 flex items-start justify-between gap-2">
          <h3 className="font-display text-xl transition-colors group-hover:text-accent">{product.name}</h3>
          <ArrowUpRight className="h-4 w-4 shrink-0 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
        </div>
        <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-muted-foreground">{product.description}</p>
        <p className="mt-3 text-sm font-medium tracking-wide">From {product.fromPrice}</p>
      </div>
    </Link>
  );
}

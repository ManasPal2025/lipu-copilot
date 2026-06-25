import Link from 'next/link';
import { ArrowRight, CheckCircle2 } from 'lucide-react';

import { ImageZoom } from '@/components/motion/image-zoom';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import type { WizardRecommendation } from '@/lib/recommendation-engine';

interface RecommendationCardProps {
  recommendation: WizardRecommendation;
  onStartOver: () => void;
}

export function RecommendationCard({ recommendation, onStartOver }: RecommendationCardProps) {
  const { product, headline, reasons, inspirationPhotos, galleryCategory, galleryHref } = recommendation;

  return (
    <div className="space-y-12">
      <div className="rounded-sm border border-border bg-card p-6 shadow-sm sm:p-10">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Your recommendation</p>
        <h2 className="mt-4 font-display text-3xl sm:text-4xl lg:text-5xl">{headline}</h2>
        <p className="mt-4 max-w-2xl text-muted-foreground editorial-prose">{product.description}</p>

        <div className="mt-10 grid gap-10 lg:grid-cols-2 lg:gap-12">
          <ImageZoom>
            <ArchitecturalImage
              src={product.image.src}
              alt={product.image.alt}
              aspect="wide"
              sizes="(max-width: 1024px) 100vw, 50vw"
            />
          </ImageZoom>

          <div className="flex flex-col justify-center">
            <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{product.category}</p>
            <h3 className="mt-2 font-display text-2xl sm:text-3xl">{product.name}</h3>
            <p className="mt-4 font-display text-lg">From {product.fromPrice}</p>

            <ul className="mt-8 space-y-3">
              {reasons.map((reason) => (
                <li key={reason} className="flex items-start gap-3 text-sm text-muted-foreground">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden />
                  {reason}
                </li>
              ))}
            </ul>

            <div className="mt-8 grid grid-cols-2 gap-4 border-t border-border pt-8">
              {product.specs.slice(0, 4).map((spec) => (
                <div key={spec.label}>
                  <p className="text-[10px] uppercase tracking-[0.15em] text-muted-foreground">{spec.label}</p>
                  <p className="mt-1.5 text-sm font-medium">{spec.value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-10 flex flex-wrap gap-4 border-t border-border pt-8">
          <Button variant="accent" asChild>
            <Link href="/contact#quote">
              Request a consultation
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/products">View all systems</Link>
          </Button>
          <Button variant="ghost" type="button" onClick={onStartOver}>
            Start over
          </Button>
        </div>
      </div>

      {inspirationPhotos.length > 0 && (
        <div>
          <div className="mb-8 max-w-2xl">
            <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Design inspiration</p>
            <h3 className="mt-3 font-display text-2xl sm:text-3xl">
              {galleryCategory?.title ?? 'Ideas for your space'}
            </h3>
            <p className="mt-3 text-muted-foreground editorial-prose">
              {galleryCategory?.description ??
                'See how similar rooms look with UPVC windows and doors in real Indian homes.'}
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-3 sm:gap-6">
            {inspirationPhotos.map((photo) => (
              <ImageZoom key={photo.src}>
                <ArchitecturalImage
                  src={photo.src}
                  alt={photo.alt}
                  aspect="video"
                  sizes="(max-width: 768px) 100vw, 33vw"
                />
              </ImageZoom>
            ))}
          </div>

          <div className="mt-8">
            <Button variant="outline" asChild>
              <Link href={galleryHref}>
                Browse more {galleryCategory?.title.toLowerCase() ?? 'ideas'}
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

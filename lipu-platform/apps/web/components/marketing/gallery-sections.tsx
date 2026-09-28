'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, X } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { Container, Section } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF } from '@/lib/constants';
import { images, type ImageAsset } from '@/lib/images';
import { cn } from '@/lib/utils';

type GalleryCategory = 'homes' | 'apartments' | 'villas' | 'balconies' | 'commercial';

type GalleryEntry = {
  id: string;
  label: string;
  category: GalleryCategory;
  image: ImageAsset;
};

const FILTERS: { id: 'all' | GalleryCategory; label: string }[] = [
  { id: 'all', label: 'All' },
  { id: 'homes', label: 'Homes' },
  { id: 'apartments', label: 'Apartments' },
  { id: 'villas', label: 'Villas' },
  { id: 'balconies', label: 'Balconies' },
  { id: 'commercial', label: 'Commercial' },
];

const GALLERY_ITEMS: GalleryEntry[] = [
  { id: 'villa', label: 'Villa', category: 'villas', image: images.ecotechGallery.villa },
  { id: 'home', label: 'Home', category: 'homes', image: images.ecotechGallery.residential },
  { id: 'balcony', label: 'Balcony', category: 'balconies', image: images.ecotechGallery.balcony },
  { id: 'apartment', label: 'Apartment', category: 'apartments', image: images.ecotechGallery.apartment },
  { id: 'commercial', label: 'Commercial', category: 'commercial', image: images.ecotechGallery.commercial },
  { id: 'hospitality', label: 'Hospitality', category: 'commercial', image: images.ecotechGallery.hospitality },
];

export function GalleryHero() {
  return (
    <Section className="pb-6 pt-24 sm:pb-8 sm:pt-28 lg:pb-8 lg:pt-32">
      <Container>
        <div className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12">
          <FadeIn>
            <p className="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">
              Gallery
            </p>
            <h1 className="mt-3 max-w-xl font-display text-[2.25rem] leading-[1.08] sm:text-4xl lg:text-[3.25rem]">
              Real spaces.
              <br />
              Real possibilities.
            </h1>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-muted-foreground sm:text-[15px]">
              A quiet collection of homes, workplaces, and outdoor spaces.
            </p>
          </FadeIn>

          <FadeIn delay={0.06}>
            <ArchitecturalImage
              src={images.ecotechGallery.hero.src}
              alt={images.ecotechGallery.hero.alt}
              aspect="video"
              priority
              sizes="(max-width: 1024px) 100vw, 50vw"
              containerClassName="rounded-md"
            />
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

export function GalleryCollection() {
  const [active, setActive] = useState<'all' | GalleryCategory>('all');
  const [viewer, setViewer] = useState<GalleryEntry | null>(null);

  const visible = useMemo(
    () => (active === 'all' ? GALLERY_ITEMS : GALLERY_ITEMS.filter((item) => item.category === active)),
    [active],
  );

  const closeViewer = useCallback(() => setViewer(null), []);

  useEffect(() => {
    if (!viewer) return;

    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') closeViewer();
    };

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', onKey);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener('keydown', onKey);
    };
  }, [viewer, closeViewer]);

  return (
    <Section className="pt-4 sm:pt-6 lg:pt-8">
      <Container>
        <FadeIn>
          <div className="flex flex-wrap gap-2">
            {FILTERS.map((filter) => (
              <button
                key={filter.id}
                type="button"
                onClick={() => setActive(filter.id)}
                className={cn(
                  'rounded-full border px-4 py-1.5 text-xs uppercase tracking-wider transition-colors',
                  active === filter.id
                    ? 'border-foreground bg-foreground text-background'
                    : 'border-border text-muted-foreground hover:border-foreground/40 hover:text-foreground',
                )}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </FadeIn>

        <div className="mt-6 grid gap-4 sm:grid-cols-2 sm:gap-5">
          {visible.map((item, index) => (
            <FadeIn key={item.id} delay={Math.min(index * 0.04, 0.16)}>
              <figure>
                <button
                  type="button"
                  onClick={() => setViewer(item)}
                  className="group relative block w-full overflow-hidden rounded-md text-left"
                  aria-label={`View ${item.label} larger`}
                >
                  <ImageZoom>
                    <ArchitecturalImage
                      src={item.image.src}
                      alt={item.image.alt}
                      aspect="video"
                      sizes="(max-width: 640px) 100vw, 50vw"
                      containerClassName="rounded-md"
                    />
                  </ImageZoom>
                  <span className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-stone-925/70 to-transparent px-5 pb-4 pt-16">
                    <span className="font-display text-lg text-stone-50">{item.label}</span>
                  </span>
                </button>
              </figure>
            </FadeIn>
          ))}
        </div>
      </Container>

      {viewer ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-stone-925/88 p-4 sm:p-8"
          role="dialog"
          aria-modal="true"
          aria-label={viewer.label}
          onClick={closeViewer}
        >
          <button
            type="button"
            onClick={closeViewer}
            className="absolute right-4 top-4 rounded-full border border-stone-600 p-2 text-stone-200 transition-colors hover:bg-stone-800 hover:text-white sm:right-8 sm:top-8"
            aria-label="Close"
          >
            <X className="h-4 w-4" />
          </button>
          <div
            className="relative w-full max-w-5xl overflow-hidden rounded-md"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="relative aspect-[3/2] w-full bg-stone-900">
              <Image
                src={viewer.image.src}
                alt={viewer.image.alt}
                fill
                className={
                  viewer.id === 'villa'
                    ? 'origin-top scale-[1.14] object-cover'
                    : 'object-contain'
                }
                sizes="100vw"
                quality={90}
              />
            </div>
            <p className="mt-3 text-sm text-stone-300">{viewer.label}</p>
          </div>
        </div>
      ) : null}
    </Section>
  );
}

export function GalleryConsultation() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <div className="mx-auto max-w-3xl text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
              Next step
            </p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.5rem]">
              Inspired by what you see?
            </h2>
            <p className="mx-auto mt-5 max-w-md text-base leading-relaxed text-muted-foreground sm:text-lg">
              Tell us about the space you have in mind.
            </p>
            <Button size="lg" className="mt-7 rounded-full" asChild>
              <Link href={CONSULTATION_HREF}>
                Request a Consultation
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </div>
        </FadeIn>
      </Container>
    </Section>
  );
}

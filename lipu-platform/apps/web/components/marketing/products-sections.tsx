import Link from 'next/link';
import { ArrowRight, ArrowUpRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { ParallaxImage } from '@/components/motion/parallax-image';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF } from '@/lib/constants';
import { images, type ImageAsset } from '@/lib/images';

type CatalogueEntry = {
  title: string;
  purpose: string;
  image: ImageAsset;
};

const windows: CatalogueEntry[] = [
  {
    title: 'Sliding Windows',
    purpose: 'Smooth lateral opening for views, ventilation, and compact spaces.',
    image: images.ecotechProducts.slidingWindow,
  },
  {
    title: 'Casement Windows',
    purpose: 'Hinged opening for controlled airflow and a secure seal when closed.',
    image: images.ecotechProducts.casementWindow,
  },
  {
    title: 'Fixed Windows',
    purpose: 'Picture glazing for light and outlook where operation is not required.',
    image: images.ecotechProducts.fixedWindow,
  },
  {
    title: 'Tilt & Turn Windows',
    purpose: 'Dual opening for ventilation and cleaning in bedrooms and living spaces.',
    image: images.ecotechProducts.tiltTurn,
  },
  {
    title: 'Combination Windows',
    purpose: 'Fixed and operable panels together for wide architectural openings.',
    image: images.ecotechProducts.combinationWindow,
  },
];

const doors: CatalogueEntry[] = [
  {
    title: 'Sliding Doors',
    purpose: 'Wide indoor–outdoor connections for living rooms, terraces, and gardens.',
    image: images.ecotechProducts.slidingDoor,
  },
  {
    title: 'French Doors',
    purpose: 'Paired hinged doors for terraces, gardens, and formal openings.',
    image: images.ecotechProducts.frenchDoor,
  },
  {
    title: 'Casement Doors',
    purpose: 'Single hinged access with a clean architectural line.',
    image: images.ecotechProducts.casementDoor,
  },
  {
    title: 'Bifold Doors',
    purpose: 'Folding panels that open a wall toward terrace or garden.',
    image: images.ecotechProducts.bifoldDoor,
  },
];

const architectural: CatalogueEntry[] = [
  {
    title: 'Large-format Glazing',
    purpose: 'Expansive spans for panoramic living and architectural statements.',
    image: images.ecotechProducts.largeFormat,
  },
  {
    title: 'Corner Glazing',
    purpose: 'Unbroken views at the building corner, integrated into the facade.',
    image: images.ecotechProducts.cornerGlazing,
  },
  {
    title: 'Balcony Systems',
    purpose: 'Glazing that turns a balcony into a usable, climate-ready room.',
    image: images.ecotechProducts.balconySystem,
  },
  {
    title: 'Partition Systems',
    purpose: 'Interior glass divisions that keep light moving through a space.',
    image: images.ecotechProducts.partition,
  },
];

function ProductEntry({ item }: { item: CatalogueEntry }) {
  return (
    <article>
      <ArchitecturalImage
        src={item.image.src}
        alt={item.image.alt}
        aspect="video"
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
        containerClassName="rounded-md"
      />
      <div className="mt-3 flex items-start justify-between gap-3">
        <div>
          <h3 className="font-display text-lg sm:text-xl">{item.title}</h3>
          <p className="mt-1.5 text-[13px] leading-relaxed text-muted-foreground">{item.purpose}</p>
        </div>
        <Link
          href={CONSULTATION_HREF}
          className="mt-1 inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-border transition-colors hover:border-foreground hover:bg-foreground hover:text-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-label={`Discuss ${item.title}`}
        >
          <ArrowUpRight className="h-4 w-4" aria-hidden />
        </Link>
      </div>
    </article>
  );
}

function CategorySection({
  eyebrow,
  title,
  description,
  entries,
  muted,
}: {
  eyebrow: string;
  title: string;
  description: string;
  entries: CatalogueEntry[];
  muted?: boolean;
}) {
  return (
    <Section className={muted ? 'bg-muted/20' : undefined}>
      <Container>
        <FadeIn>
          <SectionHeader eyebrow={eyebrow} title={title} description={description} />
        </FadeIn>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 lg:gap-5">
          {entries.map((item, index) => (
            <FadeIn key={item.title} delay={Math.min(index * 0.04, 0.16)}>
              <ProductEntry item={item} />
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

export function ProductsHero() {
  return (
    <section className="relative min-h-[62vh] overflow-hidden lg:min-h-[70vh]" aria-label="Products">
      <ParallaxImage
        src={images.ecotechProducts.hero.src}
        alt={images.ecotechProducts.hero.alt}
        priority
        overlayClassName="luxury-gradient-overlay"
        objectClassName="object-[center_right]"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-stone-925/80 via-stone-925/40 to-transparent" />

      <div className="relative flex min-h-[62vh] flex-col justify-end px-5 pb-12 pt-28 sm:px-6 lg:min-h-[70vh] lg:px-8 lg:pb-14">
        <Container>
          <FadeIn>
            <p className="mb-3 text-[11px] font-medium uppercase tracking-[0.22em] text-stone-300">
              Products
            </p>
            <h1 className="max-w-3xl font-display text-[2.25rem] leading-[1.05] text-stone-50 sm:text-5xl lg:text-[3.25rem]">
              Designed around how you live
            </h1>
            <p className="mt-4 max-w-xl text-sm leading-relaxed text-stone-300 sm:text-[15px]">
              Window, door, and architectural glazing systems for homes and projects — specified to space, climate, and
              the way you want to live.
            </p>
            <Button
              size="lg"
              className="mt-8 rounded-full bg-stone-50 text-stone-925 hover:bg-white"
              asChild
            >
              <Link href={CONSULTATION_HREF}>
                Discuss Your Project
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </FadeIn>
        </Container>
      </div>
    </section>
  );
}

export function ProductsIntro() {
  return (
    <Section>
      <Container size="narrow">
        <FadeIn>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
            The ecosystem
          </p>
          <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.35rem]">
            Systems for different spaces
          </h2>
          <p className="mt-6 text-base leading-relaxed text-muted-foreground sm:text-lg">
            Ecotech offers window, door, and architectural glazing systems designed around how a space is used —
            from everyday openings to large-format and custom applications.
          </p>
        </FadeIn>
      </Container>
    </Section>
  );
}

export function ProductsWindows() {
  return (
    <CategorySection
      eyebrow="Windows"
      title="Windows for every view"
      description="From compact openings to expansive glazing — systems chosen for light, air, and outlook."
      entries={windows}
    />
  );
}

export function ProductsDoors() {
  return (
    <CategorySection
      muted
      eyebrow="Doors"
      title="Open up new possibilities"
      description="Sliding, hinged, and folding systems that connect interiors with terrace, garden, and landscape."
      entries={doors}
    />
  );
}

export function ProductsArchitectural() {
  return (
    <CategorySection
      eyebrow="Architectural systems"
      title="Solutions for unique spaces"
      description="Larger spans, corners, balconies, and interior glass — where standard openings are not enough."
      entries={architectural}
    />
  );
}

export function ProductsCustom() {
  return (
    <Section className="bg-muted/20">
      <Container>
        <div className="grid items-center gap-10 overflow-hidden rounded-md border border-border bg-background lg:grid-cols-2 lg:gap-0">
          <FadeIn>
            <ArchitecturalImage
              src={images.ecotechProducts.customOpening.src}
              alt={images.ecotechProducts.customOpening.alt}
              aspect="auto"
              containerClassName="min-h-[240px] sm:min-h-[300px] lg:min-h-[360px]"
              sizes="(max-width: 1024px) 100vw, 50vw"
            />
          </FadeIn>
          <FadeIn delay={0.08}>
            <div className="px-6 py-8 sm:px-8 lg:px-12 lg:py-10">
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
                Custom openings
              </p>
              <h2 className="mt-3 font-display text-[1.75rem] sm:text-[2rem]">Don&apos;t see exactly what you need?</h2>
              <p className="mt-5 max-w-md text-muted-foreground leading-relaxed">
                Unusual spans, mixed configurations, and architectural openings can be discussed with our team —
                specified to the project, not a catalogue page.
              </p>
              <Button variant="outline" className="mt-10 rounded-full" asChild>
                <Link href={CONSULTATION_HREF}>
                  Discuss Your Project
                  <ArrowRight className="ml-1" />
                </Link>
              </Button>
            </div>
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

export function ProductsConsultation() {
  return (
    <Section className="bg-stone-925 text-stone-50">
      <Container>
        <FadeIn>
          <div className="mx-auto max-w-3xl text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-stone-400">Next step</p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.5rem]">
              Let&apos;s find the right system for your space
            </h2>
            <p className="mx-auto mt-5 max-w-xl text-base leading-relaxed text-stone-400 sm:text-lg">
              Share the room, the opening, and how you want to live. We will help match a system to the architecture.
            </p>
            <Button
              size="lg"
              className="mt-7 rounded-full bg-stone-50 text-stone-925 hover:bg-white"
              asChild
            >
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

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { ParallaxImage } from '@/components/motion/parallax-image';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF } from '@/lib/constants';
import { images } from '@/lib/images';

const residential = [
  {
    title: 'Balcony Transformation',
    description: 'Turn underused balcony space into a usable, climate-ready extension of the home.',
    image: images.ecotechServices.balcony,
  },
  {
    title: 'Terrace Transformation',
    description: 'Create enclosed or semi-open terrace environments for year-round living.',
    image: images.ecotechServices.terrace,
  },
  {
    title: 'Sunrooms',
    description: 'Glass-rich rooms that connect interiors with light and natural surroundings.',
    image: images.ecotechServices.sunroom,
  },
  {
    title: 'Garden Rooms',
    description: 'Dedicated glass-heavy rooms that open toward gardens and outdoor space.',
    image: images.ecotechServices.gardenRoom,
  },
  {
    title: 'Gazebos',
    description: 'Architectural outdoor retreats with refined framing and weather protection.',
    image: images.ecotechServices.gazebo,
  },
  {
    title: 'Outdoor Living',
    description: 'Indoor–outdoor spaces defined by large openings and seamless thresholds.',
    image: images.ecotechServices.outdoorLiving,
  },
  {
    title: 'Poolside Spaces',
    description: 'Premium glazed environments around pools and landscaped settings.',
    image: images.ecotechServices.poolside,
  },
] as const;

const commercial = [
  {
    title: 'Offices',
    image: images.ecotechServices.commercialOffice,
  },
  {
    title: 'Salons',
    image: images.ecotechServices.salon,
  },
  {
    title: 'Cafés & restaurants',
    image: images.ecotechServices.cafeRestaurant,
  },
  {
    title: 'Showrooms',
    image: { src: '/images/projects/corporate-lobby.jpg', alt: 'Commercial showroom-scale glazed facade' },
  },
] as const;

const hospitality = [
  {
    title: 'Hospitality environments',
    image: images.ecotechServices.hospitality,
  },
  {
    title: 'Large villas & residences',
    image: {
      src: images.ecotechInspiration.villa2.src,
      alt: 'Large residence with glazed openings in evening light',
    },
  },
  {
    title: 'Architectural developments',
    image: {
      src: images.ecotechGallery.commercial.src,
      alt: 'Large-scale glazed building at dusk',
    },
  },
] as const;

const processSteps = [
  { title: 'Understand', detail: 'Site, climate, and how the space should feel.' },
  { title: 'Design', detail: 'Systems and openings matched to the brief.' },
  { title: 'Build', detail: 'Precise fabrication and professional installation.' },
  { title: 'Transform', detail: 'Spaces that perform — light, comfort, presence.' },
] as const;

export function ServicesHero() {
  return (
    <section className="relative min-h-[62vh] overflow-hidden lg:min-h-[70vh]" aria-label="Services">
      <ParallaxImage
        src={images.ecotechServices.hero.src}
        alt="Architectural residence with expansive glazing at dusk"
        priority
        overlayClassName="luxury-gradient-overlay"
        objectClassName="object-[center_right]"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-stone-925/80 via-stone-925/45 to-stone-925/20" />

      <div className="relative flex min-h-[62vh] flex-col justify-end px-5 pb-12 pt-28 sm:px-6 lg:min-h-[70vh] lg:px-8 lg:pb-14">
        <Container>
          <FadeIn>
            <p className="mb-3 text-[11px] font-medium uppercase tracking-[0.22em] text-stone-300">Services</p>
            <h1 className="max-w-3xl font-display text-[2.25rem] leading-[1.05] text-stone-50 sm:text-5xl lg:text-[3.25rem]">
              Spaces without limits
            </h1>
            <p className="mt-4 max-w-xl text-sm leading-relaxed text-stone-300 sm:text-[15px]">
              Windows are only where we begin. From individual openings to complete architectural spaces —
              residential, commercial, and beyond.
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

export function ServicesIntro() {
  return (
    <Section>
      <Container size="narrow">
        <FadeIn>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">Philosophy</p>
          <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.35rem]">
            From openings to spaces
          </h2>
          <p className="mt-6 text-base leading-relaxed text-muted-foreground sm:text-lg">
            The right window or door does more than close an opening — it shapes light, air, views, and how a
            home connects with the outdoors. Ecotech designs systems that turn rooms into environments.
          </p>
        </FadeIn>
      </Container>
    </Section>
  );
}

export function ServicesWindowsDoors() {
  return (
    <Section className="bg-muted/20">
      <Container>
        <div className="grid items-center gap-10 overflow-hidden rounded-md border border-border bg-background lg:grid-cols-2 lg:gap-0">
          <FadeIn>
            <ArchitecturalImage
              src={images.ecotechServices.windowsDoors.src}
              alt={images.ecotechServices.windowsDoors.alt}
              aspect="auto"
              containerClassName="min-h-[240px] sm:min-h-[300px] lg:min-h-[380px]"
              sizes="(max-width: 1024px) 100vw, 50vw"
            />
          </FadeIn>
          <FadeIn delay={0.08}>
            <div className="px-6 py-8 sm:px-8 lg:px-12 lg:py-12">
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">Foundation</p>
              <h2 className="mt-3 font-display text-[1.75rem] sm:text-[2rem]">Windows &amp; doors</h2>
              <p className="mt-5 max-w-md text-muted-foreground leading-relaxed">
                Sliding, casement, fixed, and large-format openings — engineered for Odisha&apos;s climate, specified
                for the way you live.
              </p>
              <ul className="mt-8 space-y-2 text-sm text-foreground/80">
                <li>Windows &amp; glazing systems</li>
                <li>Doors &amp; large openings</li>
                <li>Performance glass &amp; finishes</li>
              </ul>
              <Button variant="outline" className="mt-10 rounded-full" asChild>
                <Link href="/products">
                  Explore Products
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

export function ServicesResidential() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Residential transformations"
            title="Spaces that extend everyday living"
            description="Beyond the opening — balconies, terraces, sunrooms, and outdoor environments that feel intentional."
          />
        </FadeIn>

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {residential.map((item, index) => (
            <FadeIn key={item.title} delay={Math.min(index * 0.04, 0.24)}>
              <article>
                <ArchitecturalImage
                  src={item.image.src}
                  alt={item.image.alt}
                  aspect="portrait"
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
                  containerClassName="rounded-md"
                />
                <h3 className="mt-3 font-display text-lg sm:text-xl">{item.title}</h3>
                <p className="mt-1.5 text-[13px] leading-relaxed text-muted-foreground">{item.description}</p>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

export function ServicesCommercial() {
  return (
    <Section className="bg-muted/25">
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Commercial spaces"
            title="Interiors that work as hard as they look"
            description="Offices, salons, cafés, restaurants, and showrooms — contemporary environments where glazing defines the experience."
          />
        </FadeIn>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {commercial.map((item, index) => (
            <FadeIn key={item.title} delay={index * 0.05}>
              <article className="group relative overflow-hidden rounded-md">
                <ArchitecturalImage
                  src={item.image.src}
                  alt={item.image.alt}
                  aspect="square"
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
                  containerClassName="rounded-md"
                />
                <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-stone-925/85 to-transparent p-5">
                  <h3 className="font-display text-lg text-stone-50">{item.title}</h3>
                </div>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

export function ServicesHospitality() {
  return (
    <Section dark>
      <Container>
        <FadeIn>
          <SectionHeader
            light
            eyebrow="Hospitality & large projects"
            title="Designed for projects of different scales"
            description="From distinctive residences to hospitality and architectural developments — systems specified for presence, performance, and climate."
          />
        </FadeIn>

        <div className="grid gap-4 lg:grid-cols-3">
          {hospitality.map((item, index) => (
            <FadeIn key={item.title} delay={index * 0.06}>
              <article>
                <ArchitecturalImage
                  src={item.image.src}
                  alt={item.image.alt}
                  aspect="video"
                  sizes="(max-width: 1024px) 100vw, 33vw"
                  containerClassName="rounded-md"
                />
                <h3 className="mt-5 font-display text-2xl text-stone-50">{item.title}</h3>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

export function ServicesProcess() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <SectionHeader
            align="center"
            className="mx-auto"
            eyebrow="How we approach a project"
            title="From drawing to reality"
            description="A clear path from brief to built space — professional, calm, and precise."
          />
        </FadeIn>

        <ol className="mt-4 grid gap-8 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">
          {processSteps.map((step, index) => (
            <FadeIn key={step.title} delay={index * 0.05}>
              <li className="border-t border-border pt-6">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                  {String(index + 1).padStart(2, '0')}
                </p>
                <h3 className="mt-3 font-display text-2xl">{step.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{step.detail}</p>
              </li>
            </FadeIn>
          ))}
        </ol>
      </Container>
    </Section>
  );
}

export function ServicesConsultation() {
  return (
    <Section className="bg-stone-925 text-stone-50">
      <Container>
        <FadeIn>
          <div className="mx-auto max-w-3xl text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-stone-400">Next step</p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] text-stone-50 sm:text-[2rem] lg:text-[2.5rem]">
              Have a project beyond the ordinary?
            </h2>
            <p className="mx-auto mt-5 max-w-xl text-base leading-relaxed text-stone-400 sm:text-lg">
              Tell us about the space. We will help you explore systems, scale, and what is possible — without a hard
              sell.
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

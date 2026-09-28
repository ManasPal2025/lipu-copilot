import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { ParallaxImage } from '@/components/motion/parallax-image';
import { Container, Section } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF, TRANSFORM_HREF } from '@/lib/constants';
import { images, type ImageAsset } from '@/lib/images';

function Caption({ children }: { children: string }) {
  return <p className="mt-3 text-sm text-muted-foreground">{children}</p>;
}

function Frame({
  image,
  aspect = 'video',
  sizes,
  caption,
  className,
}: {
  image: ImageAsset;
  aspect?: 'video' | 'portrait' | 'square' | 'wide';
  sizes: string;
  caption?: string;
  className?: string;
}) {
  return (
    <figure className={className}>
      <ArchitecturalImage
        src={image.src}
        alt={image.alt}
        aspect={aspect}
        sizes={sizes}
        containerClassName="rounded-md"
      />
      {caption ? <Caption>{caption}</Caption> : null}
    </figure>
  );
}

const chapters = [
  { title: 'Living', caption: 'Bright. Open. Inviting.', image: images.ecotechInspiration.living3 },
  { title: 'Bedroom', caption: 'Calm. Private. Light.', image: images.ecotechInspiration.bedroom1 },
  { title: 'Balcony', caption: 'Compact, made generous.', image: images.ecotechInspiration.balcony1 },
  { title: 'Terrace', caption: 'Between inside and air.', image: images.ecotechInspiration.terrace1 },
  { title: 'Villa', caption: 'Openings at architectural scale.', image: images.ecotechInspiration.villa1 },
  { title: 'Outdoor Living', caption: 'Garden, pool, pavilion.', image: images.ecotechInspiration.outdoor1 },
  { title: 'Commercial', caption: 'Workplaces that hold light.', image: images.ecotechInspiration.commercial },
] as const;

export function InspirationHero() {
  return (
    <section className="relative min-h-[64vh] overflow-hidden lg:min-h-[72vh]" aria-label="Inspiration">
      <ParallaxImage
        src={images.ecotechInspiration.hero.src}
        alt={images.ecotechInspiration.hero.alt}
        priority
        overlayClassName="luxury-gradient-overlay"
        objectClassName="object-[center_right]"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-stone-925/75 via-stone-925/30 to-transparent" />

      <div className="relative flex min-h-[64vh] flex-col justify-end px-5 pb-12 pt-28 sm:px-6 lg:min-h-[72vh] lg:px-8 lg:pb-16">
        <Container>
          <FadeIn>
            <p className="mb-3 text-[11px] font-medium uppercase tracking-[0.22em] text-stone-300">
              Inspiration
            </p>
            <h1 className="max-w-3xl font-display text-[2.25rem] leading-[1.05] text-stone-50 sm:text-5xl lg:text-[3.25rem]">
              Imagine brighter spaces
            </h1>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-stone-300 sm:text-[15px]">
              Real ideas. Beautiful possibilities.
            </p>
          </FadeIn>
        </Container>
      </div>
    </section>
  );
}

export function InspirationIntro() {
  return (
    <Section>
      <Container size="narrow">
        <FadeIn>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
            Editorial
          </p>
          <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem]">
            Openings that change how a space feels
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-muted-foreground sm:text-[15px]">
            Windows and doors shape light, views, and the way a room meets the outdoors. They set atmosphere — and how
            you move through a home.
          </p>
        </FadeIn>
      </Container>
    </Section>
  );
}

export function InspirationChapters() {
  return (
    <Section className="pt-0 sm:pt-0 lg:pt-0">
      <Container>
        <FadeIn>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
            Explore by space
          </p>
          <h2 className="mt-3 max-w-2xl font-display text-[1.75rem] sm:text-[2rem]">Chapters of a home</h2>
        </FadeIn>

        <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {chapters.map((chapter, index) => (
            <FadeIn
              key={chapter.title}
              delay={Math.min(index * 0.04, 0.2)}
              className={index === 0 ? 'sm:col-span-2 lg:col-span-2' : undefined}
            >
              <article>
                <ArchitecturalImage
                  src={chapter.image.src}
                  alt={chapter.image.alt}
                  aspect={index === 0 ? 'wide' : 'square'}
                  sizes={index === 0 ? '(max-width: 1024px) 100vw, 50vw' : '(max-width: 640px) 100vw, 25vw'}
                  containerClassName="rounded-md"
                />
                <h3 className="mt-3 font-display text-xl">{chapter.title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{chapter.caption}</p>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

export function InspirationEditorial() {
  return (
    <Section className="bg-muted/20">
      <Container>
        <FadeIn>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
            Curated spaces
          </p>
          <h2 className="mt-3 max-w-2xl font-display text-[1.75rem] sm:text-[2rem]">Visual possibilities</h2>
        </FadeIn>

        <div className="mt-8 space-y-10 lg:space-y-14">
          <div className="grid items-end gap-6 lg:grid-cols-12 lg:gap-8">
            <FadeIn className="lg:col-span-8">
              <Frame
                image={images.ecotechInspiration.living4}
                aspect="wide"
                sizes="(max-width: 1024px) 100vw, 66vw"
                caption="Light across the living space."
              />
            </FadeIn>
            <FadeIn delay={0.08} className="lg:col-span-4">
              <Frame
                image={images.ecotechInspiration.bedroom2}
                aspect="portrait"
                sizes="(max-width: 1024px) 100vw, 33vw"
                caption="Quiet light, held private."
              />
            </FadeIn>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <FadeIn>
              <Frame
                image={images.ecotechInspiration.balcony3}
                aspect="video"
                sizes="(max-width: 768px) 100vw, 50vw"
                caption="An extension of the room."
              />
            </FadeIn>
            <FadeIn delay={0.06}>
              <Frame
                image={images.ecotechInspiration.terrace2}
                aspect="video"
                sizes="(max-width: 768px) 100vw, 50vw"
                caption="Open to the terrace."
              />
            </FadeIn>
          </div>

          <FadeIn>
            <Frame
              image={images.ecotechInspiration.villa2}
              aspect="wide"
              sizes="100vw"
              caption="Framing the view."
            />
          </FadeIn>

          <div className="grid items-stretch gap-6 lg:grid-cols-3">
            <FadeIn className="lg:col-span-2">
              <Frame
                image={images.ecotechInspiration.outdoor2}
                aspect="video"
                sizes="(max-width: 1024px) 100vw, 66vw"
                caption="Open to the garden."
              />
            </FadeIn>
            <FadeIn delay={0.08}>
              <Frame
                image={images.ecotechInspiration.balcony4}
                aspect="portrait"
                sizes="(max-width: 1024px) 100vw, 33vw"
                caption="A balcony, made still."
              />
            </FadeIn>
          </div>
        </div>
      </Container>
    </Section>
  );
}

export function InspirationFeatured() {
  const features = [
    { title: 'Indoor–outdoor living', image: images.ecotechInspiration.living3, caption: 'Thresholds that disappear.' },
    { title: 'Terrace transformation', image: images.ecotechInspiration.terrace4, caption: 'An extension of the terrace.' },
    { title: 'Balcony transformation', image: images.ecotechInspiration.balcony2, caption: 'Compact space, given purpose.' },
    {
      title: 'Villa openings',
      image: images.ecotechInspiration.villa1,
      caption: 'Architecture, held in glass.',
      frameClassName: 'origin-top scale-[1.24]',
    },
    { title: 'Outdoor living', image: images.ecotechInspiration.outdoor1, caption: 'Garden, air, and shade.' },
    { title: 'Commercial interiors', image: images.ecotechInspiration.commercial, caption: 'Workspaces that invite light.' },
  ] as const;

  return (
    <Section>
      <Container>
        <FadeIn>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
            Featured
          </p>
          <h2 className="mt-3 max-w-2xl font-display text-[1.75rem] sm:text-[2rem]">Spaces worth imagining</h2>
        </FadeIn>

        <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {features.map((item, index) => (
            <FadeIn key={item.title} delay={Math.min(index * 0.04, 0.16)}>
              <article>
                <ArchitecturalImage
                  src={item.image.src}
                  alt={item.image.alt}
                  aspect="video"
                  sizes="(max-width: 768px) 100vw, 33vw"
                  className={'frameClassName' in item ? item.frameClassName : undefined}
                  containerClassName="rounded-md"
                />
                <h3 className="mt-3 font-display text-lg">{item.title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{item.caption}</p>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

export function InspirationTransform() {
  return (
    <Section dark>
      <Container>
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <FadeIn>
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-stone-400">
              Imagine your space
            </p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] text-stone-50 sm:text-[2rem] lg:text-[2.35rem]">
              See what your space could become
            </h2>
            <p className="mt-5 max-w-md text-base leading-relaxed text-stone-400">
              Visual inspiration is a starting point. Preview a transformation, then talk with our team about what is
              possible.
            </p>
            <Button
              size="lg"
              className="mt-8 rounded-full bg-stone-50 text-stone-925 hover:bg-white"
              asChild
            >
              <Link href={TRANSFORM_HREF}>
                Transform Your Space
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </FadeIn>

          <FadeIn delay={0.08}>
            <div className="overflow-hidden rounded-md border border-stone-700">
              <div className="grid grid-cols-2">
                <div className="relative">
                  <ArchitecturalImage
                    src={images.ecotechHome.transformBefore.src}
                    alt={images.ecotechHome.transformBefore.alt}
                    aspect="portrait"
                    sizes="(max-width: 1024px) 50vw, 25vw"
                    className="grayscale-[20%] brightness-90"
                  />
                  <span className="absolute left-3 top-3 rounded-full bg-background/90 px-3 py-1 text-[10px] uppercase tracking-[0.15em] text-muted-foreground">
                    Before
                  </span>
                </div>
                <div className="relative">
                  <ArchitecturalImage
                    src={images.ecotechHome.transformAfter.src}
                    alt={images.ecotechHome.transformAfter.alt}
                    aspect="portrait"
                    sizes="(max-width: 1024px) 50vw, 25vw"
                  />
                  <span className="absolute left-3 top-3 rounded-full bg-stone-50 px-3 py-1 text-[10px] uppercase tracking-[0.15em] text-stone-925">
                    After
                  </span>
                </div>
              </div>
            </div>
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

export function InspirationConsultation() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <div className="mx-auto max-w-3xl text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">Next step</p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.5rem]">
              Have a space in mind?
            </h2>
            <p className="mx-auto mt-5 max-w-lg text-base leading-relaxed text-muted-foreground sm:text-lg">
              Tell us about the room, the outlook, and how you want to live. We will help you explore what is possible.
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

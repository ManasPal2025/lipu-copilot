import type { Metadata } from 'next';
import Link from 'next/link';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images } from '@/lib/images';
import { companyValues, stats, teamMembers } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'About',
  description: 'LIPU exists to transform how Indian homes experience light, silence, and space.',
};

export default function AboutPage() {
  return (
    <>
      <PageHero
        eyebrow="About LIPU"
        title="We sell transformation, not windows"
        description="Founded on a simple belief: the right envelope changes how you live. We partner with homeowners and architects to make that change real."
        image={images.pageHero.about}
      />

      <Section>
        <Container>
          <div className="grid items-center gap-16 lg:grid-cols-2 lg:gap-24">
            <FadeIn>
              <ImageZoom>
                <ArchitecturalImage
                  src={images.about.craft.src}
                  alt={images.about.craft.alt}
                  aspect="portrait"
                  sizes="(max-width: 1024px) 100vw, 50vw"
                />
              </ImageZoom>
            </FadeIn>
            <FadeIn delay={0.1}>
              <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl">Craft meets climate</h2>
              <p className="mt-6 leading-relaxed text-muted-foreground editorial-prose">
                India demands more from building envelopes than most markets. Heat, monsoon, coastal salt, urban noise —
                our profiles are engineered for all of it, without sacrificing the architectural clarity you expect from
                international brands like Pella, Andersen, and Marvin.
              </p>
              <p className="mt-5 leading-relaxed text-muted-foreground editorial-prose">
                Our process is closer to Apple and Tesla: obsessive detail, honest communication, and an experience that
                feels premium from first touch to final install.
              </p>
              <Button variant="accent" className="mt-10" asChild>
                <Link href="/contact">Meet our team</Link>
              </Button>
            </FadeIn>
          </div>
        </Container>
      </Section>

      <section className="relative min-h-[45vh] overflow-hidden">
        <ArchitecturalImage
          src={images.about.manifesto.src}
          alt={images.about.manifesto.alt}
          aspect="auto"
          containerClassName="absolute inset-0 min-h-[45vh]"
          className="opacity-40"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-stone-925/70" />
        <Container className="relative flex min-h-[45vh] items-center py-20">
          <FadeIn>
            <blockquote className="max-w-3xl">
              <p className="font-display text-3xl leading-[1.15] text-stone-50 sm:text-4xl">
                We do not sell windows. We engineer the moment light enters your home — and everything that follows.
              </p>
            </blockquote>
          </FadeIn>
        </Container>
      </section>

      <Section className="border-t border-border bg-muted/20">
        <Container>
          <FadeIn>
            <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl">What we believe</h2>
          </FadeIn>
          <div className="mt-16 grid gap-12 md:grid-cols-3">
            {companyValues.map((value, i) => (
              <FadeIn key={value.title} delay={i * 0.08}>
                <div className="border-t border-border pt-8">
                  <h3 className="font-display text-2xl">{value.title}</h3>
                  <p className="mt-4 text-sm leading-relaxed text-muted-foreground editorial-prose">
                    {value.description}
                  </p>
                </div>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <Section dark>
        <Container>
          <FadeIn>
            <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl">Leadership</h2>
            <p className="mt-4 max-w-md text-stone-400 editorial-prose">
              Architects, engineers, and craftspeople united by one obsession — the quality of light in a home.
            </p>
          </FadeIn>

          <div className="mt-16 grid gap-10 sm:grid-cols-3">
            {teamMembers.map((member, i) => (
              <FadeIn key={member.id} delay={i * 0.08}>
                <article className="group">
                  <ImageZoom>
                    <ArchitecturalImage
                      src={member.image.src}
                      alt={member.image.alt}
                      aspect="portrait"
                      sizes="(max-width: 640px) 100vw, 33vw"
                      className="grayscale-[20%] transition-all group-hover:grayscale-0"
                    />
                  </ImageZoom>
                  <div className="mt-6 border-t border-stone-800 pt-6">
                    <h3 className="font-display text-xl text-stone-50">{member.name}</h3>
                    <p className="mt-2 text-[10px] uppercase tracking-[0.15em] text-accent">{member.role}</p>
                    <p className="mt-4 text-sm leading-relaxed text-stone-400">{member.bio}</p>
                  </div>
                </article>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <Section className="border-t border-border">
        <Container>
          <div className="grid grid-cols-2 gap-10 lg:grid-cols-4 lg:gap-12">
            {stats.map((stat, i) => (
              <FadeIn key={stat.label} delay={i * 0.06}>
                <p className="font-display text-4xl sm:text-5xl">{stat.value}</p>
                <p className="mt-3 text-sm tracking-wide text-muted-foreground">{stat.label}</p>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

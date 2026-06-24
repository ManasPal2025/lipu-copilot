'use client';

import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { useCity } from '@/components/providers/city-provider';
import { ArchitecturalImage } from '@/components/ui/architectural-image';

export function TransformationSection() {
  const { getImage, cityLabel } = useCity();
  const transformation = getImage('transformation');

  return (
    <Section>
      <Container>
        <div className="grid items-center gap-16 lg:grid-cols-2 lg:gap-24">
          <FadeIn>
            <SectionHeader
              eyebrow="The LIPU difference"
              title="Transformation before specification"
              description="Every project begins with a vision — how you want to live, not what you want to buy. Our process is designed around that truth."
            />
            <p className="mb-10 max-w-lg text-muted-foreground leading-relaxed editorial-prose">
              From coastal villas to urban apartments, we partner with homeowners in {cityLabel} and across India to
              reimagine how space, light, and silence define a home.
            </p>
            <Link
              href="/about"
              className="inline-flex items-center gap-2 text-sm font-medium tracking-wide transition-colors hover:text-accent"
            >
              Our philosophy
              <ArrowUpRight className="h-4 w-4" />
            </Link>
          </FadeIn>
          <FadeIn delay={0.15}>
            <ImageZoom>
              <ArchitecturalImage
                src={transformation.src}
                alt={transformation.alt}
                aspect="portrait"
                sizes="(max-width: 1024px) 100vw, 50vw"
              />
            </ImageZoom>
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

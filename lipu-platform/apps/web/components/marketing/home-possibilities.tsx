import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images } from '@/lib/images';

const possibilities = [
  {
    title: 'Balcony transformations',
    image: images.ecotechHome.balcony,
  },
  {
    title: 'Terrace & sunrooms',
    image: images.ecotechServices.terrace,
  },
  {
    title: 'Outdoor living',
    image: images.ecotechServices.outdoorLiving,
  },
  {
    title: 'Commercial spaces',
    image: images.ecotechServices.commercialOffice,
  },
] as const;

export function HomePossibilitiesSection() {
  return (
    <Section className="bg-muted/25">
      <Container>
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <FadeIn>
            <SectionHeader
              className="mb-0"
              eyebrow="Possibilities"
              title="From openings to extraordinary spaces"
              description="Balconies, terraces, sunrooms, garden rooms, and commercial environments — Ecotech participates in projects of every scale."
            />
          </FadeIn>
          <FadeIn delay={0.08}>
            <Button variant="outline" className="rounded-full shrink-0" asChild>
              <Link href="/services">
                Explore Services
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </FadeIn>
        </div>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {possibilities.map((item, index) => (
            <FadeIn key={item.title} delay={index * 0.05}>
              <article>
                <ArchitecturalImage
                  src={item.image.src}
                  alt={item.image.alt}
                  aspect="square"
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
                  containerClassName="rounded-md"
                />
                <h3 className="mt-3 font-display text-lg">{item.title}</h3>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

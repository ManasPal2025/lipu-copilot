import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { images } from '@/lib/images';

const offerings = [
  {
    title: 'Windows',
    description: 'Sliding, casement, fixed, and tilt & turn systems designed for light and climate.',
    image: images.ecotechHome.living,
    href: '/products',
  },
  {
    title: 'Doors',
    description: 'Sliding, French, casement, and bifold openings that connect indoors to outdoors.',
    image: images.ecotechHome.indoorOutdoor,
    href: '/products',
  },
  {
    title: 'Architectural Spaces',
    description: 'Large-format glazing, corner systems, and custom solutions for distinctive projects.',
    image: images.ecotechHome.villa,
    href: '/services',
  },
] as const;

export function HomeOfferingsSection() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="What Ecotech creates"
            title="Crafted for every space"
            description="Elegant. Durable. Timeless. Windows and doors are only the beginning — Ecotech shapes how spaces feel."
          />
        </FadeIn>

        <div className="grid gap-6 md:grid-cols-3 md:gap-5 lg:gap-6">
          {offerings.map((item, index) => (
            <FadeIn key={item.title} delay={index * 0.06}>
              <Link href={item.href} className="group block">
                <ArchitecturalImage
                  src={item.image.src}
                  alt={item.image.alt}
                  aspect="portrait"
                  sizes="(max-width: 768px) 100vw, 33vw"
                  containerClassName="rounded-md"
                />
                <div className="mt-4 flex items-start justify-between gap-4">
                  <div>
                <h3 className="font-display text-xl">{item.title}</h3>
                    <p className="mt-1.5 text-[13px] leading-relaxed text-muted-foreground">{item.description}</p>
                  </div>
                  <span className="mt-1 inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-border transition-colors group-hover:border-foreground group-hover:bg-foreground group-hover:text-background">
                    <ArrowUpRight className="h-4 w-4" aria-hidden />
                  </span>
                </div>
              </Link>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

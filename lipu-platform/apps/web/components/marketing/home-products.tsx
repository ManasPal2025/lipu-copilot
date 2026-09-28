import Link from 'next/link';
import { ArrowRight, ArrowUpRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images } from '@/lib/images';

const featured = [
  {
    title: 'Windows',
    description: 'Systems for every view — sliding, casement, fixed, and tilt & turn.',
    image: images.ecotechProducts.slidingWindow,
  },
  {
    title: 'Sliding Doors',
    description: 'Wide openings that dissolve the boundary between home and landscape.',
    image: images.ecotechProducts.slidingDoor,
  },
  {
    title: 'Entrance & French Doors',
    description: 'Statement doors with security, thermal performance, and presence.',
    image: images.ecotechProducts.frenchDoor,
  },
  {
    title: 'Large-format glazing',
    description: 'Panoramic fixed and structural spans for architectural statements.',
    image: images.ecotechProducts.largeFormat,
  },
] as const;

export function HomeProductsSection() {
  return (
    <Section>
      <Container>
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <FadeIn>
            <SectionHeader
              className="mb-0"
              eyebrow="Featured products"
              title="Systems that perform beautifully"
              description="A restrained introduction to the Ecotech ecosystem — explore the full catalogue when you are ready."
            />
          </FadeIn>
          <FadeIn delay={0.08}>
            <Button variant="outline" className="rounded-full shrink-0" asChild>
              <Link href="/products">
                Explore Products
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </FadeIn>
        </div>

        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:gap-8">
          {featured.map((item, index) => (
            <FadeIn key={item.title} delay={index * 0.05}>
              <Link href="/products" className="group grid gap-5 sm:grid-cols-12 sm:items-center">
                <div className="sm:col-span-5">
                  <ArchitecturalImage
                    src={item.image.src}
                    alt={item.image.alt}
                    aspect="video"
                    sizes="(max-width: 640px) 100vw, 40vw"
                    containerClassName="rounded-md"
                  />
                </div>
                <div className="sm:col-span-7">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="font-display text-xl sm:text-2xl">{item.title}</h3>
                    <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-border transition-colors group-hover:border-foreground group-hover:bg-foreground group-hover:text-background">
                      <ArrowUpRight className="h-4 w-4" aria-hidden />
                    </span>
                  </div>
                  <p className="mt-2 max-w-md text-[13px] leading-relaxed text-muted-foreground sm:text-sm">
                    {item.description}
                  </p>
                </div>
              </Link>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images } from '@/lib/images';

const spaces = [
  {
    title: 'Living',
    image: images.ecotechHome.living,
  },
  {
    title: 'Bedroom',
    image: images.ecotechHome.bedroom,
  },
  {
    title: 'Balcony',
    image: images.ecotechHome.balcony,
  },
  {
    title: 'Terrace',
    image: images.ecotechInspiration.terrace1,
  },
  {
    title: 'Villa',
    image: images.ecotechHome.villa,
  },
] as const;

export function HomeInspirationSection() {
  return (
    <Section dark>
      <Container>
        <div className="grid gap-8 lg:grid-cols-12 lg:gap-12 lg:items-end">
          <FadeIn className="lg:col-span-5">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-stone-400">Inspiration</p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] text-stone-50 sm:text-[2rem] lg:text-[2.5rem]">
              Inspired by your tomorrow
            </h2>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-stone-400 sm:text-[15px]">
              Editorial glimpses of living, sleeping, balconies, terraces, and villas — what your space could become.
            </p>
            <Button
              variant="outline"
              className="mt-8 rounded-full border-stone-600 bg-transparent text-stone-50 hover:bg-white/10 hover:text-white"
              asChild
            >
              <Link href="/inspiration">
                Explore Inspiration
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </FadeIn>

          <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:col-span-7 lg:grid-cols-6">
            {spaces.map((space, index) => (
              <FadeIn
                key={space.title}
                delay={index * 0.04}
                className={index === 0 ? 'col-span-2 row-span-2 lg:col-span-4 lg:row-span-2' : 'lg:col-span-2'}
              >
                <article className="group relative overflow-hidden rounded-md">
                  <ArchitecturalImage
                    src={space.image.src}
                    alt={space.image.alt}
                    aspect={index === 0 ? 'video' : 'square'}
                    sizes={index === 0 ? '(max-width: 1024px) 100vw, 40vw' : '(max-width: 1024px) 50vw, 16vw'}
                    containerClassName="rounded-md"
                  />
                  <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-stone-925/80 to-transparent p-4">
                    <p className="font-display text-base text-stone-50">{space.title}</p>
                  </div>
                </article>
              </FadeIn>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  );
}

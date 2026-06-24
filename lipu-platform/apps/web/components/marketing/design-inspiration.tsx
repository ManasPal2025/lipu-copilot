import Link from 'next/link';

import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { designStyles } from '@/lib/mock-data';

export function DesignInspirationSection() {
  return (
    <Section dark>
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Design inspiration"
            title="Ideas for every room in your home"
            description="Living rooms, balconies, kitchens, villas — browse real-home photos that help you imagine the finished result."
            light
            align="center"
          />
        </FadeIn>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4 lg:gap-6">
          {designStyles.map((style, i) => (
            <FadeIn key={style.id} delay={i * 0.08}>
              <article className="group flex h-full flex-col">
                <ImageZoom>
                  <ArchitecturalImage
                    src={style.image.src}
                    alt={style.image.alt}
                    aspect="portrait"
                    sizes="(max-width: 768px) 100vw, 25vw"
                  />
                </ImageZoom>
                <div className="mt-6 flex flex-1 flex-col">
                  <h3 className="font-display text-2xl text-stone-50">{style.name}</h3>
                  <p className="mt-3 flex-1 text-sm leading-relaxed text-stone-400">{style.description}</p>
                  <div className="mt-5 flex flex-wrap gap-2">
                    {style.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-full border border-stone-700 px-2.5 py-0.5 text-[10px] uppercase tracking-wider text-stone-500"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            </FadeIn>
          ))}
        </div>

        <FadeIn>
          <p className="mt-16 text-center text-sm text-stone-500">
            Browse all 100 ideas by room —{' '}
            <Link href="/gallery" className="text-stone-300 underline-offset-4 hover:underline">
              open the inspiration gallery
            </Link>
            {' '}or{' '}
            <Link href="/contact" className="text-stone-300 underline-offset-4 hover:underline">
              book a design consultation
            </Link>
          </p>
        </FadeIn>
      </Container>
    </Section>
  );
}

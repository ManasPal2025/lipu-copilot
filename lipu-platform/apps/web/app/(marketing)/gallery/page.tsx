import type { Metadata } from 'next';

import { PageHero } from '@/components/layout/page-hero';
import { Container, ImagePlaceholder, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { galleryItems } from '@/lib/mock-data';
import { cn } from '@/lib/utils';

export const metadata: Metadata = {
  title: 'Gallery',
  description: 'Architectural photography — moments of light, craft, and transformation by LIPU.',
};

export default function GalleryPage() {
  return (
    <>
      <PageHero
        eyebrow="Gallery"
        title="Light, captured"
        description="A curated collection of transformations — the quiet moments when architecture and atmosphere align."
        align="center"
      />

      <Section>
        <Container size="wide">
          <div className="columns-1 gap-5 sm:columns-2 lg:columns-3">
            {galleryItems.map((item, i) => (
              <FadeIn key={item.id} delay={(i % 3) * 0.06}>
                <figure className="mb-5 break-inside-avoid">
                  <ImagePlaceholder
                    label={item.imageLabel}
                    aspect={item.span === 'tall' ? 'portrait' : item.span === 'wide' ? 'wide' : 'video'}
                    className={cn(item.span === 'tall' && 'min-h-[420px]')}
                  />
                  <figcaption className="mt-3 flex items-baseline justify-between gap-4 px-1">
                    <div>
                      <span className="font-display text-lg">{item.title}</span>
                      <p className="text-xs text-muted-foreground">{item.location}</p>
                    </div>
                    <span className="text-xs uppercase tracking-wider text-muted-foreground">{item.category}</span>
                  </figcaption>
                </figure>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}

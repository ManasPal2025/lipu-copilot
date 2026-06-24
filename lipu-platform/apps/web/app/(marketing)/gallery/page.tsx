import type { Metadata } from 'next';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { GalleryGrid } from '@/components/marketing/gallery-grid';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { galleryItems } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Home Design Ideas',
  description:
    'Browse 100 real-home inspiration photos for Bhubaneswar and Odisha — living rooms, balconies, kitchens, villas, and more.',
};

export default function GalleryPage() {
  return (
    <>
      <PageHero
        eyebrow="Design ideas"
        title="What will your home look like?"
        description="Browse room-by-room inspiration for UPVC doors and windows — real homes, natural light, and finished spaces homeowners in Odisha actually want."
        align="center"
        image={{
          src: '/images/inspiration/living-room/01.jpg',
          alt: 'Bright Indian living room with natural light through large UPVC windows',
        }}
      />

      <Section>
        <Container size="wide">
          <GalleryGrid items={galleryItems} />
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

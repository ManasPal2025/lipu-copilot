import type { Metadata } from 'next';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { ContactForm } from '@/components/marketing/contact-form';
import { ContactVisualizerPreview } from '@/components/marketing/contact-visualizer-preview';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { images } from '@/lib/images';
import { studios } from '@/lib/mock-data';
import { Mail, MapPin, Phone } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Contact',
  description: 'Begin your home transformation — request a consultation with the LIPU team.',
};

export default function ContactPage() {
  return (
    <>
      <PageHero
        eyebrow="Contact"
        title="Begin your transformation"
        description="Share your vision. We respond within one business day with a thoughtful next step — never a hard sell."
        align="center"
        image={images.pageHero.contact}
      />

      <Section>
        <Container>
          <div className="grid gap-16 lg:grid-cols-12 lg:gap-20">
            <FadeIn className="lg:col-span-5">
              <div className="space-y-12">
                <ImageZoom className="hidden lg:block">
                  <ArchitecturalImage
                    src={images.contact.src}
                    alt={images.contact.alt}
                    aspect="portrait"
                    sizes="40vw"
                  />
                </ImageZoom>

                <div>
                  <h2 className="font-display text-2xl">Studios</h2>
                  <ul className="mt-8 space-y-8">
                    {studios.map((studio) => (
                      <li key={studio.city} className="border-t border-border pt-6 first:border-t-0 first:pt-0">
                        <p className="font-medium">{studio.city}</p>
                        <p className="mt-2 flex items-start gap-2 text-sm text-muted-foreground">
                          <MapPin className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />
                          {studio.address}
                        </p>
                        <p className="mt-1 text-xs text-muted-foreground">{studio.hours}</p>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h2 className="font-display text-2xl">Direct</h2>
                  <ul className="mt-6 space-y-4 text-muted-foreground">
                    <li>
                      <a href="mailto:hello@lipu.com" className="inline-flex items-center gap-2 transition-colors hover:text-foreground">
                        <Mail className="h-4 w-4" aria-hidden />
                        hello@lipu.com
                      </a>
                    </li>
                    <li>
                      <a href="tel:+919876543210" className="inline-flex items-center gap-2 transition-colors hover:text-foreground">
                        <Phone className="h-4 w-4" aria-hidden />
                        +91 98765 43210
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </FadeIn>

            <FadeIn delay={0.1} className="lg:col-span-7">
              <ContactForm />

              <ContactVisualizerPreview />
            </FadeIn>
          </div>
        </Container>
      </Section>
    </>
  );
}

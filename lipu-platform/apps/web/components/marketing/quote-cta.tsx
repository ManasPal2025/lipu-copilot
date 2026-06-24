'use client';

import Link from 'next/link';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { useCity } from '@/components/providers/city-provider';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';

export function QuoteCTASection() {
  const { getImage, style } = useCity();
  const bg = getImage('hero');

  return (
    <Section className="relative overflow-hidden border-t border-border">
      <div className="absolute inset-0">
        <ArchitecturalImage
          src={bg.src}
          alt=""
          aspect="auto"
          containerClassName="absolute inset-0 h-full w-full"
          className="opacity-20 dark:opacity-15"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-background/90 dark:bg-stone-925/92" />
      </div>

      <Container size="narrow" className="relative">
        <FadeIn>
          <div className="text-center">
            <p className="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">Begin</p>
            <h2 className="mt-5 font-display text-4xl sm:text-5xl lg:text-6xl">{style.copy.ctaTitle}</h2>
            <p className="mx-auto mt-5 max-w-xl text-muted-foreground leading-relaxed editorial-prose">
              Tell us about your home in {style.label}. We will respond with a thoughtful consultation — not a sales
              pitch.
            </p>
            <div className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button variant="accent" size="lg" asChild>
                <Link href="/contact#quote">Request a consultation</Link>
              </Button>
              <Button variant="ghost" size="lg" asChild>
                <Link href="/projects">View our work first</Link>
              </Button>
            </div>
          </div>
        </FadeIn>
      </Container>
    </Section>
  );
}

'use client';

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { ParallaxImage } from '@/components/motion/parallax-image';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF, TRANSFORM_HREF } from '@/lib/constants';
import { images } from '@/lib/images';

export function HeroSection() {
  const hero = images.ecotechHome.hero;

  return (
    <section className="relative min-h-[72vh] w-full overflow-hidden lg:min-h-[80vh]" aria-label="Hero">
      <ParallaxImage
        src={hero.src}
        alt="Architectural living space with floor-to-ceiling glazing at dusk"
        priority
        overlayClassName="luxury-gradient-overlay"
        objectClassName="object-[center_right]"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-stone-925/75 via-stone-925/35 to-transparent" />

      <div className="relative flex min-h-[72vh] flex-col justify-end px-5 pb-14 pt-28 sm:px-6 lg:min-h-[80vh] lg:px-8 lg:pb-16">
        <div className="mx-auto w-full max-w-7xl">
          <p className="mb-3 text-[11px] font-medium uppercase tracking-[0.22em] text-stone-300/90">
            Ecotech Window Systems
          </p>

          <h1 className="max-w-3xl font-display text-[2.25rem] leading-[1.05] text-stone-50 sm:text-5xl lg:text-[3.5rem]">
            Beyond frames.
            <span className="mt-1 block text-stone-300/95">Spaces that open up life.</span>
          </h1>

          <p className="mt-5 max-w-lg text-sm leading-relaxed text-stone-300/90 sm:text-[15px]">
            Premium UPVC windows, doors, and architectural glazing for homes and projects across Odisha —
            more light, comfort, and possibility.
          </p>

          <div className="mt-7 flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
            <Button
              size="lg"
              className="min-w-[220px] rounded-full bg-stone-50 text-stone-925 hover:bg-white"
              asChild
            >
              <Link href={CONSULTATION_HREF}>
                Request a Consultation
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="min-w-[220px] rounded-full border-stone-400/50 bg-transparent text-stone-50 hover:bg-white/10 hover:text-white"
              asChild
            >
              <Link href={TRANSFORM_HREF}>Transform Your Space</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}

'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

import { ParallaxImage } from '@/components/motion/parallax-image';
import { useCity } from '@/components/providers/city-provider';
import { Button } from '@/components/ui/button';

export function HeroSection() {
  const { getImage, style } = useCity();
  const hero = getImage('hero');

  return (
    <section className="relative min-h-[100svh] w-full overflow-hidden" aria-label="Hero">
      <ParallaxImage
        src={hero.src}
        alt={hero.alt}
        priority
        overlayClassName="luxury-gradient-overlay"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-stone-925/60 via-stone-925/20 to-transparent" />

      <div className="relative flex min-h-[100svh] flex-col justify-end px-5 pb-24 pt-32 sm:px-6 lg:px-8 lg:pb-28">
        <div className="mx-auto w-full max-w-7xl">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mb-6 text-xs font-medium uppercase tracking-[0.35em] text-stone-300/90"
          >
            {style.copy.heroEyebrow}
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.35 }}
            className="max-w-4xl font-display text-[2.75rem] leading-[1.02] text-stone-50 sm:text-5xl md:text-6xl lg:text-[5.25rem]"
          >
            Where light
            <br />
            <span className="text-stone-300/95">becomes architecture.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.55 }}
            className="mt-8 max-w-xl text-base leading-relaxed text-stone-300/90 sm:text-lg editorial-prose"
          >
            {style.copy.heroSubline}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.75 }}
            className="mt-12 flex flex-col gap-4 sm:flex-row sm:items-center"
          >
            <Button variant="accent" size="lg" className="min-w-[220px]" asChild>
              <Link href="/projects">
                Explore transformations
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="min-w-[220px] border-stone-500/40 bg-stone-925/20 text-stone-100 backdrop-blur-sm hover:bg-stone-50/10"
              asChild
            >
              <Link href="/#visualizer">Visualize your home</Link>
            </Button>
          </motion.div>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 1 }}
        className="absolute bottom-8 left-1/2 hidden -translate-x-1/2 sm:block"
        aria-hidden
      >
        <div className="h-12 w-px bg-gradient-to-b from-transparent via-stone-400/60 to-transparent" />
      </motion.div>
    </section>
  );
}

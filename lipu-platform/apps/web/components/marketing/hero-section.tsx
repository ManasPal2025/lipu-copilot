'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

import { ImagePlaceholder } from '@/components/layout/section';
import { Button } from '@/components/ui/button';

export function HeroSection() {
  return (
    <section className="relative min-h-[100svh] w-full overflow-hidden" aria-label="Hero">
      <div className="absolute inset-0">
        <ImagePlaceholder label="Architectural residence at golden hour — full bleed hero" aspect="hero" className="h-full min-h-[100svh]" />
        <div className="absolute inset-0 bg-gradient-to-t from-stone-925/90 via-stone-925/40 to-stone-925/20" />
      </div>

      <div className="relative flex min-h-[100svh] flex-col justify-end px-5 pb-20 pt-32 sm:px-6 lg:px-8">
        <div className="mx-auto w-full max-w-7xl">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mb-6 text-xs font-medium uppercase tracking-[0.3em] text-stone-300"
          >
            Home transformation
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.35 }}
            className="max-w-4xl font-display text-4xl leading-[1.05] text-stone-50 sm:text-5xl md:text-6xl lg:text-7xl"
          >
            Your home,
            <br />
            <span className="text-stone-300">reimagined.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.55 }}
            className="mt-6 max-w-xl text-base leading-relaxed text-stone-300 sm:text-lg"
          >
            We do not sell windows. We engineer the moment light enters your home — and everything that follows.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.75 }}
            className="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center"
          >
            <Button variant="accent" size="lg" asChild>
              <Link href="/projects">
                Explore transformations
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-stone-500/50 bg-transparent text-stone-100 hover:bg-stone-50/10"
              asChild
            >
              <Link href="/#visualizer">Visualize your home</Link>
            </Button>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

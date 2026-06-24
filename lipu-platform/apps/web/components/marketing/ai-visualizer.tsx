'use client';

import Link from 'next/link';
import { Sparkles } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { Container, Section } from '@/components/layout/section';
import { useCity } from '@/components/providers/city-provider';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';

export function AIVisualizerSection() {
  const { getImage, style } = useCity();
  const visualizer = getImage('visualizer');

  return (
    <Section id="visualizer">
      <Container>
        <div className="grid items-stretch overflow-hidden rounded-sm bg-stone-925 lg:grid-cols-2">
          <FadeIn>
            <div className="flex flex-col justify-center p-8 sm:p-12 lg:p-16 xl:p-20">
              <div className="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-stone-700 px-4 py-1.5 text-xs uppercase tracking-[0.15em] text-stone-400">
                <Sparkles className="h-3.5 w-3.5" aria-hidden />
                Coming soon
              </div>
              <h2 className="font-display text-3xl text-stone-50 sm:text-4xl lg:text-5xl">
                {style.copy.visualizerTitle}
              </h2>
              <p className="mt-5 text-stone-400 leading-relaxed editorial-prose">
                {style.copy.visualizerDescription}
              </p>
              <ul className="mt-8 space-y-3 text-sm text-stone-500">
                <li className="flex items-center gap-3">
                  <span className="h-px w-6 bg-accent" />
                  Upload exterior photo
                </li>
                <li className="flex items-center gap-3">
                  <span className="h-px w-6 bg-accent" />
                  Choose style &amp; finish
                </li>
                <li className="flex items-center gap-3">
                  <span className="h-px w-6 bg-accent" />
                  Preview in seconds
                </li>
              </ul>
              <Button variant="accent" className="mt-10 w-fit" asChild>
                <Link href="/contact#visualizer">Join the waitlist</Link>
              </Button>
            </div>
          </FadeIn>
          <FadeIn delay={0.15} className="relative min-h-[320px] lg:min-h-[520px]">
            <ImageZoom className="absolute inset-0 h-full w-full">
              <ArchitecturalImage
                src={visualizer.src}
                alt={visualizer.alt}
                aspect="auto"
                containerClassName="h-full min-h-[320px] lg:min-h-[520px]"
                sizes="(max-width: 1024px) 100vw, 50vw"
              />
            </ImageZoom>
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

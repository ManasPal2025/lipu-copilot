'use client';

import { useCity } from '@/components/providers/city-provider';
import { ArchitecturalImage } from '@/components/ui/architectural-image';

export function ContactVisualizerPreview() {
  const { getImage, style } = useCity();
  const visualizer = getImage('visualizer');

  return (
    <div id="visualizer" className="relative mt-12 overflow-hidden rounded-sm border border-border">
      <ArchitecturalImage
        src={visualizer.src}
        alt={visualizer.alt}
        aspect="video"
        className="opacity-25"
        sizes="(max-width: 1024px) 100vw, 58vw"
      />
      <div className="absolute inset-0 bg-background/90" />
      <div className="relative p-8 text-center sm:p-12">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">Coming soon</p>
        <h3 className="mt-4 font-display text-2xl sm:text-3xl">{style.copy.visualizerTitle}</h3>
        <p className="mx-auto mt-3 max-w-md text-sm text-muted-foreground editorial-prose">
          {style.copy.visualizerDescription} Join the waitlist through the consultation form.
        </p>
      </div>
    </div>
  );
}

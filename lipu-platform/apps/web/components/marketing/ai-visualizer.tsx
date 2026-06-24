import Link from 'next/link';
import { Sparkles } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, ImagePlaceholder, Section } from '@/components/layout/section';
import { Button } from '@/components/ui/button';

export function AIVisualizerSection() {
  return (
    <Section id="visualizer">
      <Container>
        <div className="grid items-center gap-12 overflow-hidden rounded-sm border border-border lg:grid-cols-2">
          <FadeIn>
            <div className="p-8 sm:p-12 lg:p-16">
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border px-4 py-1.5 text-xs uppercase tracking-[0.15em] text-muted-foreground">
                <Sparkles className="h-3.5 w-3.5" aria-hidden />
                Coming soon
              </div>
              <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl">See your home transformed</h2>
              <p className="mt-4 text-muted-foreground leading-relaxed">
                Upload a photo of your home. Our AI visualizer will show you how premium UPVC windows and doors
                could transform your facade — before you commit to anything.
              </p>
              <ul className="mt-6 space-y-2 text-sm text-muted-foreground">
                <li>· Upload exterior photo</li>
                <li>· Choose style &amp; finish</li>
                <li>· Preview in seconds</li>
              </ul>
              <Button variant="accent" className="mt-8" asChild>
                <Link href="/contact#visualizer">Join the waitlist</Link>
              </Button>
            </div>
          </FadeIn>
          <FadeIn delay={0.15}>
            <ImagePlaceholder label="AI visualization preview — home facade transformation" aspect="square" className="min-h-[320px] lg:min-h-full" />
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

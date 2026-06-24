import Link from 'next/link';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { Button } from '@/components/ui/button';

export function QuoteCTASection() {
  return (
    <Section className="border-t border-border">
      <Container size="narrow">
        <FadeIn>
          <div className="text-center">
            <p className="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">Begin</p>
            <h2 className="mt-4 font-display text-4xl sm:text-5xl">Your transformation starts here</h2>
            <p className="mx-auto mt-4 max-w-xl text-muted-foreground leading-relaxed">
              Tell us about your home. We will respond with a thoughtful consultation — not a sales pitch.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
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

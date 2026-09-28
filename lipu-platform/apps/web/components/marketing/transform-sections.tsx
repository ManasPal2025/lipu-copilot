import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF } from '@/lib/constants';
import { images } from '@/lib/images';

const STEPS = [
  { n: '01', title: 'Upload your space', body: 'A room, balcony, terrace, or facade.' },
  { n: '02', title: 'Choose what to explore', body: 'Windows, doors, or an outdoor opening.' },
  { n: '03', title: 'Visualize the possibility', body: 'See a direction for how it could feel.' },
] as const;

export function TransformHero() {
  return (
    <Section className="pb-6 pt-24 sm:pb-8 sm:pt-28 lg:pb-8 lg:pt-32">
      <Container>
        <div className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12">
          <FadeIn>
            <p className="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">
              Transform
            </p>
            <h1 className="mt-3 max-w-xl font-display text-[2.25rem] leading-[1.08] sm:text-4xl lg:text-[3.25rem]">
              Transform Your Space
            </h1>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-muted-foreground sm:text-[15px]">
              See how new windows, doors, and architectural openings could change the character of your space.
            </p>
          </FadeIn>

          <FadeIn delay={0.06}>
            <ArchitecturalImage
              src={images.ecotechTransform.hero.src}
              alt={images.ecotechTransform.hero.alt}
              aspect="video"
              priority
              sizes="(max-width: 1024px) 100vw, 50vw"
              containerClassName="rounded-md"
            />
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

export function TransformHowItWorks() {
  return (
    <Section className="py-8 sm:py-10 lg:py-12">
      <Container>
        <FadeIn>
          <div className="grid gap-6 sm:grid-cols-3 sm:gap-8">
            {STEPS.map((step) => (
              <div key={step.n}>
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">{step.n}</p>
                <h2 className="mt-2 font-display text-xl">{step.title}</h2>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{step.body}</p>
              </div>
            ))}
          </div>
        </FadeIn>
      </Container>
    </Section>
  );
}

export function TransformConsultation() {
  return (
    <Section>
      <Container>
        <FadeIn>
          <div className="mx-auto max-w-3xl text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
              Next step
            </p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.5rem]">
              Like what you see? Let&apos;s make it real.
            </h2>
            <p className="mx-auto mt-4 max-w-md text-sm leading-relaxed text-muted-foreground sm:text-[15px]">
              A visualization is a starting point. We will help you specify what is possible for your project.
            </p>
            <Button size="lg" className="mt-7 rounded-full" asChild>
              <Link href={CONSULTATION_HREF}>
                Request a Consultation
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </div>
        </FadeIn>
      </Container>
    </Section>
  );
}

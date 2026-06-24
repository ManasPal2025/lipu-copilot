import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, ImagePlaceholder, Section, SectionHeader } from '@/components/layout/section';
import { stats } from '@/lib/mock-data';

export function TransformationSection() {
  return (
    <Section>
      <Container>
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-20">
          <FadeIn>
            <SectionHeader
              eyebrow="The LIPU difference"
              title="Transformation before specification"
              description="Every project begins with a vision — how you want to live, not what you want to buy. Our process is designed around that truth."
            />
            <p className="mb-8 max-w-lg text-muted-foreground leading-relaxed">
              From coastal villas to urban penthouses, we partner with homeowners, architects, and designers to
              reimagine how space, light, and silence define a home.
            </p>
            <Link
              href="/about"
              className="inline-flex items-center gap-2 text-sm font-medium tracking-wide hover:text-accent"
            >
              Our philosophy
              <ArrowUpRight className="h-4 w-4" />
            </Link>
          </FadeIn>
          <FadeIn delay={0.15}>
            <ImagePlaceholder label="Interior flooded with natural light after transformation" aspect="portrait" />
          </FadeIn>
        </div>

        <div className="mt-20 grid grid-cols-2 gap-8 border-t border-border pt-12 lg:grid-cols-4">
          {stats.map((stat, i) => (
            <FadeIn key={stat.label} delay={i * 0.08}>
              <p className="font-display text-3xl sm:text-4xl">{stat.value}</p>
              <p className="mt-2 text-sm text-muted-foreground">{stat.label}</p>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

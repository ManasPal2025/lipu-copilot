import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { stats } from '@/lib/mock-data';

export function HeroStatsStrip() {
  return (
    <Section className="border-y border-border bg-stone-925 py-12 text-stone-50 lg:py-16">
      <Container>
        <div className="grid grid-cols-2 gap-8 lg:grid-cols-4 lg:gap-12">
          {stats.map((stat, i) => (
            <FadeIn key={stat.label} delay={i * 0.06}>
              <p className="font-display text-3xl sm:text-4xl lg:text-5xl">{stat.value}</p>
              <p className="mt-2 text-xs uppercase tracking-[0.15em] text-stone-500">{stat.label}</p>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

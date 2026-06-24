import type { Metadata } from 'next';
import Link from 'next/link';

import { PageHero } from '@/components/layout/page-hero';
import { Container, ImagePlaceholder, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { Button } from '@/components/ui/button';
import { companyValues, stats, teamMembers } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'About',
  description: 'LIPU exists to transform how Indian homes experience light, silence, and space.',
};

export default function AboutPage() {
  return (
    <>
      <PageHero
        eyebrow="About LIPU"
        title="We sell transformation, not windows"
        description="Founded on a simple belief: the right envelope changes how you live. We partner with homeowners and architects to make that change real."
      />

      <Section>
        <Container>
          <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-20">
            <FadeIn>
              <ImagePlaceholder label="Craftsperson inspecting window profile — atelier quality" aspect="portrait" />
            </FadeIn>
            <FadeIn delay={0.1}>
              <h2 className="font-display text-3xl sm:text-4xl">Craft meets climate</h2>
              <p className="mt-4 leading-relaxed text-muted-foreground">
                India demands more from building envelopes than most markets. Heat, monsoon, coastal salt, urban noise —
                our profiles are engineered for all of it, without sacrificing the architectural clarity you expect from
                international brands like Pella, Andersen, and REHAU.
              </p>
              <p className="mt-4 leading-relaxed text-muted-foreground">
                Our process is closer to Apple and Tesla: obsessive detail, honest communication, and an experience that
                feels premium from first touch to final install.
              </p>
              <Button variant="accent" className="mt-8" asChild>
                <Link href="/contact">Meet our team</Link>
              </Button>
            </FadeIn>
          </div>
        </Container>
      </Section>

      <Section className="border-t border-border bg-muted/30">
        <Container>
          <FadeIn>
            <h2 className="font-display text-3xl sm:text-4xl">What we believe</h2>
          </FadeIn>
          <div className="mt-12 grid gap-8 md:grid-cols-3">
            {companyValues.map((value, i) => (
              <FadeIn key={value.title} delay={i * 0.08}>
                <div className="border-t border-border pt-6">
                  <h3 className="font-display text-xl">{value.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{value.description}</p>
                </div>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <Section>
        <Container>
          <FadeIn>
            <h2 className="font-display text-3xl sm:text-4xl">Leadership</h2>
          </FadeIn>
          <div className="mt-12 grid gap-8 sm:grid-cols-3">
            {teamMembers.map((member, i) => (
              <FadeIn key={member.id} delay={i * 0.08}>
                <div className="border-t border-border pt-6">
                  <div className="mb-4 h-16 w-16 rounded-full image-placeholder" aria-hidden />
                  <h3 className="font-display text-xl">{member.name}</h3>
                  <p className="mt-1 text-xs uppercase tracking-wider text-accent">{member.role}</p>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{member.bio}</p>
                </div>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <Section className="border-t border-border">
        <Container>
          <div className="grid grid-cols-2 gap-8 lg:grid-cols-4">
            {stats.map((stat, i) => (
              <FadeIn key={stat.label} delay={i * 0.06}>
                <p className="font-display text-3xl sm:text-4xl">{stat.value}</p>
                <p className="mt-2 text-sm text-muted-foreground">{stat.label}</p>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

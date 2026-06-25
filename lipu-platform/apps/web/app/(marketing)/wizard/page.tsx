import type { Metadata } from 'next';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { RecommendationWizard } from '@/components/mvp/wizard/recommendation-wizard';
import { QuoteCTASection } from '@/components/marketing/quote-cta';

export const metadata: Metadata = {
  title: 'Find Your Window & Door Ideas',
  description:
    'Answer five quick questions about your home in Bhubaneswar or Odisha — get a personalised UPVC profile and design inspiration.',
};

export default function WizardPage() {
  return (
    <>
      <PageHero
        eyebrow="Recommendation wizard"
        title="Ideas for your home, in five steps"
        description="Tell us about your apartment or villa, the room you are planning, and your comfort priorities. We will suggest a UPVC system and real-home photos to match."
        align="center"
        image={{
          src: '/images/inspiration/living-room/03.jpg',
          alt: 'Warm living space with soft daylight through wide glass openings',
        }}
      />

      <Section className="bg-muted/15">
        <Container size="narrow">
          <RecommendationWizard />
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

import type { Metadata } from 'next';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { CostEstimator } from '@/components/mvp/estimator/cost-estimator';
import { QuoteCTASection } from '@/components/marketing/quote-cta';

export const metadata: Metadata = {
  title: 'UPVC Window Cost Estimator',
  description:
    'Get an indicative price range for UPVC windows and doors in Bhubaneswar and Odisha — enter dimensions, window type, and glass option.',
};

export default function EstimatePage() {
  return (
    <>
      <PageHero
        eyebrow="Cost estimator"
        title="What might it cost?"
        description="Enter your opening size, window type, and glass choice for a ballpark estimate. Final pricing always follows a site visit — never a form on a website."
        align="center"
        image={{
          src: '/images/inspiration/apartment/04.jpg',
          alt: 'Contemporary Indian apartment living room with city views',
        }}
      />

      <Section className="bg-muted/15">
        <Container size="narrow">
          <CostEstimator />
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

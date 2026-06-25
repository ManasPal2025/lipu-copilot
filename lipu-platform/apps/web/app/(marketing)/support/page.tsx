import type { Metadata } from 'next';
import { Clock, HeartHandshake, ShieldCheck } from 'lucide-react';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { ComplaintForm } from '@/components/mvp/support/complaint-form';
import { FadeIn } from '@/components/motion/fade-in';

export const metadata: Metadata = {
  title: 'Customer Support',
  description:
    'Report an issue with your LIPU UPVC windows or doors in Bhubaneswar and Odisha. We respond within one business day.',
};

const assurances = [
  {
    icon: HeartHandshake,
    title: 'We listen first',
    description: 'Every message is read by our support team — not an automated queue.',
  },
  {
    icon: Clock,
    title: 'Call back within 24 hours',
    description: 'Share your number and we will reach you on the next business day.',
  },
  {
    icon: ShieldCheck,
    title: 'Warranty honoured',
    description: 'Installation and product issues are resolved under our warranty policy.',
  },
];

export default function SupportPage() {
  return (
    <>
      <PageHero
        eyebrow="Customer support"
        title="We are here to help"
        description="Something not quite right with your windows or doors? Tell us in your own words. No login required — just your name, phone, and a clear description."
        align="center"
        image={{
          src: '/images/inspiration/bedroom/02.jpg',
          alt: 'Calm bedroom interior with natural light through UPVC windows',
        }}
      />

      <Section className="bg-muted/15">
        <Container size="narrow">
          <FadeIn>
            <div className="mb-12 grid gap-6 sm:grid-cols-3">
              {assurances.map((item) => (
                <div key={item.title} className="border-t border-border pt-5">
                  <item.icon className="h-5 w-5 text-accent" aria-hidden />
                  <p className="mt-3 font-display text-lg">{item.title}</p>
                  <p className="mt-2 text-sm text-muted-foreground">{item.description}</p>
                </div>
              ))}
            </div>
          </FadeIn>

          <ComplaintForm />
        </Container>
      </Section>
    </>
  );
}

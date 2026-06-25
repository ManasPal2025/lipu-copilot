import type { Metadata } from 'next';
import { BookOpen, Leaf, Shield } from 'lucide-react';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { ConsultChat } from '@/components/mvp/consult/consult-chat';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { FadeIn } from '@/components/motion/fade-in';

export const metadata: Metadata = {
  title: 'UPVC Consultant',
  description:
    'Ask practical questions about UPVC windows and doors for your home in Bhubaneswar and Odisha — glass, noise, heat, and monsoon performance.',
};

const highlights = [
  {
    icon: BookOpen,
    title: 'Grounded in our knowledge base',
    description: 'Answers draw from Odisha-specific product guides, FAQs, and installation notes.',
  },
  {
    icon: Leaf,
    title: 'Climate-aware advice',
    description: 'Heat, humidity, monsoon rain, and coastal conditions — not generic catalogue copy.',
  },
  {
    icon: Shield,
    title: 'No login required',
    description: 'Ask freely. Nothing is stored — refresh the page to start a new conversation.',
  },
];

export default function ConsultPage() {
  return (
    <>
      <PageHero
        eyebrow="UPVC consultant"
        title="Questions about your home?"
        description="Ask about window types, glass choices, noise reduction, or cyclone readiness for Bhubaneswar and across Odisha. Practical answers — not a sales pitch."
        align="center"
        image={{
          src: '/images/inspiration/balcony/04.jpg',
          alt: 'Balcony with wide glass openings overlooking a Bhubaneswar neighbourhood',
        }}
      />

      <Section className="bg-muted/15">
        <Container size="narrow">
          <FadeIn>
            <div className="mb-10 grid gap-6 sm:grid-cols-3">
              {highlights.map((item) => (
                <div key={item.title} className="border-t border-border pt-5">
                  <item.icon className="h-5 w-5 text-accent" aria-hidden />
                  <p className="mt-3 font-display text-lg">{item.title}</p>
                  <p className="mt-2 text-sm text-muted-foreground">{item.description}</p>
                </div>
              ))}
            </div>
          </FadeIn>

          <ConsultChat />
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

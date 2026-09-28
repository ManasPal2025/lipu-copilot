import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { Button } from '@/components/ui/button';
import { CONSULTATION_HREF } from '@/lib/constants';

const audiences = ['Residential', 'Commercial', 'Hospitality', 'Large architectural projects'] as const;

export function HomeConsultationSection() {
  return (
    <Section className="bg-stone-925 text-stone-50">
      <Container>
        <FadeIn>
          <div className="mx-auto max-w-3xl text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-stone-400">Let&apos;s talk</p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.5rem]">
              Have a project in mind?
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-sm leading-relaxed text-stone-400 sm:text-[15px]">
              Share your vision. We help homeowners, architects, and project teams specify openings and spaces that
              perform beautifully in Odisha&apos;s climate.
            </p>

            <ul className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-[13px] text-stone-300">
              {audiences.map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="h-1 w-1 rounded-full bg-stone-500" aria-hidden />
                  {item}
                </li>
              ))}
            </ul>

            <Button
              size="lg"
              className="mt-7 rounded-full bg-stone-50 text-stone-925 hover:bg-white"
              asChild
            >
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

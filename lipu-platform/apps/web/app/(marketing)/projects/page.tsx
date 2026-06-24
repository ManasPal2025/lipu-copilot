import type { Metadata } from 'next';
import Link from 'next/link';

import { PageHero } from '@/components/layout/page-hero';
import { Container, ImagePlaceholder, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { Button } from '@/components/ui/button';
import { featuredProjects } from '@/lib/mock-data';

export const metadata: Metadata = {
  title: 'Projects',
  description:
    'Case studies in home transformation — residential, commercial, and heritage projects across India.',
};

export default function ProjectsPage() {
  return (
    <>
      <PageHero
        eyebrow="Case studies"
        title="Every project, a transformation"
        description="From first consultation to final installation — stories of homes reimagined through light, silence, and craft."
        dark
      />

      <Section dark className="!pt-0">
        <Container>
          <div className="space-y-24">
            {featuredProjects.map((project, i) => (
              <FadeIn key={project.id} delay={i * 0.04}>
                <article
                  className={`grid gap-8 lg:grid-cols-12 lg:gap-12 ${i % 2 === 1 ? 'lg:[&>*:first-child]:order-2' : ''}`}
                >
                  <div className="lg:col-span-7">
                    <ImagePlaceholder label={project.imageLabel} aspect="wide" />
                  </div>
                  <div className="flex flex-col justify-center lg:col-span-5">
                    <p className="text-xs uppercase tracking-[0.2em] text-stone-500">
                      {project.location} · {project.type}
                    </p>
                    <h2 className="mt-3 font-display text-3xl text-stone-50 sm:text-4xl">{project.title}</h2>
                    <p className="mt-4 leading-relaxed text-stone-400">{project.description}</p>

                    <dl className="mt-8 grid grid-cols-2 gap-4 border-t border-stone-800 pt-6 text-sm">
                      <div>
                        <dt className="text-stone-500">Windows</dt>
                        <dd className="mt-1 text-stone-200">{project.windows}</dd>
                      </div>
                      <div>
                        <dt className="text-stone-500">Doors</dt>
                        <dd className="mt-1 text-stone-200">{project.doors}</dd>
                      </div>
                      <div>
                        <dt className="text-stone-500">Duration</dt>
                        <dd className="mt-1 text-stone-200">{project.duration}</dd>
                      </div>
                      {project.architect && (
                        <div>
                          <dt className="text-stone-500">Architect</dt>
                          <dd className="mt-1 text-stone-200">{project.architect}</dd>
                        </div>
                      )}
                    </dl>

                    <Button
                      variant="outline"
                      className="mt-8 w-fit border-stone-700 text-stone-100 hover:bg-stone-800"
                      asChild
                    >
                      <Link href="/contact#quote">Start a similar project</Link>
                    </Button>
                  </div>
                </article>
              </FadeIn>
            ))}
          </div>
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

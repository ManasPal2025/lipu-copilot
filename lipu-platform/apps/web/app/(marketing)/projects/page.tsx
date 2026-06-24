import type { Metadata } from 'next';
import Link from 'next/link';

import { PageHero } from '@/components/layout/page-hero';
import { Container, Section } from '@/components/layout/section';
import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { QuoteCTASection } from '@/components/marketing/quote-cta';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images } from '@/lib/images';
import { featuredProjects } from '@/lib/mock-data';
import { cn } from '@/lib/utils';

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
        image={images.pageHero.projects}
      />

      <Section dark className="!pt-0">
        <Container>
          <FadeIn>
            <p className="mb-16 max-w-2xl text-sm uppercase tracking-[0.2em] text-stone-500">
              {featuredProjects.length} transformations · Residential &amp; commercial
            </p>
          </FadeIn>

          <div className="space-y-28 lg:space-y-40">
            {featuredProjects.map((project, i) => {
              const fullBleed = i % 2 === 0;
              return (
                <FadeIn key={project.id} delay={i * 0.04}>
                  <article id={project.slug} className="scroll-mt-28">
                    {fullBleed ? (
                      <div className="relative mb-10 overflow-hidden lg:mb-14">
                        <ImageZoom>
                          <ArchitecturalImage
                            src={project.image.src}
                            alt={project.image.alt}
                            aspect="wide"
                            containerClassName="min-h-[320px] sm:min-h-[420px] lg:min-h-[520px]"
                            sizes="100vw"
                          />
                        </ImageZoom>
                        <div className="absolute inset-0 bg-gradient-to-t from-stone-925/90 via-transparent to-transparent" />
                        <div className="absolute bottom-0 left-0 right-0 p-8 sm:p-12 lg:p-16">
                          <p className="text-xs uppercase tracking-[0.2em] text-stone-400">
                            {String(i + 1).padStart(2, '0')} · {project.location}
                          </p>
                          <h2 className="mt-2 font-display text-4xl text-stone-50 sm:text-5xl lg:text-6xl">
                            {project.title}
                          </h2>
                        </div>
                      </div>
                    ) : null}

                    <div
                      className={cn(
                        fullBleed
                          ? 'max-w-3xl'
                          : 'grid gap-10 lg:grid-cols-12 lg:gap-16 lg:[&>*:first-child]:order-2',
                      )}
                    >
                      {!fullBleed && (
                        <div className="min-w-0 lg:col-span-7">
                          <ImageZoom>
                            <ArchitecturalImage
                              src={project.image.src}
                              alt={project.image.alt}
                              aspect="wide"
                              sizes="(max-width: 1024px) 100vw, 58vw"
                            />
                          </ImageZoom>
                        </div>
                      )}

                      <div
                        className={cn(
                          'flex min-w-0 flex-col justify-center',
                          !fullBleed && 'lg:col-span-5',
                        )}
                      >
                        {!fullBleed && (
                          <>
                            <p className="text-xs uppercase tracking-[0.2em] text-stone-500">
                              {String(i + 1).padStart(2, '0')} · {project.location} · {project.type}
                            </p>
                            <h2 className="mt-4 font-display text-3xl text-stone-50 sm:text-4xl lg:text-5xl">
                              {project.title}
                            </h2>
                          </>
                        )}
                        {fullBleed && (
                          <p className="text-xs uppercase tracking-[0.2em] text-stone-500">{project.type}</p>
                        )}

                        {project.pullQuote && (
                          <p className="mt-6 max-w-[68ch] border-l-2 border-accent pl-5 font-display text-xl leading-snug text-stone-200 sm:text-2xl">
                            {project.pullQuote}
                          </p>
                        )}

                        <p className="mt-5 max-w-[68ch] leading-relaxed text-stone-400 editorial-prose">
                          {project.description}
                        </p>

                        <dl className="mt-10 grid grid-cols-2 gap-6 border-t border-stone-800 pt-8 text-sm">
                          <div>
                            <dt className="text-[10px] uppercase tracking-[0.15em] text-stone-500">Windows</dt>
                            <dd className="mt-2 font-display text-2xl text-stone-200">{project.windows}</dd>
                          </div>
                          <div>
                            <dt className="text-[10px] uppercase tracking-[0.15em] text-stone-500">Doors</dt>
                            <dd className="mt-2 font-display text-2xl text-stone-200">{project.doors}</dd>
                          </div>
                          <div>
                            <dt className="text-[10px] uppercase tracking-[0.15em] text-stone-500">Duration</dt>
                            <dd className="mt-2 font-display text-2xl text-stone-200">{project.duration}</dd>
                          </div>
                          {project.architect && (
                            <div>
                              <dt className="text-[10px] uppercase tracking-[0.15em] text-stone-500">Architect</dt>
                              <dd className="mt-2 text-stone-200">{project.architect}</dd>
                            </div>
                          )}
                        </dl>

                        <Button
                          variant="outline"
                          className="mt-10 w-fit border-stone-700 text-stone-100 hover:bg-stone-800"
                          asChild
                        >
                          <Link href="/contact#quote">Start a similar project</Link>
                        </Button>
                      </div>
                    </div>
                  </article>
                </FadeIn>
              );
            })}
          </div>
        </Container>
      </Section>

      <QuoteCTASection />
    </>
  );
}

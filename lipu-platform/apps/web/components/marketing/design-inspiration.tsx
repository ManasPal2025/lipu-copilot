import { FadeIn } from '@/components/motion/fade-in';
import { Container, ImagePlaceholder, Section, SectionHeader } from '@/components/layout/section';
import { designStyles } from '@/lib/mock-data';
import Link from 'next/link';

export function DesignInspirationSection() {
  return (
    <Section dark>
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Design inspiration"
            title="Find your architectural language"
            description="Every home has a story. We help you discover the design vocabulary that tells yours."
            light
            align="center"
          />
        </FadeIn>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {designStyles.map((style, i) => (
            <FadeIn key={style.id} delay={i * 0.08}>
              <article className="group flex h-full flex-col">
                <ImagePlaceholder label={style.imageLabel} aspect="portrait" />
                <div className="mt-5 flex flex-1 flex-col">
                  <h3 className="font-display text-2xl text-stone-50">{style.name}</h3>
                  <p className="mt-2 flex-1 text-sm leading-relaxed text-stone-400">{style.description}</p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {style.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-full border border-stone-700 px-2.5 py-0.5 text-[10px] uppercase tracking-wider text-stone-500"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            </FadeIn>
          ))}
        </div>

        <FadeIn>
          <p className="mt-12 text-center text-sm text-stone-500">
            Not sure where to begin?{' '}
            <Link href="/contact" className="text-stone-300 underline-offset-4 hover:underline">
              Book a design consultation
            </Link>
          </p>
        </FadeIn>
      </Container>
    </Section>
  );
}

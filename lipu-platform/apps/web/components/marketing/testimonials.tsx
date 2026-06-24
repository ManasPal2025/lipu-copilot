import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { testimonials } from '@/lib/mock-data';

export function TestimonialsSection() {
  return (
    <Section dark>
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Voices"
            title="Transformation, in their words"
            light
            align="center"
          />
        </FadeIn>

        <div className="grid gap-8 md:grid-cols-3">
          {testimonials.map((item, i) => (
            <FadeIn key={item.id} delay={i * 0.1}>
              <blockquote className="flex h-full flex-col border-l border-stone-700 pl-6">
                <p className="font-display text-xl leading-relaxed text-stone-200">&ldquo;{item.quote}&rdquo;</p>
                <footer className="mt-auto pt-6 text-sm text-stone-500">
                  <p className="text-stone-300">{item.name}</p>
                  <p>
                    {item.location} · {item.project}
                  </p>
                </footer>
              </blockquote>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

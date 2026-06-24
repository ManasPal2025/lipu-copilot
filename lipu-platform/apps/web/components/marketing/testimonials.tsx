import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
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

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {testimonials.map((item, i) => (
            <FadeIn key={item.id} delay={i * 0.1}>
              <blockquote className="group flex h-full flex-col overflow-hidden rounded-sm border border-stone-800 bg-stone-900/50">
                <ImageZoom>
                  <ArchitecturalImage
                    src={item.image.src}
                    alt={item.image.alt}
                    aspect="video"
                    sizes="(max-width: 768px) 100vw, 25vw"
                    className="opacity-90 transition-opacity group-hover:opacity-100"
                  />
                </ImageZoom>
                <div className="flex flex-1 flex-col p-6">
                  <p className="font-display text-lg leading-relaxed text-stone-200 lg:text-xl">
                    &ldquo;{item.quote}&rdquo;
                  </p>
                  <footer className="mt-auto pt-6 text-sm text-stone-500">
                    <p className="text-stone-300">{item.name}</p>
                    <p className="mt-1">
                      {item.location} · {item.project}
                    </p>
                  </footer>
                </div>
              </blockquote>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { beforeAfterStories } from '@/lib/mock-data';

export function BeforeAfterSection() {
  return (
    <Section id="before-after" className="bg-muted/20">
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Before & after"
            title="See the shift"
            description="The difference is not just visual. It is acoustic. Thermal. Emotional. This is what transformation feels like."
            align="center"
          />
        </FadeIn>

        <div className="space-y-24 lg:space-y-32">
          {beforeAfterStories.map((story, index) => (
            <FadeIn key={story.id} delay={index * 0.1}>
              <article className="grid gap-10 lg:grid-cols-12 lg:gap-16">
                <div className="lg:col-span-5 lg:py-6">
                  <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{story.location}</p>
                  <h3 className="mt-3 font-display text-3xl sm:text-4xl">{story.title}</h3>
                  <p className="mt-5 text-muted-foreground leading-relaxed editorial-prose">{story.story}</p>
                  <div className="mt-10 space-y-5 border-l-2 border-accent pl-6">
                    <div>
                      <p className="text-[10px] font-medium uppercase tracking-[0.15em] text-muted-foreground">
                        Before
                      </p>
                      <p className="mt-2 text-sm leading-relaxed">{story.beforeLabel}</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-medium uppercase tracking-[0.15em] text-accent">After</p>
                      <p className="mt-2 text-sm leading-relaxed">{story.afterLabel}</p>
                    </div>
                  </div>
                </div>
                <div className="grid gap-5 sm:grid-cols-2 lg:col-span-7">
                  <div>
                    <p className="mb-3 text-[10px] uppercase tracking-[0.15em] text-muted-foreground">Before</p>
                    <ImageZoom>
                      <ArchitecturalImage
                        src={story.beforeImage.src}
                        alt={story.beforeImage.alt}
                        aspect="portrait"
                        className="grayscale-[30%] brightness-90"
                        sizes="(max-width: 640px) 100vw, 35vw"
                      />
                    </ImageZoom>
                  </div>
                  <div>
                    <p className="mb-3 text-[10px] uppercase tracking-[0.15em] text-accent">After</p>
                    <ImageZoom>
                      <ArchitecturalImage
                        src={story.afterImage.src}
                        alt={story.afterImage.alt}
                        aspect="portrait"
                        sizes="(max-width: 640px) 100vw, 35vw"
                      />
                    </ImageZoom>
                  </div>
                </div>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>
    </Section>
  );
}

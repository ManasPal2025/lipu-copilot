import { FadeIn } from '@/components/motion/fade-in';
import { Container, ImagePlaceholder, Section, SectionHeader } from '@/components/layout/section';
import { beforeAfterStories } from '@/lib/mock-data';

export function BeforeAfterSection() {
  return (
    <Section id="before-after">
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Before & after"
            title="See the shift"
            description="The difference is not just visual. It is acoustic. Thermal. Emotional. This is what transformation feels like."
            align="center"
          />
        </FadeIn>

        <div className="space-y-20">
          {beforeAfterStories.map((story, index) => (
            <FadeIn key={story.id} delay={index * 0.1}>
              <article className="grid gap-8 lg:grid-cols-12 lg:gap-10">
                <div className="lg:col-span-5 lg:py-8">
                  <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{story.location}</p>
                  <h3 className="mt-2 font-display text-3xl">{story.title}</h3>
                  <p className="mt-4 text-muted-foreground leading-relaxed">{story.story}</p>
                  <div className="mt-8 space-y-4 border-l-2 border-accent pl-5">
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Before</p>
                      <p className="mt-1 text-sm">{story.beforeLabel}</p>
                    </div>
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-accent">After</p>
                      <p className="mt-1 text-sm">{story.afterLabel}</p>
                    </div>
                  </div>
                </div>
                <div className="grid gap-4 sm:grid-cols-2 lg:col-span-7">
                  <div>
                    <p className="mb-2 text-xs uppercase tracking-wider text-muted-foreground">Before</p>
                    <ImagePlaceholder label={`Before — ${story.title}`} aspect="portrait" />
                  </div>
                  <div>
                    <p className="mb-2 text-xs uppercase tracking-wider text-accent">After</p>
                    <ImagePlaceholder label={`After — ${story.title}`} aspect="portrait" />
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

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { TRANSFORM_HREF } from '@/lib/constants';
import { images } from '@/lib/images';

export function HomeTransformSection() {
  return (
    <Section className="bg-muted/20" id="transform">
      <Container>
        <div className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12">
          <FadeIn>
            <div className="relative overflow-hidden rounded-md border border-border bg-background shadow-sm">
              <div className="grid grid-cols-2">
                <div className="relative">
                  <ArchitecturalImage
                    src={images.ecotechHome.transformBefore.src}
                    alt={images.ecotechHome.transformBefore.alt}
                    aspect="portrait"
                    sizes="(max-width: 1024px) 50vw, 25vw"
                    className="grayscale-[25%] brightness-90"
                  />
                  <span className="absolute left-3 top-3 rounded-full bg-background/90 px-3 py-1 text-[10px] uppercase tracking-[0.15em] text-muted-foreground backdrop-blur-sm">
                    Before
                  </span>
                </div>
                <div className="relative">
                  <ArchitecturalImage
                    src={images.ecotechHome.transformAfter.src}
                    alt={images.ecotechHome.transformAfter.alt}
                    aspect="portrait"
                    sizes="(max-width: 1024px) 50vw, 25vw"
                  />
                  <span className="absolute left-3 top-3 rounded-full bg-foreground px-3 py-1 text-[10px] uppercase tracking-[0.15em] text-background">
                    After
                  </span>
                </div>
              </div>
            </div>
          </FadeIn>

          <FadeIn delay={0.1}>
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
              Visualize your home
            </p>
            <h2 className="mt-3 font-display text-[1.75rem] leading-[1.12] sm:text-[2rem] lg:text-[2.5rem]">
              See your space differently
            </h2>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-muted-foreground sm:text-[15px]">
              Preview how Ecotech windows and doors can transform your home — then talk with our team about what is
              possible for your project.
            </p>
            <Button size="lg" className="mt-8 rounded-full" asChild>
              <Link href={TRANSFORM_HREF}>
                Transform Your Space
                <ArrowRight className="ml-1" />
              </Link>
            </Button>
          </FadeIn>
        </div>
      </Container>
    </Section>
  );
}

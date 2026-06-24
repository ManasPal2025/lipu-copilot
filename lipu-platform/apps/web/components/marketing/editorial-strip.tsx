import { FadeIn } from '@/components/motion/fade-in';
import { ParallaxImage } from '@/components/motion/parallax-image';
import { Container } from '@/components/layout/section';
import { images } from '@/lib/images';

export function EditorialStrip() {
  return (
    <section className="relative min-h-[50vh] overflow-hidden lg:min-h-[60vh]" aria-label="Editorial">
      <ParallaxImage
        src={images.editorialStrip.src}
        alt={images.editorialStrip.alt}
        overlayClassName="luxury-gradient-overlay"
      />
      <div className="absolute inset-0 bg-stone-925/40" />

      <Container className="relative flex min-h-[50vh] items-center lg:min-h-[60vh]">
        <FadeIn>
          <blockquote className="max-w-3xl">
            <p className="font-display text-3xl leading-[1.15] text-stone-50 sm:text-4xl lg:text-5xl">
              &ldquo;Architecture is the thoughtful making of space. We begin where the glass meets the light.&rdquo;
            </p>
            <footer className="mt-8 text-xs uppercase tracking-[0.25em] text-stone-400">
              The LIPU philosophy
            </footer>
          </blockquote>
        </FadeIn>
      </Container>
    </section>
  );
}

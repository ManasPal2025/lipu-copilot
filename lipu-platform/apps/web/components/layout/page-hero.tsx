import { FadeIn } from '@/components/motion/fade-in';
import { ParallaxImage } from '@/components/motion/parallax-image';
import { Container } from '@/components/layout/section';
import type { ImageAsset } from '@/lib/images';
import { cn } from '@/lib/utils';

interface PageHeroProps {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: 'left' | 'center';
  dark?: boolean;
  image?: ImageAsset;
}

export function PageHero({
  eyebrow,
  title,
  description,
  align = 'left',
  dark = false,
  image,
}: PageHeroProps) {
  if (image) {
    return (
      <section className="relative min-h-[55vh] overflow-hidden border-b border-stone-800 lg:min-h-[62vh]" aria-label={title}>
        <ParallaxImage
          src={image.src}
          alt={image.alt}
          priority
          overlayClassName="luxury-gradient-overlay"
        />
        <div className="absolute inset-0 bg-stone-925/30" />

        <div className="relative flex min-h-[55vh] flex-col justify-end px-5 pb-16 pt-32 sm:px-6 lg:min-h-[62vh] lg:px-8 lg:pb-20">
          <Container>
            <FadeIn>
              <div className={cn('max-w-3xl', align === 'center' && 'mx-auto text-center')}>
                {eyebrow && (
                  <p className="mb-4 text-xs font-medium uppercase tracking-[0.25em] text-stone-300">
                    {eyebrow}
                  </p>
                )}
                <h1 className="font-display text-4xl leading-[1.05] text-stone-50 sm:text-5xl lg:text-6xl">
                  {title}
                </h1>
                {description && (
                  <p className="mt-5 max-w-2xl text-base leading-relaxed text-stone-300 sm:text-lg editorial-prose">
                    {description}
                  </p>
                )}
              </div>
            </FadeIn>
          </Container>
        </div>
      </section>
    );
  }

  return (
    <section
      className={cn(
        'border-b border-border pt-28 sm:pt-32',
        dark ? 'bg-stone-925 text-stone-50' : 'bg-background',
      )}
    >
      <Container>
        <FadeIn>
          <div className={cn('max-w-3xl', align === 'center' && 'mx-auto text-center')}>
            {eyebrow && (
              <p
                className={cn(
                  'mb-4 text-xs font-medium uppercase tracking-[0.2em]',
                  dark ? 'text-stone-400' : 'text-muted-foreground',
                )}
              >
                {eyebrow}
              </p>
            )}
            <h1
              className={cn(
                'font-display text-4xl leading-[1.05] sm:text-5xl lg:text-6xl',
                dark ? 'text-stone-50' : '',
              )}
            >
              {title}
            </h1>
            {description && (
              <p
                className={cn(
                  'mt-5 text-base leading-relaxed sm:text-lg editorial-prose',
                  dark ? 'text-stone-400' : 'text-muted-foreground',
                )}
              >
                {description}
              </p>
            )}
          </div>
        </FadeIn>
      </Container>
      <div className="h-12 sm:h-16" />
    </section>
  );
}

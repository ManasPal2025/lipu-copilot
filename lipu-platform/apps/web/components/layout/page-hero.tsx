import { FadeIn } from '@/components/motion/fade-in';
import { Container } from '@/components/layout/section';

interface PageHeroProps {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: 'left' | 'center';
  dark?: boolean;
}

export function PageHero({ eyebrow, title, description, align = 'left', dark = false }: PageHeroProps) {
  return (
    <section
      className={`border-b border-border pt-28 sm:pt-32 ${dark ? 'bg-stone-925 text-stone-50' : 'bg-background'}`}
    >
      <Container>
        <FadeIn>
          <div className={align === 'center' ? 'mx-auto max-w-3xl text-center' : 'max-w-3xl'}>
            {eyebrow && (
              <p
                className={`mb-4 text-xs font-medium uppercase tracking-[0.2em] ${dark ? 'text-stone-400' : 'text-muted-foreground'}`}
              >
                {eyebrow}
              </p>
            )}
            <h1 className={`font-display text-4xl leading-tight sm:text-5xl lg:text-6xl ${dark ? 'text-stone-50' : ''}`}>
              {title}
            </h1>
            {description && (
              <p
                className={`mt-5 text-base leading-relaxed sm:text-lg ${dark ? 'text-stone-400' : 'text-muted-foreground'}`}
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

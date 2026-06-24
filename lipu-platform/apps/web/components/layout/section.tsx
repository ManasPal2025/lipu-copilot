import { cn } from '@/lib/utils';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  size?: 'default' | 'narrow' | 'wide';
}

export function Container({ children, className, size = 'default' }: ContainerProps) {
  return (
    <div
      className={cn(
        'mx-auto w-full px-5 sm:px-6 lg:px-8',
        size === 'narrow' && 'max-w-4xl',
        size === 'default' && 'max-w-7xl',
        size === 'wide' && 'max-w-[1400px]',
        className,
      )}
    >
      {children}
    </div>
  );
}

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
  dark?: boolean;
}

export function Section({ children, className, id, dark = false }: SectionProps) {
  return (
    <section
      id={id}
      className={cn(
        'py-16 sm:py-20 lg:py-28',
        dark && 'bg-stone-925 text-stone-50',
        className,
      )}
    >
      {children}
    </section>
  );
}

interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: 'left' | 'center';
  light?: boolean;
}

export function SectionHeader({ eyebrow, title, description, align = 'left', light = false }: SectionHeaderProps) {
  return (
    <div className={cn('mb-12 max-w-3xl', align === 'center' && 'mx-auto text-center')}>
      {eyebrow && (
        <p
          className={cn(
            'mb-4 text-xs font-medium uppercase tracking-[0.2em]',
            light ? 'text-stone-400' : 'text-muted-foreground',
          )}
        >
          {eyebrow}
        </p>
      )}
      <h2
        className={cn(
          'font-display text-3xl leading-tight sm:text-4xl lg:text-5xl',
          light ? 'text-stone-50' : 'text-foreground',
        )}
      >
        {title}
      </h2>
      {description && (
        <p
          className={cn(
            'mt-4 text-base leading-relaxed sm:text-lg',
            light ? 'text-stone-400' : 'text-muted-foreground',
          )}
        >
          {description}
        </p>
      )}
    </div>
  );
}

interface ImagePlaceholderProps {
  label: string;
  className?: string;
  aspect?: 'video' | 'square' | 'portrait' | 'wide' | 'hero';
}

export function ImagePlaceholder({ label, className, aspect = 'video' }: ImagePlaceholderProps) {
  const aspectClass = {
    video: 'aspect-video',
    square: 'aspect-square',
    portrait: 'aspect-[3/4]',
    wide: 'aspect-[21/9]',
    hero: 'aspect-[4/5] sm:aspect-[16/9] lg:aspect-[21/9]',
  }[aspect];

  return (
    <div
      className={cn('image-placeholder relative w-full', aspectClass, className)}
      role="img"
      aria-label={label}
    >
      <div className="absolute inset-0 flex items-end p-6 sm:p-8">
        <p className="max-w-md text-xs uppercase tracking-[0.15em] text-stone-600/80 dark:text-stone-400/80">
          {label}
        </p>
      </div>
    </div>
  );
}

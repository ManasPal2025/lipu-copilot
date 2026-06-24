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
        'py-20 sm:py-24 lg:py-32',
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
  className?: string;
}

export function SectionHeader({ eyebrow, title, description, align = 'left', light = false, className }: SectionHeaderProps) {
  return (
    <div className={cn('mb-12 max-w-3xl', align === 'center' && 'mx-auto text-center', className)}>
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
          'font-display text-3xl leading-[1.1] sm:text-4xl lg:text-[3.25rem] lg:leading-[1.08]',
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

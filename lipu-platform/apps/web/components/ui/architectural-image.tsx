import Image from 'next/image';

import type { AspectRatio } from '@/lib/images';
import { cn } from '@/lib/utils';

/**
 * Full class strings must live in this file.
 * Tailwind only scans app/ and components/, so the map in lib/images.ts is purged.
 */
const aspectClasses: Record<AspectRatio, string> = {
  video: 'aspect-video',
  square: 'aspect-square',
  portrait: 'aspect-[3/4]',
  wide: 'aspect-[21/9]',
  hero: 'aspect-[4/5] sm:aspect-[16/9] lg:aspect-[21/9]',
  auto: '',
};

interface ArchitecturalImageProps {
  src: string;
  alt: string;
  aspect?: AspectRatio;
  className?: string;
  containerClassName?: string;
  priority?: boolean;
  sizes?: string;
  quality?: number;
}

export function ArchitecturalImage({
  src,
  alt,
  aspect = 'video',
  className,
  containerClassName,
  priority = false,
  sizes = '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw',
  quality = 85,
}: ArchitecturalImageProps) {
  return (
    <div
      className={cn(
        'relative overflow-hidden bg-stone-200 dark:bg-stone-900',
        aspect !== 'auto' && aspectClasses[aspect],
        aspect === 'auto' && 'h-full w-full min-h-[240px]',
        containerClassName,
      )}
    >
      <Image
        src={src}
        alt={alt}
        fill
        className={cn('object-cover', className)}
        sizes={sizes}
        priority={priority}
        quality={quality}
        loading={priority ? undefined : 'lazy'}
      />
    </div>
  );
}

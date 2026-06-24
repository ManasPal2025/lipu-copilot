import Image from 'next/image';

import { aspectClasses, type AspectRatio } from '@/lib/images';
import { cn } from '@/lib/utils';

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

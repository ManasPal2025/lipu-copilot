'use client';

import type { ReactNode } from 'react';

import { cn } from '@/lib/utils';

interface ImageZoomProps {
  children: ReactNode;
  className?: string;
  zoomClassName?: string;
}

/** Luxury hover zoom — subtle scale on editorial imagery */
export function ImageZoom({ children, className, zoomClassName }: ImageZoomProps) {
  return (
    <div className={cn('group/image overflow-hidden', className)}>
      <div
        className={cn(
          'h-full w-full transition-transform duration-700 ease-out group-hover/image:scale-[1.04]',
          zoomClassName,
        )}
      >
        {children}
      </div>
    </div>
  );
}

'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import Image from 'next/image';
import { useRef } from 'react';

import { cn } from '@/lib/utils';

interface ParallaxImageProps {
  src: string;
  alt: string;
  className?: string;
  priority?: boolean;
  overlayClassName?: string;
  objectClassName?: string;
}

/** Subtle parallax for cinematic hero backgrounds */
export function ParallaxImage({ src, alt, className, priority, overlayClassName, objectClassName }: ParallaxImageProps) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start start', 'end start'],
  });
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '6%']);
  const scale = useTransform(scrollYProgress, [0, 1], [1.02, 1.06]);

  return (
    <div ref={ref} className={cn('absolute inset-0 overflow-hidden', className)}>
      <motion.div style={{ y, scale }} className="absolute inset-0 h-[110%] w-full -top-[5%]">
        <Image
          src={src}
          alt={alt}
          fill
          className={cn('object-cover', objectClassName ?? 'object-center')}
          sizes="100vw"
          priority={priority}
          quality={90}
        />
      </motion.div>
      {overlayClassName && <div className={cn('absolute inset-0', overlayClassName)} />}
    </div>
  );
}

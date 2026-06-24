'use client';

import { motion } from 'framer-motion';
import type { ReactNode } from 'react';

interface FadeInProps {
  children: ReactNode;
  className?: string;
  delay?: number;
  direction?: 'up' | 'none';
}

export function FadeIn({ children, className, delay = 0, direction = 'up' }: FadeInProps) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: direction === 'up' ? 28 : 0 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}

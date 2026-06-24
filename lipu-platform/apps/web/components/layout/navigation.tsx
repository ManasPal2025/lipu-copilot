'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

import { NAV_LINKS } from '@/lib/constants';
import { cn } from '@/lib/utils';

interface NavigationProps {
  className?: string;
  linkClassName?: string;
  activeClassName?: string;
  inactiveClassName?: string;
  onNavigate?: () => void;
}

export function Navigation({
  className,
  linkClassName,
  activeClassName = 'text-foreground',
  inactiveClassName = 'text-muted-foreground',
  onNavigate,
}: NavigationProps) {
  const pathname = usePathname();

  return (
    <nav className={cn('flex items-center gap-8', className)} aria-label="Main navigation">
      {NAV_LINKS.map((link) => {
        const isActive = pathname === link.href;
        return (
          <Link
            key={link.href}
            href={link.href}
            onClick={onNavigate}
            className={cn(
              'text-sm tracking-wide transition-colors hover:text-foreground',
              linkClassName,
              isActive ? activeClassName : inactiveClassName,
            )}
            aria-current={isActive ? 'page' : undefined}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}

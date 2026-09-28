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

function isActivePath(pathname: string, href: string): boolean {
  if (href === '/') {
    return pathname === '/';
  }
  return pathname === href || pathname.startsWith(`${href}/`);
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
    <nav className={cn('flex items-center gap-7 xl:gap-9', className)} aria-label="Main navigation">
      {NAV_LINKS.map((link) => {
        const isActive = isActivePath(pathname, link.href);
        return (
          <Link
            key={link.href}
            href={link.href}
            onClick={onNavigate}
            className={cn(
              'text-[13px] tracking-[0.04em] transition-colors',
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

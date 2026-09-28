'use client';

import Link from 'next/link';
import { useEffect, useId, useRef, useState } from 'react';
import { UserRound } from 'lucide-react';

import { useAccount } from '@/components/providers/account-provider';
import { SIGN_IN_HREF } from '@/lib/constants';
import { cn } from '@/lib/utils';

const items = [
  { href: '/profile', label: 'My Profile' },
  { href: '/profile/consultations', label: 'My Consultations' },
  { href: '/profile/transformations', label: 'My Transformations' },
] as const;

export function AccountMenu({ className }: { className?: string }) {
  const account = useAccount();
  const [open, setOpen] = useState(false);
  const menuId = useId();
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onPointer = (event: MouseEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) setOpen(false);
    };
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false);
    };
    document.addEventListener('mousedown', onPointer);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onPointer);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  if (account.status !== 'authenticated') {
    return (
      <Link href={SIGN_IN_HREF} className={className} aria-label="Sign in">
        <UserRound className="h-4 w-4" aria-hidden />
      </Link>
    );
  }

  return (
    <div className="relative" ref={rootRef}>
      <button
        type="button"
        className={className}
        aria-label="Account menu"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls={menuId}
        onClick={() => setOpen((current) => !current)}
      >
        <UserRound className="h-4 w-4" aria-hidden />
      </button>
      {open ? (
        <div
          id={menuId}
          role="menu"
          className="absolute right-0 z-50 mt-2 w-56 max-w-[calc(100vw-2.5rem)] border border-border/70 bg-background/95 p-2 shadow-sm backdrop-blur-md"
        >
          {items.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              role="menuitem"
              className="block px-3 py-2.5 text-sm text-foreground transition-colors hover:bg-muted"
              onClick={() => setOpen(false)}
            >
              {item.label}
            </Link>
          ))}
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-2.5 text-left text-sm text-foreground transition-colors hover:bg-muted"
            onClick={() => {
              setOpen(false);
              void account.signOut();
            }}
          >
            Sign Out
          </button>
        </div>
      ) : null}
    </div>
  );
}

export function AccountMenuLinks({ onNavigate }: { onNavigate: () => void }) {
  const account = useAccount();

  if (account.status !== 'authenticated') {
    return (
      <Link
        href={SIGN_IN_HREF}
        onClick={onNavigate}
        className="px-2 py-2 text-sm tracking-wide text-foreground"
      >
        Sign in
      </Link>
    );
  }

  return (
    <div className="flex flex-col">
      {items.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          onClick={onNavigate}
          className="px-2 py-2.5 text-sm text-foreground"
        >
          {item.label}
        </Link>
      ))}
      <button
        type="button"
        className="px-2 py-2.5 text-left text-sm text-foreground"
        onClick={() => {
          onNavigate();
          void account.signOut();
        }}
      >
        Sign Out
      </button>
    </div>
  );
}

export function accountTriggerClass(transparent: boolean, bordered: boolean): string {
  return cn(
    'inline-flex h-10 w-10 items-center justify-center rounded-full transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
    bordered && 'border focus-visible:ring-offset-2',
    transparent
      ? bordered
        ? 'border-stone-400/40 text-stone-100 hover:bg-white/10'
        : 'text-stone-50'
      : bordered
        ? 'border-border text-foreground hover:bg-muted'
        : 'text-foreground',
  );
}

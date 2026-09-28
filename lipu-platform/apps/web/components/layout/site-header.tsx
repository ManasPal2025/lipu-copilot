'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useId, useState } from 'react';
import { Menu, X } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

import { AccountMenu, AccountMenuLinks, accountTriggerClass } from '@/components/account/account-menu';
import { Navigation } from '@/components/layout/navigation';
import { Container } from '@/components/layout/section';
import { Button } from '@/components/ui/button';
import {
  CONSULTATION_HREF,
  NAV_LINKS,
  SITE_LOGO,
  SITE_NAME,
  TRANSFORM_HREF,
} from '@/lib/constants';
import { cn } from '@/lib/utils';

export function SiteHeader() {
  const pathname = usePathname();
  const isHome = pathname === '/';
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const menuId = useId();

  const transparent = isHome && !scrolled;

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 48);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  return (
    <header
      className={cn(
        'fixed inset-x-0 top-0 z-50 transition-colors duration-300',
        transparent
          ? 'bg-transparent'
          : 'border-b border-border/50 bg-background/90 backdrop-blur-md',
      )}
    >
      <Container>
        <div className="flex h-16 items-center justify-between gap-4 sm:h-[4.5rem]">
          <Link
            href="/"
            className="relative flex shrink-0 items-center"
            aria-label={`${SITE_NAME} home`}
          >
            <Image
              src={SITE_LOGO.src}
              alt={SITE_LOGO.alt}
              width={160}
              height={48}
              className="h-9 w-auto object-contain sm:h-10"
              priority
            />
          </Link>

          <Navigation
            className="hidden lg:flex"
            inactiveClassName={
              transparent
                ? 'text-stone-300 hover:text-stone-50'
                : 'text-muted-foreground hover:text-foreground'
            }
            activeClassName={transparent ? 'text-stone-50' : 'text-foreground'}
          />

          <div className="hidden items-center gap-3 lg:flex">
            <Link
              href={TRANSFORM_HREF}
              className={cn(
                'text-[13px] font-medium tracking-wide transition-colors',
                transparent
                  ? 'text-stone-100 hover:text-white'
                  : 'text-foreground hover:text-accent',
              )}
            >
              Transform
            </Link>
            <Button
              variant={transparent ? 'outline' : 'default'}
              size="sm"
              className={cn(
                'rounded-full px-5',
                transparent &&
                  'border-stone-400/50 bg-transparent text-stone-50 hover:bg-white/10 hover:text-white',
              )}
              asChild
            >
              <Link href={CONSULTATION_HREF}>Request a Consultation</Link>
            </Button>
            <AccountMenu className={accountTriggerClass(transparent, true)} />
          </div>

          <div className="flex items-center gap-1 lg:hidden">
            <AccountMenu className={accountTriggerClass(transparent, false)} />
            <button
              type="button"
              className={cn(
                'inline-flex h-10 w-10 items-center justify-center rounded-full transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
                transparent ? 'text-stone-50' : 'text-foreground',
              )}
              onClick={() => setOpen((v) => !v)}
              aria-expanded={open}
              aria-controls={menuId}
              aria-label={open ? 'Close menu' : 'Open menu'}
            >
              {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </Container>

      <AnimatePresence>
        {open && (
          <motion.div
            id={menuId}
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 top-16 z-40 bg-background sm:top-[4.5rem] lg:hidden"
          >
            <Container className="flex h-[calc(100svh-4rem)] flex-col py-8 sm:h-[calc(100svh-4.5rem)]">
              <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
                {NAV_LINKS.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    onClick={() => setOpen(false)}
                    className={cn(
                      'rounded-sm px-2 py-3.5 font-display text-2xl transition-colors',
                      pathname === link.href ? 'text-foreground' : 'text-muted-foreground',
                    )}
                    aria-current={pathname === link.href ? 'page' : undefined}
                  >
                    {link.label}
                  </Link>
                ))}
                <Link
                  href={TRANSFORM_HREF}
                  onClick={() => setOpen(false)}
                  className={cn(
                    'rounded-sm px-2 py-3.5 font-display text-2xl transition-colors',
                    pathname === TRANSFORM_HREF ? 'text-foreground' : 'text-muted-foreground',
                  )}
                >
                  Transform
                </Link>
              </nav>

              <div className="mt-auto flex flex-col gap-4 border-t border-border pt-6">
                <AccountMenuLinks onNavigate={() => setOpen(false)} />
                <Button variant="default" size="lg" className="rounded-full" asChild>
                  <Link href={CONSULTATION_HREF} onClick={() => setOpen(false)}>
                    Request a Consultation
                  </Link>
                </Button>
              </div>
            </Container>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}

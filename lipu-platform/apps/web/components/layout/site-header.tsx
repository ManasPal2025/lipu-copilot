'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Menu, X } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

import { Navigation } from '@/components/layout/navigation';
import { CitySelector } from '@/components/layout/city-selector';
import { ThemeToggle } from '@/components/layout/theme-toggle';
import { Container } from '@/components/layout/section';
import { Button } from '@/components/ui/button';
import { SITE_NAME } from '@/lib/constants';
import { cn } from '@/lib/utils';

export function SiteHeader() {
  const pathname = usePathname();
  const isHome = pathname === '/';
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  const transparent = isHome && !scrolled;

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 48);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open, pathname]);

  return (
    <header
      className={cn(
        'fixed inset-x-0 top-0 z-50 transition-all duration-500',
        transparent
          ? 'bg-transparent'
          : 'border-b border-border/60 bg-background/95 backdrop-blur-md',
      )}
    >
      <Container>
        <div className="flex h-16 items-center justify-between sm:h-20">
          <Link href="/" className="group flex flex-col" aria-label={`${SITE_NAME} home`}>
            <span
              className={cn(
                'font-display text-xl tracking-[0.25em] sm:text-2xl',
                transparent ? 'text-stone-50' : 'text-foreground',
              )}
            >
              {SITE_NAME}
            </span>
            <span
              className={cn(
                'hidden text-[10px] uppercase tracking-[0.3em] sm:block',
                transparent ? 'text-stone-400' : 'text-muted-foreground',
              )}
            >
              Transformation
            </span>
          </Link>

          <Navigation
            className="hidden lg:flex"
            inactiveClassName={transparent ? 'text-stone-300 hover:text-stone-50' : 'text-muted-foreground'}
            activeClassName={transparent ? 'text-stone-50' : 'text-foreground'}
          />

          <div className="hidden items-center gap-2 lg:flex">
            <CitySelector inverted={transparent} />
            <ThemeToggle inverted={transparent} />
            <Button
              variant="ghost"
              size="sm"
              className={transparent ? 'text-stone-200 hover:bg-white/10 hover:text-white' : ''}
              asChild
            >
              <Link href="/contact">Consultation</Link>
            </Button>
            <Button variant="accent" size="sm" asChild>
              <Link href="/contact#quote">Begin transformation</Link>
            </Button>
          </div>

          <div className="flex items-center gap-1 lg:hidden">
            <CitySelector inverted={transparent} />
            <ThemeToggle inverted={transparent} />
            <button
              type="button"
              className={cn(
                'inline-flex items-center justify-center rounded-sm p-2',
                transparent ? 'text-stone-50' : 'text-foreground',
              )}
              onClick={() => setOpen((v) => !v)}
              aria-expanded={open}
              aria-controls="mobile-nav"
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
            id="mobile-nav"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 top-16 z-40 bg-background lg:hidden"
          >
            <Container className="flex h-[calc(100vh-4rem)] flex-col py-6">
              <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
                {[
                  { href: '/projects', label: 'Projects' },
                  { href: '/gallery', label: 'Design Ideas' },
                  { href: '/products', label: 'Products' },
                  { href: '/about', label: 'About' },
                  { href: '/contact', label: 'Contact' },
                ].map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={cn(
                      'rounded-sm px-3 py-4 font-display text-2xl',
                      pathname === link.href ? 'text-foreground' : 'text-muted-foreground',
                    )}
                  >
                    {link.label}
                  </Link>
                ))}
              </nav>
              <div className="mt-auto flex flex-col gap-3 border-t border-border pt-6">
                <CitySelector className="w-full max-w-none [&_select]:max-w-none" />
                <Button variant="accent" size="lg" asChild>
                  <Link href="/contact#quote">Begin transformation</Link>
                </Button>
                <Button variant="outline" size="lg" asChild>
                  <Link href="/contact">Book consultation</Link>
                </Button>
              </div>
            </Container>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}

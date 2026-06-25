import Link from 'next/link';

import { Container } from '@/components/layout/section';
import { Separator } from '@/components/ui/separator';
import { NAV_LINKS, SITE_NAME, SITE_TAGLINE } from '@/lib/constants';

export function SiteFooter() {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-stone-925 text-stone-300" role="contentinfo">
      <Container className="py-16 lg:py-20">
        <div className="grid gap-12 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="font-display text-2xl tracking-[0.2em] text-stone-50">{SITE_NAME}</p>
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-stone-400">{SITE_TAGLINE}</p>
            <p className="mt-6 text-sm text-stone-500">
              Premium UPVC windows &amp; doors.
              <br />
              Crafted for transformation, not transaction.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:col-span-7">
            <div>
              <p className="mb-4 text-xs font-medium uppercase tracking-[0.2em] text-stone-500">Explore</p>
              <ul className="space-y-3">
                {NAV_LINKS.map((link) => (
                  <li key={link.href}>
                    <Link href={link.href} className="text-sm text-stone-400 transition-colors hover:text-stone-50">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="mb-4 text-xs font-medium uppercase tracking-[0.2em] text-stone-500">Experience</p>
              <ul className="space-y-3 text-sm text-stone-400">
                <li>
                  <Link href="/#visualizer" className="transition-colors hover:text-stone-50">
                    AI Home Visualizer
                  </Link>
                </li>
                <li>
                  <Link href="/support" className="transition-colors hover:text-stone-50">
                    Customer support
                  </Link>
                </li>
                <li>
                  <Link href="/contact#quote" className="transition-colors hover:text-stone-50">
                    Request a quote
                  </Link>
                </li>
                <li>
                  <Link href="/projects" className="transition-colors hover:text-stone-50">
                    Case studies
                  </Link>
                </li>
              </ul>
            </div>
            <div className="col-span-2 sm:col-span-1">
              <p className="mb-4 text-xs font-medium uppercase tracking-[0.2em] text-stone-500">Contact</p>
              <ul className="space-y-3 text-sm text-stone-400">
                <li>hello@lipu.com</li>
                <li>+91 98765 43210</li>
                <li>Mumbai · Pune · Goa</li>
              </ul>
            </div>
          </div>
        </div>

        <Separator className="my-10 bg-stone-800" />

        <div className="flex flex-col gap-4 text-xs text-stone-500 sm:flex-row sm:items-center sm:justify-between">
          <p>© {year} {SITE_NAME}. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="/about" className="hover:text-stone-300">
              Privacy
            </Link>
            <Link href="/about" className="hover:text-stone-300">
              Terms
            </Link>
          </div>
        </div>
      </Container>
    </footer>
  );
}

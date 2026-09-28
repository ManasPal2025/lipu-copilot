import Image from 'next/image';
import Link from 'next/link';

import { Container } from '@/components/layout/section';
import {
  CONSULTATION_HREF,
  NAV_LINKS,
  SITE_LOGO,
  SITE_NAME,
  SITE_TAGLINE,
  TRANSFORM_HREF,
} from '@/lib/constants';

export function SiteFooter() {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-stone-925 text-stone-300" role="contentinfo">
      <Container className="py-14 lg:py-16">
        <div className="flex flex-col gap-12 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-sm">
            <Link href="/" className="inline-block" aria-label={`${SITE_NAME} home`}>
              <Image
                src={SITE_LOGO.src}
                alt={SITE_LOGO.alt}
                width={168}
                height={50}
                className="h-10 w-auto object-contain"
              />
            </Link>
            <p className="mt-5 text-sm leading-relaxed text-stone-400">{SITE_TAGLINE}</p>
            <p className="mt-3 text-sm text-stone-500">
              Premium UPVC windows and doors for homes and projects across Odisha.
            </p>
          </div>

          <nav aria-label="Footer navigation">
            <ul className="flex flex-wrap gap-x-8 gap-y-3">
              {NAV_LINKS.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-stone-400 transition-colors hover:text-stone-50"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
              <li>
                <Link
                  href={TRANSFORM_HREF}
                  className="text-sm text-stone-400 transition-colors hover:text-stone-50"
                >
                  Transform
                </Link>
              </li>
              <li>
                <Link
                  href={CONSULTATION_HREF}
                  className="text-sm text-stone-400 transition-colors hover:text-stone-50"
                >
                  Request a Consultation
                </Link>
              </li>
            </ul>
          </nav>
        </div>

        <div className="mt-12 flex flex-col gap-3 border-t border-stone-800 pt-8 text-xs text-stone-500 sm:flex-row sm:items-center sm:justify-between">
          <p>© {year} {SITE_NAME}. All rights reserved.</p>
          <p>Designed and developed by Manas Ranjan Pal, VayuLabs Inc.</p>
        </div>
      </Container>
    </footer>
  );
}

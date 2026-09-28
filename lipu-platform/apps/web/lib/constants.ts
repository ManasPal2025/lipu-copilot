export const SITE_NAME = 'Ecotech Window Systems';
export const SITE_SHORT_NAME = 'Ecotech';
export const SITE_TAGLINE = 'Beyond frames';
export const SITE_DESCRIPTION =
  'Premium UPVC windows and doors for architectural spaces across Odisha. From openings to extraordinary living environments.';

/** Primary marketing navigation (center of header). */
export const NAV_LINKS = [
  { href: '/', label: 'Home' },
  { href: '/services', label: 'Services' },
  { href: '/products', label: 'Products' },
  { href: '/inspiration', label: 'Inspiration' },
  { href: '/contact', label: 'Contact' },
] as const;

/** Existing Transform experience — redesign deferred. */
export const TRANSFORM_HREF = '/wizard';

/** Existing consultation form target. */
export const CONSULTATION_HREF = '/contact#quote';

/** Profile entry point. */
export const PROFILE_HREF = '/profile';

export const SIGN_IN_HREF = '/sign-in';
export const SIGN_UP_HREF = '/sign-up';

export const SITE_LOGO = {
  src: '/images/brand/ecotech-logo.jpeg',
  alt: 'Ecotech Window Systems',
} as const;

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export const SITE_NAME = 'LIPU';
export const SITE_TAGLINE = 'Home transformation, reimagined';
export const SITE_DESCRIPTION =
  'Premium UPVC windows and doors crafted for architectural transformation. Experience your home before you build it.';

export const NAV_LINKS = [
  { href: '/projects', label: 'Projects' },
  { href: '/gallery', label: 'Design Ideas' },
  { href: '/products', label: 'Products' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
] as const;

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

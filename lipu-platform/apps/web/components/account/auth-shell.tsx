import Image from 'next/image';
import Link from 'next/link';

import { SITE_NAME } from '@/lib/constants';
import { images } from '@/lib/images';

export function AuthShell({
  headline,
  supporting,
  children,
}: {
  headline: string;
  supporting: string;
  children: React.ReactNode;
}) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="relative h-64 sm:h-96 lg:h-auto">
        <Image
          src={images.ecotechContact.hero.src}
          alt={images.ecotechContact.hero.alt}
          fill
          priority
          sizes="(min-width: 1024px) 50vw, 100vw"
          className="object-cover"
        />
      </div>
      <div className="flex flex-col justify-center px-6 py-12 sm:px-12 lg:px-16">
        <Link href="/" className="text-xs uppercase tracking-[0.22em] text-muted-foreground">
          {SITE_NAME}
        </Link>
        <h1 className="mt-8 max-w-md font-display text-4xl sm:text-5xl">{headline}</h1>
        <p className="mt-4 max-w-md text-muted-foreground">{supporting}</p>
        <div className="mt-10 w-full max-w-md border border-border/70 bg-background/75 p-6 backdrop-blur-md sm:p-8">
          {children}
        </div>
      </div>
    </div>
  );
}

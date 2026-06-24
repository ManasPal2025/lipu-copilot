import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Container } from '@/components/layout/section';

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-5">
      <Container size="narrow" className="text-center">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">404</p>
        <h1 className="mt-4 font-display text-4xl sm:text-5xl">Page not found</h1>
        <p className="mt-4 text-muted-foreground">
          The page you are looking for does not exist — but transformation might.
        </p>
        <Button variant="accent" className="mt-8" asChild>
          <Link href="/">Return home</Link>
        </Button>
      </Container>
    </div>
  );
}

import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';
import type { NextFetchEvent, NextRequest } from 'next/server';

const isProfile = createRouteMatcher(['/profile(.*)']);

function clerkReady(): boolean {
  const publishable = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? '';
  const secret = process.env.CLERK_SECRET_KEY ?? '';
  return (
    publishable.startsWith('pk_') &&
    !publishable.includes('YOUR') &&
    secret.startsWith('sk_') &&
    !secret.includes('YOUR')
  );
}

const handleClerk = clerkMiddleware(async (auth, request) => {
  if (isProfile(request)) {
    await auth.protect();
  }
});

export default function middleware(request: NextRequest, event: NextFetchEvent) {
  if (!clerkReady()) {
    return NextResponse.next();
  }
  return handleClerk(request, event);
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};

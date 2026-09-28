import type { Metadata } from 'next';
import { SignIn } from '@clerk/nextjs';
import Link from 'next/link';

import { AuthShell } from '@/components/account/auth-shell';
import { CONSULTATION_HREF, SIGN_UP_HREF } from '@/lib/constants';
import { isClerkConfigured } from '@/lib/clerk';

export const metadata: Metadata = {
  title: 'Sign in',
  description: 'Sign in to your Ecotech account.',
};

export default function SignInPage() {
  return (
    <AuthShell headline="Welcome back" supporting="Continue your Ecotech journey.">
      {isClerkConfigured() ? (
        <SignIn
          routing="path"
          path="/sign-in"
          signUpUrl={SIGN_UP_HREF}
          forceRedirectUrl="/profile"
          fallbackRedirectUrl="/profile"
        />
      ) : (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Sign-in is not available until the Clerk publishable key is configured for this environment.
          </p>
          <Link href={CONSULTATION_HREF} className="inline-block text-sm tracking-wide">
            Request a consultation
          </Link>
        </div>
      )}
    </AuthShell>
  );
}

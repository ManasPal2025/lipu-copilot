import type { Metadata } from 'next';
import { SignUp } from '@clerk/nextjs';
import Link from 'next/link';

import { AuthShell } from '@/components/account/auth-shell';
import { CONSULTATION_HREF, SIGN_IN_HREF } from '@/lib/constants';
import { isClerkConfigured } from '@/lib/clerk';

export const metadata: Metadata = {
  title: 'Create account',
  description: 'Create your Ecotech account.',
};

export default function SignUpPage() {
  return (
    <AuthShell
      headline="Create your Ecotech account"
      supporting="Save your projects, consultations and transformations in one place."
    >
      {isClerkConfigured() ? (
        <SignUp
          routing="path"
          path="/sign-up"
          signInUrl={SIGN_IN_HREF}
          forceRedirectUrl="/profile"
          fallbackRedirectUrl="/profile"
        />
      ) : (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Account creation is not available until the Clerk publishable key is configured for this environment.
          </p>
          <Link href={CONSULTATION_HREF} className="inline-block text-sm tracking-wide">
            Request a consultation
          </Link>
        </div>
      )}
    </AuthShell>
  );
}

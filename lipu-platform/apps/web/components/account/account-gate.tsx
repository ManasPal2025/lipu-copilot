'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

import { Container, Section } from '@/components/layout/section';
import { useAccount } from '@/components/providers/account-provider';
import { SIGN_IN_HREF } from '@/lib/constants';

export function AccountGate({ children }: { children: React.ReactNode }) {
  const account = useAccount();
  const router = useRouter();

  useEffect(() => {
    if (account.status === 'guest') {
      router.replace(SIGN_IN_HREF);
    }
  }, [account.status, router]);

  if (account.status !== 'authenticated') {
    return (
      <Section className="pt-28 sm:pt-32">
        <Container size="narrow">
          <p className="text-sm text-muted-foreground">Loading your account</p>
        </Container>
      </Section>
    );
  }

  return children;
}

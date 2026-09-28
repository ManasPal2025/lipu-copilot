import type { Metadata } from 'next';

import { AccountGate } from '@/components/account/account-gate';
import { TransformationHistory } from '@/components/account/transformation-history';

export const metadata: Metadata = {
  title: 'Transformations',
  description: 'Your Ecotech transformations.',
};

export default function TransformationsPage() {
  return (
    <AccountGate>
      <TransformationHistory />
    </AccountGate>
  );
}

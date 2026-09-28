import type { Metadata } from 'next';

import { AccountGate } from '@/components/account/account-gate';
import { ConsultationHistory } from '@/components/account/consultation-history';

export const metadata: Metadata = {
  title: 'Consultations',
  description: 'Your Ecotech consultation history.',
};

export default function ConsultationsPage() {
  return (
    <AccountGate>
      <ConsultationHistory />
    </AccountGate>
  );
}

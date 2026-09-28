import type { Metadata } from 'next';

import { AccountGate } from '@/components/account/account-gate';
import { ProfileScreen } from '@/components/account/profile-screen';

export const metadata: Metadata = {
  title: 'Profile',
  description: 'Your Ecotech account.',
};

export default function ProfilePage() {
  return (
    <AccountGate>
      <ProfileScreen />
    </AccountGate>
  );
}

import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';

import { AccountGate } from '@/components/account/account-gate';
import { AccountStateProvider, type AccountValue } from '@/components/providers/account-provider';

const replace = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({ replace }),
}));

const guest: AccountValue = {
  status: 'guest',
  user: null,
  getToken: async () => null,
  signOut: async () => undefined,
};

describe('AccountGate', () => {
  beforeEach(() => {
    replace.mockClear();
  });

  it('sends a guest to sign-in', async () => {
    render(
      <AccountStateProvider value={guest}>
        <AccountGate>
          <p>Private profile</p>
        </AccountGate>
      </AccountStateProvider>,
    );

    expect(screen.queryByText(/private profile/i)).not.toBeInTheDocument();
    await waitFor(() => expect(replace).toHaveBeenCalledWith('/sign-in'));
  });
});

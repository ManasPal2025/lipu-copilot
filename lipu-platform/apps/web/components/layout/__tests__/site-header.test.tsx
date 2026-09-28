import '@testing-library/jest-dom';
import { fireEvent, render, screen } from '@testing-library/react';

import { SiteHeader } from '@/components/layout/site-header';
import { AccountStateProvider, type AccountValue } from '@/components/providers/account-provider';

jest.mock('next/navigation', () => ({
  usePathname: () => '/services',
  useRouter: () => ({ replace: jest.fn(), push: jest.fn() }),
}));

jest.mock('next/image', () => ({
  __esModule: true,
  default: ({ alt }: { alt: string }) => <span role="img" aria-label={alt} />,
}));

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ children, href, ...props }: { children: React.ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

const guest: AccountValue = {
  status: 'guest',
  user: null,
  getToken: async () => null,
  signOut: async () => undefined,
};

function signedIn(signOut: () => Promise<void>): AccountValue {
  return {
    status: 'authenticated',
    user: {
      firstName: 'Asha',
      lastName: 'Rao',
      email: 'asha@example.com',
      phone: null,
      imageUrl: null,
    },
    getToken: async () => 'session-token',
    signOut,
  };
}

describe('SiteHeader authentication', () => {
  it('shows the guest sign-in entry', () => {
    render(
      <AccountStateProvider value={guest}>
        <SiteHeader />
      </AccountStateProvider>,
    );

    expect(screen.getAllByRole('link', { name: /sign in/i }).length).toBeGreaterThan(0);
    expect(screen.getByRole('link', { name: /transform/i })).toBeInTheDocument();
    expect(screen.getAllByRole('link', { name: /request a consultation/i }).length).toBeGreaterThan(0);
    expect(screen.queryByRole('menu')).not.toBeInTheDocument();
  });

  it('opens the account menu for a signed-in visitor', () => {
    render(
      <AccountStateProvider value={signedIn(async () => undefined)}>
        <SiteHeader />
      </AccountStateProvider>,
    );

    fireEvent.click(screen.getAllByRole('button', { name: /account menu/i })[0]);
    expect(screen.getByRole('menuitem', { name: /my profile/i })).toHaveAttribute('href', '/profile');
    expect(screen.getByRole('menuitem', { name: /my consultations/i })).toHaveAttribute(
      'href',
      '/profile/consultations',
    );
    expect(screen.getByRole('menuitem', { name: /my transformations/i })).toHaveAttribute(
      'href',
      '/profile/transformations',
    );
  });

  it('signs out through the account menu', () => {
    const signOut = jest.fn(async () => undefined);
    render(
      <AccountStateProvider value={signedIn(signOut)}>
        <SiteHeader />
      </AccountStateProvider>,
    );

    fireEvent.click(screen.getAllByRole('button', { name: /account menu/i })[0]);
    fireEvent.click(screen.getByRole('menuitem', { name: /sign out/i }));
    expect(signOut).toHaveBeenCalledTimes(1);
  });
});

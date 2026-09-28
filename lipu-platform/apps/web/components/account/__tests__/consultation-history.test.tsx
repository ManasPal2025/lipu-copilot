import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { ConsultationHistory } from '@/components/account/consultation-history';
import { AccountStateProvider, type AccountValue } from '@/components/providers/account-provider';

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ children, href, ...props }: { children: React.ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

const account: AccountValue = {
  status: 'authenticated',
  user: {
    firstName: 'Asha',
    lastName: 'Rao',
    email: 'asha@example.com',
    phone: null,
    imageUrl: null,
  },
  getToken: async () => 'session-token',
  signOut: async () => undefined,
};

const mine = {
  id: '11111111-1111-1111-1111-111111111111',
  created_at: '2026-09-23T10:30:00Z',
  project_type: 'RESIDENTIAL',
  city: 'Bhubaneswar',
  status: 'NEW',
  message: 'We want larger openings in the living room.',
};

const contacted = {
  id: '22222222-2222-2222-2222-222222222222',
  created_at: '2026-09-12T10:30:00Z',
  project_type: 'COMMERCIAL',
  city: 'Cuttack',
  status: 'CONTACTED',
  message: 'A'.repeat(220),
};

function renderHistory() {
  return render(
    <AccountStateProvider value={account}>
      <ConsultationHistory />
    </AccountStateProvider>,
  );
}

describe('ConsultationHistory', () => {
  const originalFetch = global.fetch;

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('renders the signed-in customer consultations', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ items: [mine], page: 1, page_size: 10, total: 1, has_next: false }),
    });

    renderHistory();

    expect(await screen.findByRole('heading', { name: 'Residential' })).toBeInTheDocument();
    expect(screen.getByText('Bhubaneswar')).toBeInTheDocument();
    expect(screen.getByText('New')).toBeInTheDocument();
    expect(screen.getByText(mine.message)).toBeInTheDocument();
    expect(screen.getByText(/2026/)).toBeInTheDocument();
    expect(screen.queryByText(/2026-09-23T/)).not.toBeInTheDocument();
    const url = String((global.fetch as jest.Mock).mock.calls[0][0]);
    expect(url).toContain('/consultations/me');
    expect(url).not.toContain('user_id');
  });

  it('shows an empty state with a consultation link', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ items: [], page: 1, page_size: 10, total: 0, has_next: false }),
    });

    renderHistory();

    expect(await screen.findByText('No consultations yet')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /request a consultation/i })).toHaveAttribute('href', '/contact#quote');
    expect(screen.getByRole('link', { name: /explore inspiration/i })).toHaveAttribute('href', '/inspiration');
  });

  it('shows a loading state before the history arrives', async () => {
    let resolveFetch: (value: { ok: boolean; json: () => Promise<unknown> }) => void = () => undefined;
    global.fetch = jest.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        }),
    );

    renderHistory();

    expect(await screen.findByText(/loading your consultations/i)).toBeInTheDocument();
    resolveFetch({
      ok: true,
      json: async () => ({ items: [], page: 1, page_size: 10, total: 0, has_next: false }),
    });
    await waitFor(() => expect(screen.getByText('No consultations yet')).toBeInTheDocument());
  });

  it('shows a readable error and can try again', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ error: { message: 'database relation missing' } }),
    });

    renderHistory();

    expect(await screen.findByText(/couldn't load your consultations/i)).toBeInTheDocument();
    expect(screen.getByText(/please try again/i)).toBeInTheDocument();
    expect(screen.queryByText(/database relation/i)).not.toBeInTheDocument();

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ items: [mine], page: 1, page_size: 10, total: 1, has_next: false }),
    });
    fireEvent.click(screen.getByRole('button', { name: /try again/i }));
    expect(await screen.findByRole('heading', { name: 'Residential' })).toBeInTheDocument();
  });

  it('labels status and project type and reveals the full message', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ items: [contacted], page: 1, page_size: 10, total: 1, has_next: false }),
    });

    renderHistory();

    expect(await screen.findByRole('heading', { name: 'Commercial' })).toBeInTheDocument();
    expect(screen.getByText('Contacted')).toBeInTheDocument();
    expect(screen.queryByText(contacted.message)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /read more/i }));
    expect(screen.getByText(contacted.message)).toBeInTheDocument();
  });

  it('renders only the consultations returned for this account', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ items: [mine], page: 1, page_size: 10, total: 1, has_next: false }),
    });

    renderHistory();

    expect(await screen.findByText(mine.message)).toBeInTheDocument();
    expect(screen.queryByText(/showroom glazing for another account/i)).not.toBeInTheDocument();
  });
});

import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { TransformationHistory } from '@/components/account/transformation-history';
import { AccountStateProvider, type AccountValue } from '@/components/providers/account-provider';

jest.mock('next/image', () => ({
  __esModule: true,
  default: ({ alt, src }: { alt: string; src: string }) => <span role="img" aria-label={alt} data-src={src} />,
}));

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

const completed = {
  id: '11111111-1111-1111-1111-111111111111',
  created_at: '2026-09-23T10:30:00Z',
  target: 'WINDOWS',
  variant: 'SLIDING',
  status: 'COMPLETED',
  source_asset: {
    id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    mime_type: 'image/png',
    public_url: '/images/transform/ecotech/transform-sample-living-01.png',
  },
  result: {
    id: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    created_at: '2026-09-23T10:40:00Z',
    asset: {
      id: 'cccccccc-cccc-cccc-cccc-cccccccccccc',
      mime_type: 'image/png',
      public_url: '/images/transform/ecotech/transform-sample-balcony-01.png',
    },
  },
};

const configured = {
  id: '22222222-2222-2222-2222-222222222222',
  created_at: '2026-09-12T10:30:00Z',
  target: 'DOORS',
  variant: 'BIFOLD',
  status: 'CONFIGURED',
  source_asset: null,
  result: null,
};

const uploaded = {
  id: '33333333-3333-3333-3333-333333333333',
  created_at: '2026-09-01T10:30:00Z',
  target: 'TERRACE',
  variant: 'LARGE_OPENING',
  status: 'UPLOADED',
  source_asset: {
    id: 'dddddddd-dddd-dddd-dddd-dddddddddddd',
    mime_type: 'image/png',
    public_url: null,
  },
  result: {
    id: 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
    created_at: '2026-09-01T10:40:00Z',
    asset: {
      id: 'ffffffff-ffff-ffff-ffff-ffffffffffff',
      mime_type: 'image/png',
      public_url: 'private/secret-object-key',
    },
  },
};

function page(items: unknown[], hasNext = false, pageNumber = 1, total = items.length) {
  return { items, page: pageNumber, page_size: 10, total, has_next: hasNext };
}

function renderHistory() {
  return render(
    <AccountStateProvider value={account}>
      <TransformationHistory />
    </AccountStateProvider>,
  );
}

describe('TransformationHistory', () => {
  const originalFetch = global.fetch;

  afterEach(() => {
    global.fetch = originalFetch;
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

    expect(await screen.findByText(/loading your transformations/i)).toBeInTheDocument();
    resolveFetch({ ok: true, json: async () => page([]) });
    await waitFor(() => expect(screen.getByText('No transformations yet')).toBeInTheDocument());
  });

  it('shows an empty state with transform and inspiration links', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: true, json: async () => page([]) });

    renderHistory();

    expect(await screen.findByText('No transformations yet')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /transform your space/i })).toHaveAttribute('href', '/wizard');
    expect(screen.getByRole('link', { name: /explore inspiration/i })).toHaveAttribute('href', '/inspiration');
  });

  it('renders several transformations with readable labels and a result image', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => page([completed, configured]),
    });

    renderHistory();

    expect(await screen.findByRole('heading', { name: 'Windows' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Doors' })).toBeInTheDocument();
    expect(screen.getByText('Sliding')).toBeInTheDocument();
    expect(screen.getByText('Bifold')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
    expect(screen.getByText('Configured')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Your space' })).toHaveAttribute(
      'data-src',
      completed.source_asset.public_url,
    );
    expect(screen.getByRole('img', { name: 'Ecotech possibility' })).toHaveAttribute(
      'data-src',
      completed.result.asset.public_url,
    );
    expect(screen.getAllByText(/a visual record is not available/i)).toHaveLength(1);
    expect(screen.getAllByText(/2026/)).toHaveLength(2);
    expect(screen.queryByText(/2026-09-23T/)).not.toBeInTheDocument();
    const url = String((global.fetch as jest.Mock).mock.calls[0][0]);
    expect(url).toContain('/transform/requests/me');
    expect(url).not.toContain('user_id');
  });

  it('does not render an image when no safe public url exists', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => page([uploaded]),
    });

    renderHistory();

    expect(await screen.findByRole('heading', { name: 'Terrace' })).toBeInTheDocument();
    expect(screen.getByText('Large Opening')).toBeInTheDocument();
    expect(screen.getByText('Uploaded')).toBeInTheDocument();
    expect(screen.queryByRole('img')).not.toBeInTheDocument();
    expect(screen.getByText(/a visual record is not available/i)).toBeInTheDocument();
    expect(screen.queryByText(/secret-object-key/i)).not.toBeInTheDocument();
  });

  it('renders a signed source url for the customer image', async () => {
    const signed = 'https://storage.example/signed/token?expires=900';
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () =>
        page([
          {
            ...uploaded,
            source_asset: { ...uploaded.source_asset, public_url: signed },
            result: null,
          },
        ]),
    });

    renderHistory();

    expect(await screen.findByRole('img', { name: 'Your space' })).toHaveAttribute('src', signed);
    expect(screen.queryByRole('img', { name: 'Ecotech possibility' })).not.toBeInTheDocument();
  });

  it('shows processing and a failed retry that reuses the request', async () => {
    const failed = {
      ...uploaded,
      id: '44444444-4444-4444-4444-444444444444',
      status: 'FAILED',
      source_asset: {
        ...uploaded.source_asset,
        public_url: 'https://storage.example/signed/source',
      },
      result: null,
    };
    const processing = { ...configured, id: '55555555-5555-5555-5555-555555555555', status: 'PROCESSING' };
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => page([processing, failed]),
    });

    renderHistory();

    expect(await screen.findByText(/your visualization is being prepared/i)).toBeInTheDocument();
    expect(screen.getByText(/your original image is safe/i)).toBeInTheDocument();
    expect(screen.queryByText(/openai/i)).not.toBeInTheDocument();

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        status: 'COMPLETED',
        result: {
          id: 'result-asset',
          mime_type: 'image/png',
          public_url: 'https://storage.example/signed/result',
        },
      }),
    });
    fireEvent.click(screen.getByRole('button', { name: /try again/i }));

    expect(await screen.findByRole('img', { name: 'Ecotech possibility' })).toHaveAttribute(
      'src',
      'https://storage.example/signed/result',
    );
    const retryCall = (global.fetch as jest.Mock).mock.calls.at(-1);
    expect(String(retryCall?.[0])).toContain(`/transform/requests/${failed.id}/generate`);
    expect(retryCall?.[1].method).toBe('POST');
  });

  it('labels the remaining targets and statuses', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () =>
        page([
          { ...configured, id: '1', target: 'BALCONY', variant: 'CASEMENT', status: 'PROCESSING' },
          { ...configured, id: '2', target: 'OUTDOOR', variant: 'FRENCH', status: 'FAILED' },
        ]),
    });

    renderHistory();

    expect(await screen.findByRole('heading', { name: 'Balcony' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Outdoor' })).toBeInTheDocument();
    expect(screen.getByText('Casement')).toBeInTheDocument();
    expect(screen.getByText('French')).toBeInTheDocument();
    expect(screen.getByText('Processing')).toBeInTheDocument();
    expect(screen.getByText('Failed')).toBeInTheDocument();
  });

  it('shows a readable error and can try again', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ error: { message: 'database relation missing' } }),
    });

    renderHistory();

    expect(await screen.findByText(/couldn't load your transformations/i)).toBeInTheDocument();
    expect(screen.getByText(/please try again/i)).toBeInTheDocument();
    expect(screen.queryByText(/database relation/i)).not.toBeInTheDocument();

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => page([completed]),
    });
    fireEvent.click(screen.getByRole('button', { name: /try again/i }));
    expect(await screen.findByRole('heading', { name: 'Windows' })).toBeInTheDocument();
  });

  it('appends the next page without replacing the first', async () => {
    global.fetch = jest.fn().mockImplementation((input: string) => {
      const url = String(input);
      if (url.includes('page=2')) {
        return Promise.resolve({ ok: true, json: async () => page([configured], false, 2, 2) });
      }
      return Promise.resolve({ ok: true, json: async () => page([completed], true, 1, 2) });
    });

    renderHistory();

    expect(await screen.findByRole('heading', { name: 'Windows' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /load more/i }));
    expect(await screen.findByRole('heading', { name: 'Doors' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Windows' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /load more/i })).not.toBeInTheDocument();
  });
});

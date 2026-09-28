import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { TransformWorkspace } from '@/components/marketing/transform-workspace';
import { AccountStateProvider, type AccountValue } from '@/components/providers/account-provider';

jest.mock('next/image', () => ({
  __esModule: true,
  default: ({ alt }: { alt: string }) => <span role="img" aria-label={alt} />,
}));

const signedIn: AccountValue = {
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

function renderWorkspace(account?: AccountValue) {
  if (!account) return render(<TransformWorkspace />);
  return render(
    <AccountStateProvider value={account}>
      <TransformWorkspace />
    </AccountStateProvider>,
  );
}

function chooseSample() {
  fireEvent.click(screen.getByText('Living'));
  fireEvent.click(screen.getByRole('button', { name: 'Windows' }));
  fireEvent.click(screen.getByRole('button', { name: 'Sliding' }));
  fireEvent.click(screen.getByRole('button', { name: /visualize my space/i }));
}

function postedBody(): Record<string, unknown> {
  const init = (global.fetch as jest.Mock).mock.calls[0][1] as { body: string; method: string };
  expect(init.method).toBe('POST');
  return JSON.parse(init.body) as Record<string, unknown>;
}

describe('TransformWorkspace persistence', () => {
  const originalFetch = global.fetch;

  beforeAll(() => {
    URL.createObjectURL = jest.fn(() => 'blob:preview');
    URL.revokeObjectURL = jest.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('lets a guest run the demonstration without saving', async () => {
    global.fetch = jest.fn();
    renderWorkspace();
    chooseSample();

    expect(
      await screen.findByRole('heading', { name: /your space, then a possibility/i }, { timeout: 3000 }),
    ).toBeInTheDocument();
    expect(screen.getByText(/not a generated result/i)).toBeInTheDocument();
    expect(global.fetch).not.toHaveBeenCalled();
    expect(screen.queryByRole('link', { name: /sign in/i })).not.toBeInTheDocument();
  });

  it('saves a signed-in sample before showing the demonstration', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: true, json: async () => ({ id: 'saved' }) });
    renderWorkspace(signedIn);
    chooseSample();

    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
    const url = String((global.fetch as jest.Mock).mock.calls[0][0]);
    expect(url).toContain('/transform/requests');
    expect(url).not.toContain('/me');
    const body = postedBody();
    expect(body.target).toBe('WINDOWS');
    expect(body.variant).toBe('SLIDING');
    expect(body).not.toHaveProperty('user_id');
    expect(body).not.toHaveProperty('status');
    expect(body.source_asset).toEqual({
      mime_type: 'image/png',
      source_kind: 'SAMPLE',
      sample_id: 'living',
    });
    expect(
      await screen.findByRole('heading', { name: /your space, then a possibility/i }, { timeout: 3000 }),
    ).toBeInTheDocument();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('saves an uploaded photo without sending a user id', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        id: 'saved-request',
        status: 'COMPLETED',
        result: {
          id: 'result',
          mime_type: 'image/png',
          public_url: 'https://storage.example/signed/result',
        },
      }),
    });
    renderWorkspace(signedIn);

    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['room'], 'room.jpg', { type: 'image/jpeg' });
    fireEvent.change(input, { target: { files: [file] } });
    expect(await screen.findByText('room.jpg')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Doors' }));
    fireEvent.click(screen.getByRole('button', { name: 'French' }));
    fireEvent.click(screen.getByRole('button', { name: /visualize my space/i }));

    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
    const init = (global.fetch as jest.Mock).mock.calls[0][1] as {
      body: FormData;
      headers: Record<string, string>;
    };
    expect(init.body).toBeInstanceOf(FormData);
    expect(init.headers['Content-Type']).toBeUndefined();
    expect(init.body.get('target')).toBe('DOORS');
    expect(init.body.get('variant')).toBe('FRENCH');
    expect(init.body.get('source_kind')).toBe('UPLOAD');
    expect(init.body.get('user_id')).toBeNull();
    expect(init.body.get('file')).toBeTruthy();
    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(3));
    const calls = (global.fetch as jest.Mock).mock.calls.map((call) => String(call[0]));
    expect(calls[1]).toContain('/configure');
    expect(calls[2]).toContain('/generate');
    expect(calls.some((url) => url.includes('user_id'))).toBe(false);
    expect(await screen.findByText('Completed')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Ecotech possibility' })).toHaveAttribute(
      'src',
      'https://storage.example/signed/result',
    );
    expect(screen.queryByText(/not a generated result/i)).not.toBeInTheDocument();
  });

  it('shows uploading and a retry when the image cannot be saved', async () => {
    let resolveFetch: (value: { ok: boolean; json: () => Promise<{ id: string }> }) => void = () => undefined;
    global.fetch = jest.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        }),
    );
    renderWorkspace(signedIn);
    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(['room'], 'room.jpg', { type: 'image/jpeg' })] },
    });
    fireEvent.click(await screen.findByRole('button', { name: 'Windows' }));
    fireEvent.click(screen.getByRole('button', { name: 'Sliding' }));
    fireEvent.click(screen.getByRole('button', { name: /visualize my space/i }));

    expect(await screen.findByText('Uploading image')).toBeInTheDocument();
    resolveFetch({ ok: false, json: async () => ({ id: 'no' }) });
    expect(await screen.findByRole('alert')).toHaveTextContent(/upload failed/i);
    expect(screen.queryByText(/traceback/i)).not.toBeInTheDocument();

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        id: 'saved-request',
        status: 'COMPLETED',
        result: {
          id: 'result',
          mime_type: 'image/png',
          public_url: 'https://storage.example/signed/result',
        },
      }),
    });
    fireEvent.click(screen.getByRole('button', { name: /retry/i }));
    expect(await screen.findByText('Completed')).toBeInTheDocument();
  });

  it('shows processing, then a safe failure, and retries the same request', async () => {
    const responses = [
      { ok: true, json: async () => ({ id: 'saved-request' }) },
      { ok: true, json: async () => ({ id: 'saved-request', status: 'CONFIGURED' }) },
      { ok: false, status: 503, json: async () => ({ error: { message: 'provider stack trace' } }) },
    ];
    global.fetch = jest.fn().mockImplementation(() => Promise.resolve(responses.shift()));
    renderWorkspace(signedIn);
    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(['room'], 'room.jpg', { type: 'image/jpeg' })] },
    });
    fireEvent.click(await screen.findByRole('button', { name: 'Windows' }));
    fireEvent.click(screen.getByRole('button', { name: 'Sliding' }));
    fireEvent.click(screen.getByRole('button', { name: /visualize my space/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent(/your original image is safe/i);
    expect(screen.queryByText(/stack trace/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/not a generated result/i)).not.toBeInTheDocument();

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        status: 'COMPLETED',
        result: { id: 'result', mime_type: 'image/png', public_url: 'https://storage.example/signed/result' },
      }),
    });
    fireEvent.click(screen.getByRole('button', { name: /retry/i }));
    expect(await screen.findByRole('img', { name: 'Ecotech possibility' })).toHaveAttribute(
      'src',
      'https://storage.example/signed/result',
    );
    const urls = (global.fetch as jest.Mock).mock.calls.map((call) => String(call[0]));
    expect(urls.filter((url) => url.endsWith('/transform/requests'))).toHaveLength(1);
    expect(urls.filter((url) => url.endsWith('/generate'))).toHaveLength(2);
  });

  it('ignores a second click while generation is in progress', async () => {
    let release: (value: { ok: boolean; json: () => Promise<unknown> }) => void = () => undefined;
    const pending = new Promise<{ ok: boolean; json: () => Promise<unknown> }>((resolve) => {
      release = resolve;
    });
    global.fetch = jest
      .fn()
      .mockResolvedValueOnce({ ok: true, json: async () => ({ id: 'saved-request' }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'CONFIGURED' }) })
      .mockImplementationOnce(() => pending);
    renderWorkspace(signedIn);
    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(['room'], 'room.jpg', { type: 'image/jpeg' })] },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Windows' }));
    fireEvent.click(screen.getByRole('button', { name: 'Sliding' }));
    const visualize = screen.getByRole('button', { name: /visualize my space/i });
    fireEvent.click(visualize);
    expect(await screen.findByText('Processing')).toBeInTheDocument();
    fireEvent.click(visualize);
    expect(global.fetch).toHaveBeenCalledTimes(3);
    release({
      ok: true,
      json: async () => ({
        status: 'COMPLETED',
        result: { id: 'result', mime_type: 'image/png', public_url: 'https://storage.example/signed/result' },
      }),
    });
    expect(await screen.findByText('Completed')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(3);
  });

  it('lets a guest upload without calling generation', async () => {
    global.fetch = jest.fn();
    renderWorkspace();
    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(['room'], 'room.jpg', { type: 'image/jpeg' })] },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Windows' }));
    fireEvent.click(screen.getByRole('button', { name: 'Sliding' }));
    fireEvent.click(screen.getByRole('button', { name: /visualize my space/i }));

    expect(
      await screen.findByRole('heading', { name: /your space, then a possibility/i }, { timeout: 3000 }),
    ).toBeInTheDocument();
    expect(screen.getByText(/not a generated result/i)).toBeInTheDocument();
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('shows a readable save error and can retry without hiding the preview', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ error: { message: 'duplicate key value' } }),
    });
    renderWorkspace(signedIn);
    chooseSample();

    expect(await screen.findByRole('alert')).toHaveTextContent(/couldn't save this transformation/i);
    expect(screen.queryByText(/duplicate key/i)).not.toBeInTheDocument();
    expect(
      await screen.findByRole('heading', { name: /your space, then a possibility/i }, { timeout: 3000 }),
    ).toBeInTheDocument();

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 'saved' }),
    });
    fireEvent.click(screen.getByRole('button', { name: /retry/i }));
    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
    expect(screen.getByRole('heading', { name: /your space, then a possibility/i })).toBeInTheDocument();
  });
});

import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { ContactForm } from '@/components/marketing/contact-form';

function fillAndSubmit() {
  fireEvent.change(screen.getByLabelText(/first name/i), { target: { value: 'Asha' } });
  fireEvent.change(screen.getByLabelText(/last name/i), { target: { value: 'Rao' } });
  fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'asha@example.com' } });
  fireEvent.change(screen.getByLabelText(/city/i), { target: { value: 'Bhubaneswar' } });
  fireEvent.change(screen.getByLabelText(/project type/i), { target: { value: 'residential' } });
  fireEvent.change(screen.getByLabelText(/tell us about your home/i), {
    target: { value: 'Larger openings in the living room.' },
  });
  const form = screen.getByRole('button', { name: /submit request/i }).closest('form');
  if (!form) {
    throw new Error('Consultation form was not rendered.');
  }
  fireEvent.submit(form);
}

describe('ContactForm consultation submit', () => {
  const originalFetch = global.fetch;

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('posts a valid request and shows the existing confirmation', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: true, json: async () => ({ success: true }) });

    render(<ContactForm />);
    fillAndSubmit();

    expect(await screen.findByRole('heading', { name: /thank you/i })).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/consultations',
      expect.objectContaining({ method: 'POST' })
    );
    const init = (global.fetch as jest.Mock).mock.calls[0][1] as { headers: Record<string, string> };
    expect(init.headers.Authorization).toBeUndefined();
  });

  it('stays available to a guest without asking them to sign in', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: true, json: async () => ({ success: true }) });

    render(<ContactForm />);

    expect(screen.getByRole('heading', { name: /request a consultation/i })).toBeInTheDocument();
    expect(screen.queryByRole('link', { name: /sign in/i })).not.toBeInTheDocument();
    fillAndSubmit();
    expect(await screen.findByRole('heading', { name: /thank you/i })).toBeInTheDocument();
  });

  it('keeps the form and shows a readable error when the request fails', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: false, status: 500 });

    render(<ContactForm />);
    fillAndSubmit();

    expect(await screen.findByRole('alert')).toHaveTextContent(/couldn't send your request/i);
    expect(screen.queryByText(/500 internal server error/i)).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit request/i })).toBeEnabled();
  });

  it('disables submit while the request is in flight', async () => {
    let resolveFetch: (value: { ok: boolean }) => void = () => undefined;
    global.fetch = jest.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        })
    );

    render(<ContactForm />);
    fillAndSubmit();

    const sending = await screen.findByRole('button', { name: /sending request/i });
    expect(sending).toBeDisabled();
    fireEvent.click(sending);
    expect(global.fetch).toHaveBeenCalledTimes(1);

    resolveFetch({ ok: true });
    await waitFor(() => expect(screen.getByRole('heading', { name: /thank you/i })).toBeInTheDocument());
  });
});

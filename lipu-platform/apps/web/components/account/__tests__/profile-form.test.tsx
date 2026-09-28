import '@testing-library/jest-dom';
import { fireEvent, render, screen } from '@testing-library/react';

import { ProfileForm, type ProfileDraft } from '@/components/account/profile-form';

const initial: ProfileDraft = {
  first_name: 'Asha',
  last_name: 'Rao',
  phone: '',
  city: 'Bhubaneswar',
  state: '',
  company: '',
  preferred_contact_method: '',
  project_interests: [],
};

describe('ProfileForm', () => {
  it('saves profile changes', async () => {
    const onSave = jest.fn(async () => undefined);
    render(<ProfileForm email="asha@example.com" initial={initial} onSave={onSave} />);

    fireEvent.change(screen.getByLabelText(/phone/i), { target: { value: '+91 98765 43210' } });
    fireEvent.click(screen.getByRole('button', { name: /save changes/i }));

    expect(await screen.findByRole('status')).toHaveTextContent(/saved/i);
    expect(onSave).toHaveBeenCalledWith(expect.objectContaining({ phone: '+91 98765 43210' }));
    expect(screen.getByLabelText(/email/i)).toBeDisabled();
  });

  it('keeps the form and shows an error when saving fails', async () => {
    const onSave = jest.fn(async () => {
      throw new Error('We could not save your profile.');
    });
    render(<ProfileForm email="asha@example.com" initial={initial} onSave={onSave} />);

    fireEvent.click(screen.getByRole('button', { name: /save changes/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent(/could not save your profile/i);
    expect(screen.getByLabelText(/first name/i)).toHaveValue('Asha');
  });
});

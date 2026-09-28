'use client';

import { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export type ProfileDraft = {
  first_name: string;
  last_name: string;
  phone: string;
  city: string;
  state: string;
  company: string;
  preferred_contact_method: '' | 'EMAIL' | 'PHONE' | 'WHATSAPP';
  project_interests: string[];
};

const INTERESTS = [
  { value: 'RESIDENTIAL', label: 'Residential' },
  { value: 'RENOVATION', label: 'Renovation' },
  { value: 'COMMERCIAL', label: 'Commercial' },
  { value: 'HOSPITALITY', label: 'Hospitality' },
  { value: 'ARCHITECTURAL', label: 'Architectural' },
  { value: 'ARCHITECT', label: 'Architect' },
  { value: 'OTHER', label: 'Other' },
] as const;

export function ProfileForm({
  email,
  initial,
  onSave,
}: {
  email: string;
  initial: ProfileDraft;
  onSave: (draft: ProfileDraft) => Promise<void>;
}) {
  const [draft, setDraft] = useState(initial);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  function update(field: keyof ProfileDraft, value: string) {
    setSaved(false);
    setDraft((current) => ({ ...current, [field]: value }));
  }

  function toggleInterest(value: string) {
    setSaved(false);
    setDraft((current) => {
      const selected = current.project_interests.includes(value)
        ? current.project_interests.filter((item) => item !== value)
        : [...current.project_interests, value];
      return { ...current, project_interests: selected };
    });
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (saving) return;
    setSaving(true);
    setError(null);
    setSaved(false);
    try {
      await onSave(draft);
      setSaved(true);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'We could not save your profile.');
    } finally {
      setSaving(false);
    }
  }

  return (
    <form id="personal-details" onSubmit={handleSubmit} className="space-y-8">
      <div className="grid gap-6 sm:grid-cols-2">
        <Field label="First name" id="profile-first-name">
          <Input
            id="profile-first-name"
            value={draft.first_name}
            autoComplete="given-name"
            onChange={(event) => update('first_name', event.target.value)}
          />
        </Field>
        <Field label="Last name" id="profile-last-name">
          <Input
            id="profile-last-name"
            value={draft.last_name}
            autoComplete="family-name"
            onChange={(event) => update('last_name', event.target.value)}
          />
        </Field>
        <Field label="Email" id="profile-email">
          <Input id="profile-email" value={email} type="email" disabled readOnly />
        </Field>
        <Field label="Phone" id="profile-phone">
          <Input
            id="profile-phone"
            value={draft.phone}
            type="tel"
            autoComplete="tel"
            onChange={(event) => update('phone', event.target.value)}
          />
        </Field>
        <Field label="City" id="profile-city">
          <Input
            id="profile-city"
            value={draft.city}
            autoComplete="address-level2"
            onChange={(event) => update('city', event.target.value)}
          />
        </Field>
        <Field label="State" id="profile-state">
          <Input
            id="profile-state"
            value={draft.state}
            autoComplete="address-level1"
            onChange={(event) => update('state', event.target.value)}
          />
        </Field>
        <Field label="Company" id="profile-company">
          <Input
            id="profile-company"
            value={draft.company}
            autoComplete="organization"
            onChange={(event) => update('company', event.target.value)}
          />
        </Field>
        <Field label="Contact preference" id="profile-contact">
          <select
            id="profile-contact"
            value={draft.preferred_contact_method}
            onChange={(event) => update('preferred_contact_method', event.target.value)}
            className="flex h-11 w-full rounded-sm border border-input bg-background px-4 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">No preference</option>
            <option value="EMAIL">Email</option>
            <option value="PHONE">Phone</option>
            <option value="WHATSAPP">WhatsApp</option>
          </select>
        </Field>
      </div>

      <fieldset>
        <legend className="text-xs font-medium uppercase tracking-wider">Interests</legend>
        <div className="mt-4 flex flex-wrap gap-x-5 gap-y-3">
          {INTERESTS.map((interest) => (
            <label key={interest.value} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={draft.project_interests.includes(interest.value)}
                onChange={() => toggleInterest(interest.value)}
              />
              {interest.label}
            </label>
          ))}
        </div>
      </fieldset>

      <div className="flex flex-wrap items-center gap-4">
        <Button type="submit" variant="accent" className="rounded-full" disabled={saving}>
          {saving ? 'Saving changes' : 'Save changes'}
        </Button>
        {saved ? (
          <p role="status" className="text-sm text-muted-foreground">
            Saved
          </p>
        ) : null}
        {error ? (
          <p role="alert" className="text-sm text-muted-foreground">
            {error}
          </p>
        ) : null}
      </div>
    </form>
  );
}

function Field({
  id,
  label,
  children,
}: {
  id: string;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label htmlFor={id} className="mb-2 block text-xs font-medium uppercase tracking-wider">
        {label}
      </label>
      {children}
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

import { ProfileForm, type ProfileDraft } from '@/components/account/profile-form';
import { Container, Section } from '@/components/layout/section';
import { useAccount } from '@/components/providers/account-provider';
import { Button } from '@/components/ui/button';
import { API_BASE_URL } from '@/lib/constants';

type Me = {
  id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  phone: string | null;
  avatar_url: string | null;
  created_at: string;
  profile: {
    city: string | null;
    state: string | null;
    company: string | null;
    preferred_contact_method: string | null;
    project_interests: string[];
  };
};

function draftFrom(me: Me): ProfileDraft {
  const method = me.profile.preferred_contact_method;
  const preference: ProfileDraft['preferred_contact_method'] =
    method === 'EMAIL' || method === 'PHONE' || method === 'WHATSAPP' ? method : '';
  return {
    first_name: me.first_name ?? '',
    last_name: me.last_name ?? '',
    phone: me.phone ?? '',
    city: me.profile.city ?? '',
    state: me.profile.state ?? '',
    company: me.profile.company ?? '',
    preferred_contact_method: preference,
    project_interests: me.profile.project_interests ?? [],
  };
}

function displayName(me: Me): string {
  const name = [me.first_name, me.last_name].filter(Boolean).join(' ');
  return name || me.email;
}

function initials(me: Me): string {
  const letters = [me.first_name, me.last_name]
    .filter((part): part is string => Boolean(part))
    .map((part) => part.slice(0, 1).toUpperCase());
  return letters.join('') || me.email.slice(0, 1).toUpperCase();
}

export function ProfileScreen() {
  const account = useAccount();
  const [me, setMe] = useState<Me | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (account.status !== 'authenticated') return;
    let cancelled = false;
    async function load() {
      const token = await account.getToken();
      const response = await fetch(`${API_BASE_URL}/users/me`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!response.ok) {
        if (!cancelled) setError('We could not load your profile.');
        return;
      }
      const body = (await response.json()) as Me;
      if (!cancelled) setMe(body);
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, [account]);

  async function save(draft: ProfileDraft) {
    const token = await account.getToken();
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({
        first_name: draft.first_name || null,
        last_name: draft.last_name || null,
        phone: draft.phone || null,
        city: draft.city || null,
        state: draft.state || null,
        company: draft.company || null,
        preferred_contact_method: draft.preferred_contact_method || null,
        project_interests: draft.project_interests,
      }),
    });
    if (!response.ok) {
      const body = (await response.json().catch(() => null)) as { error?: { message?: string } } | null;
      throw new Error(body?.error?.message || 'We could not save your profile.');
    }
    setMe((await response.json()) as Me);
  }

  if (error) {
    return (
      <Section className="pt-28 sm:pt-32">
        <Container size="narrow">
          <p role="alert" className="text-muted-foreground">
            {error}
          </p>
        </Container>
      </Section>
    );
  }

  if (!me) {
    return (
      <Section className="pt-28 sm:pt-32">
        <Container size="narrow">
          <p className="text-sm text-muted-foreground">Loading your profile</p>
        </Container>
      </Section>
    );
  }

  const created = new Intl.DateTimeFormat('en-IN', {
    month: 'long',
    year: 'numeric',
  }).format(new Date(me.created_at));
  const avatar = me.avatar_url || account.user?.imageUrl;

  return (
    <Section className="pt-28 sm:pt-32">
      <Container size="narrow" className="space-y-16">
        <header className="border-b border-border/70 pb-10">
          <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Account</p>
          <h1 className="mt-4 font-display text-4xl sm:text-5xl">Your Ecotech profile</h1>
          <div className="mt-8 flex items-center gap-5">
            <span
              className="inline-flex h-16 w-16 shrink-0 items-center justify-center rounded-full border border-border/70 bg-muted/40 bg-cover bg-center font-display text-xl"
              style={avatar ? { backgroundImage: `url(${avatar})` } : undefined}
              role="img"
              aria-label={displayName(me)}
            >
              {avatar ? <span className="sr-only">{displayName(me)}</span> : initials(me)}
            </span>
            <div>
              <p className="font-display text-2xl">{displayName(me)}</p>
              <p className="mt-1 text-sm text-muted-foreground">{me.email}</p>
              <p className="mt-1 text-sm text-muted-foreground">Member since {created}</p>
            </div>
          </div>
          <Button
            type="button"
            variant="outline"
            className="mt-8 rounded-full"
            onClick={() => document.getElementById('profile-first-name')?.focus()}
          >
            Edit profile
          </Button>
        </header>

        <section className="border-b border-border/70 pb-12">
          <h2 className="font-display text-3xl">Personal details</h2>
          <div className="mt-8">
            <ProfileForm key={me.id} email={me.email} initial={draftFrom(me)} onSave={save} />
          </div>
        </section>

        <section className="border-b border-border/70 pb-12">
          <h2 className="font-display text-3xl">Your Ecotech journey</h2>
          <div className="mt-8 grid gap-6 sm:grid-cols-3">
            <JourneyLink href="/profile/consultations" title="Consultations" text="Requests you have sent." />
            <JourneyLink
              href="/profile/transformations"
              title="Transformations"
              text="Studies of your openings."
            />
            <div>
              <p className="font-display text-xl">Projects</p>
              <p className="mt-2 text-sm text-muted-foreground">Projects will appear here.</p>
            </div>
          </div>
        </section>

        <section>
          <h2 className="font-display text-3xl">Account</h2>
          <Button
            type="button"
            variant="outline"
            className="mt-8 rounded-full"
            onClick={() => void account.signOut()}
          >
            Sign out
          </Button>
        </section>
      </Container>
    </Section>
  );
}

function JourneyLink({ href, title, text }: { href: string; title: string; text: string }) {
  return (
    <Link href={href} className="block">
      <p className="font-display text-xl">{title}</p>
      <p className="mt-2 text-sm text-muted-foreground">{text}</p>
    </Link>
  );
}

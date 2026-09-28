'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

import { Container, Section } from '@/components/layout/section';
import { useAccount } from '@/components/providers/account-provider';
import { Button } from '@/components/ui/button';
import { API_BASE_URL, CONSULTATION_HREF } from '@/lib/constants';

type ConsultationItem = {
  id: string;
  created_at: string;
  project_type: string;
  city: string;
  status: string;
  message: string;
};

type ConsultationPage = {
  items: ConsultationItem[];
  page: number;
  page_size: number;
  total: number;
  has_next: boolean;
};

const PROJECT_LABELS: Record<string, string> = {
  RESIDENTIAL: 'Residential',
  RENOVATION: 'Renovation',
  COMMERCIAL: 'Commercial',
  HOSPITALITY: 'Hospitality',
  ARCHITECTURAL: 'Architectural',
  ARCHITECT: 'Architect',
  OTHER: 'Other',
};

const STATUS_LABELS: Record<string, string> = {
  NEW: 'New',
  CONTACTED: 'Contacted',
  QUALIFIED: 'Qualified',
  PROPOSAL: 'Proposal',
  NEGOTIATION: 'Negotiation',
  WON: 'Won',
  LOST: 'Lost',
  CLOSED: 'Closed',
};

const PREVIEW_LENGTH = 180;

function label(map: Record<string, string>, value: string): string {
  return map[value] ?? value;
}

function formatDate(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat(undefined, {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(date);
}

export function ConsultationHistory() {
  const account = useAccount();
  const [page, setPage] = useState(1);
  const [data, setData] = useState<ConsultationPage | null>(null);
  const [phase, setPhase] = useState<'loading' | 'ready' | 'error'>('loading');
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (account.status !== 'authenticated') return;
    let cancelled = false;

    async function load() {
      setPhase('loading');
      try {
        const token = await account.getToken();
        const response = await fetch(
          `${API_BASE_URL}/consultations/me?page=${page}&page_size=10`,
          { headers: token ? { Authorization: `Bearer ${token}` } : {} },
        );
        if (!response.ok) throw new Error('unavailable');
        const body = (await response.json()) as ConsultationPage;
        if (!cancelled) {
          setData(body);
          setPhase('ready');
        }
      } catch {
        if (!cancelled) setPhase('error');
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [account, attempt, page]);

  return (
    <Section className="pt-28 sm:pt-32">
      <Container size="narrow">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">My consultations</p>
        <h1 className="mt-4 font-display text-4xl sm:text-5xl">Your Ecotech project conversations</h1>

        {phase === 'loading' ? (
          <p className="mt-12 text-sm text-muted-foreground">Loading your consultations</p>
        ) : null}

        {phase === 'error' ? (
          <div className="mt-12 max-w-md border-t border-border/70 pt-8">
            <p className="font-display text-2xl">We couldn&apos;t load your consultations</p>
            <p className="mt-3 text-sm text-muted-foreground">Please try again.</p>
            <Button
              type="button"
              variant="outline"
              className="mt-8 rounded-full"
              onClick={() => setAttempt((current) => current + 1)}
            >
              Try again
            </Button>
          </div>
        ) : null}

        {phase === 'ready' && data && data.total === 0 ? (
          <div className="mt-12 max-w-md border-t border-border/70 pt-8">
            <p className="font-display text-3xl">No consultations yet</p>
            <p className="mt-4 text-muted-foreground">
              Have a project in mind? Start a conversation with the Ecotech team.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button variant="accent" className="rounded-full" asChild>
                <Link href={CONSULTATION_HREF}>Request a Consultation</Link>
              </Button>
              <Button variant="outline" className="rounded-full" asChild>
                <Link href="/inspiration">Explore Inspiration</Link>
              </Button>
            </div>
          </div>
        ) : null}

        {phase === 'ready' && data && data.total > 0 ? (
          <div className="mt-12">
            <ul className="border-b border-border/70">
              {data.items.map((item) => (
                <li key={item.id}>
                  <ConsultationEntry item={item} />
                </li>
              ))}
            </ul>
            {data.page > 1 || data.has_next ? (
              <div className="mt-8 flex items-center justify-between gap-4 text-sm">
                <button
                  type="button"
                  className="disabled:opacity-40"
                  disabled={data.page <= 1}
                  onClick={() => setPage((current) => Math.max(1, current - 1))}
                >
                  Previous
                </button>
                <button
                  type="button"
                  className="disabled:opacity-40"
                  disabled={!data.has_next}
                  onClick={() => setPage((current) => current + 1)}
                >
                  Next
                </button>
              </div>
            ) : null}
          </div>
        ) : null}
      </Container>
    </Section>
  );
}

function ConsultationEntry({ item }: { item: ConsultationItem }) {
  const [open, setOpen] = useState(false);
  const long = item.message.length > PREVIEW_LENGTH;
  const message = open || !long ? item.message : `${item.message.slice(0, PREVIEW_LENGTH).trimEnd()}…`;

  return (
    <article className="border-t border-border/70 py-8">
      <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Consultation</p>
      <div className="mt-4 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2">
        <h2 className="font-display text-2xl">{label(PROJECT_LABELS, item.project_type)}</h2>
        <time dateTime={item.created_at} className="text-sm text-muted-foreground">
          {formatDate(item.created_at)}
        </time>
      </div>
      <p className="mt-2 text-sm">{item.city}</p>
      <p className="mt-6 text-xs uppercase tracking-[0.18em] text-muted-foreground">Status</p>
      <p className="mt-2 text-sm">{label(STATUS_LABELS, item.status)}</p>
      <p className="mt-6 max-w-xl whitespace-pre-wrap text-muted-foreground">{message}</p>
      {long ? (
        <button type="button" className="mt-4 text-sm tracking-wide" onClick={() => setOpen((current) => !current)}>
          {open ? 'Show less' : 'Read more'}
        </button>
      ) : null}
    </article>
  );
}

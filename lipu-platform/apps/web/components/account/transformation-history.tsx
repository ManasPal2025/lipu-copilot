'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

import { Container, Section } from '@/components/layout/section';
import { useAccount } from '@/components/providers/account-provider';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { API_BASE_URL, TRANSFORM_HREF } from '@/lib/constants';

type HistoryAsset = {
  id: string;
  mime_type: string;
  public_url: string | null;
};

type HistoryResult = {
  id: string;
  created_at: string;
  asset: HistoryAsset | null;
};

type TransformationItem = {
  id: string;
  created_at: string;
  target: string;
  variant: string | null;
  status: string;
  source_asset: HistoryAsset | null;
  result: HistoryResult | null;
};

type TransformationPage = {
  items: TransformationItem[];
  page: number;
  page_size: number;
  total: number;
  has_next: boolean;
};

const TARGET_LABELS: Record<string, string> = {
  WINDOWS: 'Windows',
  DOORS: 'Doors',
  BALCONY: 'Balcony',
  TERRACE: 'Terrace',
  OUTDOOR: 'Outdoor',
};

const VARIANT_LABELS: Record<string, string> = {
  SLIDING: 'Sliding',
  CASEMENT: 'Casement',
  LARGE_OPENING: 'Large Opening',
  BIFOLD: 'Bifold',
  FRENCH: 'French',
};

const STATUS_LABELS: Record<string, string> = {
  UPLOADED: 'Uploaded',
  CONFIGURED: 'Configured',
  PROCESSING: 'Processing',
  COMPLETED: 'Completed',
  FAILED: 'Failed',
};

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

function safeImageUrl(value: string | null | undefined): string | null {
  if (!value) return null;
  if (value.startsWith('/images/')) {
    if (value.includes('..') || value.includes('\\') || value.includes('?') || value.includes('#')) {
      return null;
    }
    return value;
  }
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' && url.protocol !== 'http:') return null;
    if (url.username || url.password) return null;
    return url.toString();
  } catch {
    return null;
  }
}

export function TransformationHistory() {
  const account = useAccount();
  const [page, setPage] = useState(1);
  const [items, setItems] = useState<TransformationItem[]>([]);
  const [total, setTotal] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [phase, setPhase] = useState<'loading' | 'ready' | 'error'>('loading');
  const [loadingMore, setLoadingMore] = useState(false);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (account.status !== 'authenticated') return;
    let cancelled = false;

    async function load() {
      if (page === 1) setPhase('loading');
      else setLoadingMore(true);
      try {
        const token = await account.getToken();
        const response = await fetch(
          `${API_BASE_URL}/transform/requests/me?page=${page}&page_size=10`,
          { headers: token ? { Authorization: `Bearer ${token}` } : {} },
        );
        if (!response.ok) throw new Error('unavailable');
        const body = (await response.json()) as TransformationPage;
        if (!cancelled) {
          setItems((current) => (page === 1 ? body.items : [...current, ...body.items]));
          setTotal(body.total);
          setHasNext(body.has_next);
          setPhase('ready');
          setLoadingMore(false);
        }
      } catch {
        if (!cancelled) {
          setLoadingMore(false);
          setPhase('error');
        }
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [account, attempt, page]);

  async function retryGeneration(id: string) {
    try {
      const token = await account.getToken();
      const response = await fetch(`${API_BASE_URL}/transform/requests/${id}/generate`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!response.ok) return;
      const body = (await response.json()) as {
        status?: string;
        result?: { id: string; mime_type: string; public_url: string | null };
      };
      setItems((current) =>
        current.map((item) =>
          item.id === id
            ? {
                ...item,
                status: body.status ?? item.status,
                result: body.result
                  ? {
                      id: body.result.id,
                      created_at: item.created_at,
                      asset: body.result,
                    }
                  : item.result,
              }
            : item,
        ),
      );
    } catch {
      return;
    }
  }

  return (
    <Section className="pt-28 sm:pt-32">
      <Container size="narrow">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Your transformations</p>
        <h1 className="mt-4 font-display text-4xl sm:text-5xl">
          A record of the spaces you&apos;ve explored with Ecotech.
        </h1>

        {phase === 'loading' ? (
          <p className="mt-12 text-sm text-muted-foreground">Loading your transformations</p>
        ) : null}

        {phase === 'error' ? (
          <div className="mt-12 max-w-md border-t border-border/70 pt-8">
            <p className="font-display text-2xl">We couldn&apos;t load your transformations</p>
            <p className="mt-3 text-sm text-muted-foreground">Please try again.</p>
            <Button
              type="button"
              variant="outline"
              className="mt-8 rounded-full"
              onClick={() => {
                setPage(1);
                setAttempt((current) => current + 1);
              }}
            >
              Try again
            </Button>
          </div>
        ) : null}

        {phase === 'ready' && total === 0 ? (
          <div className="mt-12 max-w-md border-t border-border/70 pt-8">
            <p className="font-display text-3xl">No transformations yet</p>
            <p className="mt-4 text-muted-foreground">Explore how your space could look with Ecotech.</p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button variant="accent" className="rounded-full" asChild>
                <Link href={TRANSFORM_HREF}>Transform Your Space</Link>
              </Button>
              <Button variant="outline" className="rounded-full" asChild>
                <Link href="/inspiration">Explore Inspiration</Link>
              </Button>
            </div>
          </div>
        ) : null}

        {phase === 'ready' && total > 0 ? (
          <div className="mt-12">
            <ul className="border-b border-border/70">
              {items.map((item) => (
                <li key={item.id}>
                  <TransformationEntry item={item} onRetry={(id) => void retryGeneration(id)} />
                </li>
              ))}
            </ul>
            {hasNext ? (
              <div className="mt-8">
                <Button
                  type="button"
                  variant="outline"
                  className="rounded-full"
                  disabled={loadingMore}
                  onClick={() => setPage((current) => current + 1)}
                >
                  Load more
                </Button>
              </div>
            ) : null}
          </div>
        ) : null}
      </Container>
    </Section>
  );
}

function TransformationEntry({
  item,
  onRetry,
}: {
  item: TransformationItem;
  onRetry: (id: string) => void;
}) {
  const sourceUrl = safeImageUrl(item.source_asset?.public_url);
  const resultUrl = safeImageUrl(item.result?.asset?.public_url);

  return (
    <article className="border-t border-border/70 py-8">
      <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Transformation</p>
      <div className="mt-4 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2">
        <h2 className="font-display text-2xl">{label(TARGET_LABELS, item.target)}</h2>
        <time dateTime={item.created_at} className="text-sm text-muted-foreground">
          {formatDate(item.created_at)}
        </time>
      </div>
      {item.variant ? <p className="mt-2 text-sm">{label(VARIANT_LABELS, item.variant)}</p> : null}
      <p className="mt-6 text-xs uppercase tracking-[0.18em] text-muted-foreground">Status</p>
      <p className="mt-2 text-sm">{label(STATUS_LABELS, item.status)}</p>
      {sourceUrl || resultUrl ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {sourceUrl ? (
            <figure>
              {sourceUrl.startsWith('/images/') ? (
                <ArchitecturalImage src={sourceUrl} alt="Your space" aspect="video" />
              ) : (
                <div className="relative aspect-video overflow-hidden bg-stone-200">
                  {/* Signed URLs are short-lived and come from a private bucket, so they cannot be listed as Next image hosts. */}
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={sourceUrl} alt="Your space" className="h-full w-full object-cover" />
                </div>
              )}
              <figcaption className="mt-2 text-xs uppercase tracking-[0.18em] text-muted-foreground">
                Your space
              </figcaption>
            </figure>
          ) : null}
          {resultUrl ? (
            <figure>
              {resultUrl.startsWith('/images/') ? (
                <ArchitecturalImage src={resultUrl} alt="Ecotech possibility" aspect="video" />
              ) : (
                <div className="relative aspect-video overflow-hidden bg-stone-200">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={resultUrl} alt="Ecotech possibility" className="h-full w-full object-cover" />
                </div>
              )}
              <figcaption className="mt-2 text-xs uppercase tracking-[0.18em] text-muted-foreground">
                Ecotech possibility
              </figcaption>
            </figure>
          ) : null}
        </div>
      ) : null}
      {item.status === 'PROCESSING' ? (
        <p className="mt-6 max-w-xl text-sm text-muted-foreground">Your visualization is being prepared.</p>
      ) : null}
      {item.status === 'FAILED' ? (
        <div className="mt-6 max-w-xl">
          <p className="text-sm text-muted-foreground">
            {"We couldn't complete this transformation. Your original image is safe."}
          </p>
          <button type="button" className="mt-3 text-sm tracking-wide" onClick={() => onRetry(item.id)}>
            Try again
          </button>
        </div>
      ) : null}
      {!sourceUrl && !resultUrl && item.status !== 'PROCESSING' && item.status !== 'FAILED' ? (
        <p className="mt-6 max-w-xl text-sm text-muted-foreground">
          A visual record is not available for this request.
        </p>
      ) : null}
    </article>
  );
}

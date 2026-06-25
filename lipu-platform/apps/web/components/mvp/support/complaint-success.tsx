import Link from 'next/link';
import { CheckCircle2, Phone } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { getIssueLabel, getProductLabel, type ComplaintSubmitResponse } from '@/lib/support-types';

interface ComplaintSuccessProps {
  response: ComplaintSubmitResponse;
  productType: string;
  issueType: string;
  phone: string;
  onSubmitAnother: () => void;
}

export function ComplaintSuccess({
  response,
  productType,
  issueType,
  phone,
  onSubmitAnother,
}: ComplaintSuccessProps) {
  return (
    <div className="rounded-sm border border-border bg-card p-8 text-center shadow-sm sm:p-12">
      <CheckCircle2 className="mx-auto h-14 w-14 text-accent" aria-hidden />
      <p className="mt-8 text-xs uppercase tracking-[0.2em] text-muted-foreground">Reference number</p>
      <p className="mt-2 font-display text-4xl tracking-wide">{response.ticketNumber}</p>
      <h2 className="mt-8 font-display text-3xl">We have received your message</h2>
      <p className="mx-auto mt-4 max-w-md text-muted-foreground editorial-prose">{response.message}</p>

      <div className="mx-auto mt-8 max-w-sm rounded-sm bg-muted/30 p-5 text-left text-sm">
        <p className="font-medium">{getProductLabel(productType)}</p>
        <p className="mt-1 text-muted-foreground">{getIssueLabel(issueType)}</p>
        <p className="mt-4 flex items-center gap-2 text-muted-foreground">
          <Phone className="h-4 w-4 shrink-0" aria-hidden />
          We will reach you at {phone}
        </p>
      </div>

      <p className="mx-auto mt-6 max-w-md text-xs text-muted-foreground">
        Save your reference number. A copy is stored on this device for your convenience.
      </p>

      <div className="mt-10 flex flex-wrap justify-center gap-4">
        <Button variant="accent" asChild>
          <Link href="/">Back to home</Link>
        </Button>
        <Button variant="outline" type="button" onClick={onSubmitAnother}>
          Submit another issue
        </Button>
      </div>
    </div>
  );
}

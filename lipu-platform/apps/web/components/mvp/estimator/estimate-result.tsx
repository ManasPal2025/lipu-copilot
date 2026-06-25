import Link from 'next/link';
import { ArrowRight, Info } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Button } from '@/components/ui/button';
import { formatInr, type EstimateResult } from '@/lib/pricing-calculator';

interface EstimateResultCardProps {
  result: EstimateResult;
  width: number;
  height: number;
  onReset: () => void;
}

export function EstimateResultCard({ result, width, height, onReset }: EstimateResultCardProps) {
  return (
    <FadeIn>
      <div className="rounded-sm border border-border bg-card p-6 shadow-sm sm:p-8">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Your estimate</p>
        <h2 className="mt-3 font-display text-3xl sm:text-4xl">
          {formatInr(result.minTotal)} – {formatInr(result.maxTotal)}
        </h2>
        <p className="mt-3 text-sm text-muted-foreground">
          {result.windowType.label} · {width} × {height} ft · {result.glassType.label}
        </p>

        <div className="mt-8 space-y-4 border-t border-border pt-8">
          {result.lineItems.map((item) => (
            <div key={item.label} className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-medium">{item.label}</p>
                {item.detail && <p className="mt-1 text-xs text-muted-foreground">{item.detail}</p>}
              </div>
              <p className="shrink-0 text-sm font-medium">{formatInr(item.amount)}</p>
            </div>
          ))}

          <div className="flex items-center justify-between border-t border-border pt-4">
            <p className="font-display text-lg">Mid-point total</p>
            <p className="font-display text-lg">{formatInr(result.total)}</p>
          </div>
        </div>

        <div className="mt-6 flex items-start gap-3 rounded-sm bg-muted/40 p-4">
          <Info className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" aria-hidden />
          <p className="text-xs leading-relaxed text-muted-foreground">{result.disclaimer}</p>
        </div>

        <div className="mt-8 flex flex-wrap gap-4">
          <Button variant="accent" asChild>
            <Link href="/contact#quote">
              Book a site visit for exact quote
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/wizard">Not sure which type? Try the wizard</Link>
          </Button>
          <Button variant="ghost" type="button" onClick={onReset}>
            Calculate again
          </Button>
        </div>
      </div>
    </FadeIn>
  );
}

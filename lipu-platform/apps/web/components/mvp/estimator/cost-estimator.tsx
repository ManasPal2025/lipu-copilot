'use client';

import { useState } from 'react';
import { Calculator } from 'lucide-react';

import { EstimateResultCard } from '@/components/mvp/estimator/estimate-result';
import { FadeIn } from '@/components/motion/fade-in';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { calculateEstimate, rules, type EstimateResult } from '@/lib/pricing-calculator';
import { cn } from '@/lib/utils';

export function CostEstimator() {
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');
  const [windowTypeId, setWindowTypeId] = useState(rules.windowTypes[0]?.id ?? '');
  const [glassTypeId, setGlassTypeId] = useState(rules.glassTypes[1]?.id ?? 'double');
  const [result, setResult] = useState<EstimateResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  function handleCalculate(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);

    const widthNum = parseFloat(width);
    const heightNum = parseFloat(height);

    if (!width || !height || Number.isNaN(widthNum) || Number.isNaN(heightNum)) {
      setError('Enter valid width and height in feet.');
      setResult(null);
      return;
    }

    if (widthNum <= 0 || heightNum <= 0) {
      setError('Width and height must be greater than zero.');
      setResult(null);
      return;
    }

    if (widthNum > 20 || heightNum > 12) {
      setError('For openings larger than 20 × 12 ft, please request a custom consultation.');
      setResult(null);
      return;
    }

    const estimate = calculateEstimate({
      width: widthNum,
      height: heightNum,
      windowTypeId,
      glassTypeId,
    });

    if (!estimate) {
      setError('Could not calculate estimate. Check your selections.');
      setResult(null);
      return;
    }

    setResult(estimate);
  }

  function handleReset() {
    setResult(null);
    setError(null);
  }

  if (result) {
    return (
      <EstimateResultCard
        result={result}
        width={parseFloat(width)}
        height={parseFloat(height)}
        onReset={handleReset}
      />
    );
  }

  return (
    <FadeIn>
      <form onSubmit={handleCalculate} className="space-y-10">
        <div className="grid gap-6 sm:grid-cols-2">
          <div>
            <label htmlFor="width" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Width ({rules.dimensionUnit})
            </label>
            <Input
              id="width"
              name="width"
              type="number"
              inputMode="decimal"
              min="0.5"
              step="0.1"
              placeholder="e.g. 4"
              value={width}
              onChange={(e) => setWidth(e.target.value)}
              required
              className="h-12"
            />
          </div>
          <div>
            <label htmlFor="height" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Height ({rules.dimensionUnit})
            </label>
            <Input
              id="height"
              name="height"
              type="number"
              inputMode="decimal"
              min="0.5"
              step="0.1"
              placeholder="e.g. 5"
              value={height}
              onChange={(e) => setHeight(e.target.value)}
              required
              className="h-12"
            />
          </div>
        </div>

        <fieldset>
          <legend className="mb-4 text-xs font-medium uppercase tracking-wider">Window type</legend>
          <div className="grid gap-3 sm:grid-cols-2">
            {rules.windowTypes.map((type) => (
              <button
                key={type.id}
                type="button"
                onClick={() => setWindowTypeId(type.id)}
                className={cn(
                  'rounded-sm border p-4 text-left transition-colors',
                  windowTypeId === type.id
                    ? 'border-accent bg-accent/5 ring-1 ring-accent'
                    : 'border-border bg-card hover:border-foreground/25',
                )}
              >
                <span className="font-display text-base">{type.label}</span>
                <p className="mt-1 text-xs text-muted-foreground">{type.description}</p>
              </button>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="mb-4 text-xs font-medium uppercase tracking-wider">Glass type</legend>
          <div className="grid gap-3 sm:grid-cols-2">
            {rules.glassTypes.map((type) => (
              <button
                key={type.id}
                type="button"
                onClick={() => setGlassTypeId(type.id)}
                className={cn(
                  'rounded-sm border p-4 text-left transition-colors',
                  glassTypeId === type.id
                    ? 'border-accent bg-accent/5 ring-1 ring-accent'
                    : 'border-border bg-card hover:border-foreground/25',
                )}
              >
                <span className="font-display text-base">{type.label}</span>
                <p className="mt-1 text-xs text-muted-foreground">{type.description}</p>
              </button>
            ))}
          </div>
        </fieldset>

        {error && (
          <p className="text-sm text-destructive" role="alert">
            {error}
          </p>
        )}

        <div className="border-t border-border pt-8">
          <Button type="submit" variant="accent" size="lg">
            <Calculator className="h-4 w-4" />
            Calculate estimate
          </Button>
          <p className="mt-4 text-xs text-muted-foreground">
            Rates from configurable pricing rules — indicative only, inclusive of GST at{' '}
            {Math.round(rules.gstRate * 100)}%.
          </p>
        </div>
      </form>
    </FadeIn>
  );
}

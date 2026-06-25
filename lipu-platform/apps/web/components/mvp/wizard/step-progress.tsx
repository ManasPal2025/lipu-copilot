import { cn } from '@/lib/utils';

interface StepProgressProps {
  current: number;
  total: number;
  labels?: string[];
}

export function StepProgress({ current, total, labels }: StepProgressProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between text-xs uppercase tracking-[0.15em] text-muted-foreground">
        <span>
          Step {current + 1} of {total}
        </span>
        {labels?.[current] && <span className="normal-case tracking-normal">{labels[current]}</span>}
      </div>
      <div className="flex gap-2">
        {Array.from({ length: total }).map((_, index) => (
          <div
            key={index}
            className={cn(
              'h-1 flex-1 rounded-full transition-colors duration-300',
              index <= current ? 'bg-accent' : 'bg-border',
            )}
            aria-hidden
          />
        ))}
      </div>
    </div>
  );
}

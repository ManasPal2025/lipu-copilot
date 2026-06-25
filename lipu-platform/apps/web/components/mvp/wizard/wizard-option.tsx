import { cn } from '@/lib/utils';

interface WizardOptionProps {
  label: string;
  description: string;
  selected: boolean;
  onSelect: () => void;
}

export function WizardOption({ label, description, selected, onSelect }: WizardOptionProps) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        'w-full rounded-sm border p-5 text-left transition-colors',
        selected
          ? 'border-accent bg-accent/5 ring-1 ring-accent'
          : 'border-border bg-card hover:border-foreground/25',
      )}
    >
      <span className="font-display text-lg">{label}</span>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{description}</p>
    </button>
  );
}

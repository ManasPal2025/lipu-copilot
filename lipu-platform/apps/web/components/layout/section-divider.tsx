export function SectionDivider({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-6 px-5 sm:px-6 lg:px-8" aria-hidden={!label}>
      <div className="h-px flex-1 bg-border" />
      {label && (
        <span className="text-[10px] uppercase tracking-[0.3em] text-muted-foreground">{label}</span>
      )}
      <div className="h-px flex-1 bg-border" />
    </div>
  );
}

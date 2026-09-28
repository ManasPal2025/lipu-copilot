'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, DoorOpen, PanelTop, Square, Sunset, Trees, Upload, X } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section } from '@/components/layout/section';
import { useAccount } from '@/components/providers/account-provider';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import { Button } from '@/components/ui/button';
import { images, type ImageAsset } from '@/lib/images';
import { API_BASE_URL } from '@/lib/constants';
import {
  getDemoResult,
  type TransformDemoResult,
  type TransformTarget,
  type TransformVariant,
} from '@/lib/transform-demo';
import { cn } from '@/lib/utils';

const ACCEPT = 'image/jpeg,image/png,image/webp';
const MAX_BYTES = 10 * 1024 * 1024;

type Source =
  | { kind: 'file'; file: File; previewUrl: string; name: string }
  | { kind: 'sample'; id: string; image: ImageAsset };

const MARK_CROP = 'origin-top scale-[1.24]';

const SAMPLES: { id: string; label: string; image: ImageAsset }[] = [
  { id: 'villa', label: 'Villa', image: images.ecotechTransform.villa },
  { id: 'apartment', label: 'Apartment', image: images.ecotechTransform.apartment },
  { id: 'living', label: 'Living', image: images.ecotechTransform.living },
  { id: 'balcony', label: 'Balcony', image: images.ecotechTransform.balcony },
];

const TARGETS: { id: TransformTarget; label: string; icon: typeof Square }[] = [
  { id: 'windows', label: 'Windows', icon: Square },
  { id: 'doors', label: 'Doors', icon: DoorOpen },
  { id: 'balcony', label: 'Balcony', icon: PanelTop },
  { id: 'terrace', label: 'Terrace', icon: Sunset },
  { id: 'outdoor', label: 'Outdoor', icon: Trees },
];

const WINDOW_VARIANTS: { id: TransformVariant; label: string }[] = [
  { id: 'sliding', label: 'Sliding' },
  { id: 'casement', label: 'Casement' },
  { id: 'large-opening', label: 'Large opening' },
];

const DOOR_VARIANTS: { id: TransformVariant; label: string }[] = [
  { id: 'sliding', label: 'Sliding' },
  { id: 'bifold', label: 'Bifold' },
  { id: 'french', label: 'French' },
];

const API_TARGET: Record<TransformTarget, string> = {
  windows: 'WINDOWS',
  doors: 'DOORS',
  balcony: 'BALCONY',
  terrace: 'TERRACE',
  outdoor: 'OUTDOOR',
};

const API_VARIANT: Record<TransformVariant, string> = {
  sliding: 'SLIDING',
  casement: 'CASEMENT',
  'large-opening': 'LARGE_OPENING',
  bifold: 'BIFOLD',
  french: 'FRENCH',
};

const SAVE_NOTICE =
  "We couldn't save this transformation to your account. You can still continue with the preview.";
const UPLOAD_FAILED =
  "Upload failed. We couldn't save this transformation to your account. You can still continue with the preview.";
const GENERATION_FAILED =
  "We couldn't complete this transformation. Your original image is safe.";
const ALREADY_PROCESSING = 'Transformation is already being processed.';

type PipelinePhase = 'idle' | 'preparing' | 'uploading' | 'configuring' | 'processing' | 'completed' | 'failed';

function persistenceBody(source: Source, target: TransformTarget, variant?: TransformVariant) {
  return {
    target: API_TARGET[target],
    variant: variant ? API_VARIANT[variant] : null,
    source_asset:
      source.kind === 'sample'
        ? { mime_type: 'image/png', source_kind: 'SAMPLE', sample_id: source.id }
        : { mime_type: source.file.type, source_kind: 'UPLOAD' },
  };
}

function revokeIfFile(source: Source | null) {
  if (source?.kind === 'file') URL.revokeObjectURL(source.previewUrl);
}

export function TransformWorkspace() {
  const inputRef = useRef<HTMLInputElement>(null);
  const sourceRef = useRef<Source | null>(null);
  const timerRef = useRef<number | null>(null);
  const [source, setSource] = useState<Source | null>(null);
  const [target, setTarget] = useState<TransformTarget | null>(null);
  const [variant, setVariant] = useState<TransformVariant | undefined>();
  const [dragging, setDragging] = useState(false);
  const [status, setStatus] = useState<'idle' | 'processing' | 'result' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [result, setResult] = useState<TransformDemoResult | null>(null);
  const [saveNotice, setSaveNotice] = useState<string | null>(null);
  const [pipelinePhase, setPipelinePhase] = useState<PipelinePhase>('idle');
  const [requestId, setRequestId] = useState<string | null>(null);
  const [requestSelection, setRequestSelection] = useState<string | null>(null);
  const [generatedUrl, setGeneratedUrl] = useState<string | null>(null);
  const busyRef = useRef(false);

  const account = useAccount();

  const previewSrc = source?.kind === 'file' ? source.previewUrl : source?.image.src;
  const previewAlt = source?.kind === 'file' ? source.name : source?.image.alt;
  const sourceLabel = source?.kind === 'file' ? source.name : source ? `Sample · ${source.id}` : null;
  const configured = Boolean(source && target);
  const variants = target === 'windows' ? WINDOW_VARIANTS : target === 'doors' ? DOOR_VARIANTS : null;

  const currentSrc = previewSrc;

  const clearTimer = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const replaceSource = useCallback(
    (next: Source | null) => {
      clearTimer();
      setSource((prev) => {
        revokeIfFile(prev);
        sourceRef.current = next;
        return next;
      });
      setResult(null);
      setStatus('idle');
      setErrorMessage(null);
      setSaveNotice(null);
      setPipelinePhase('idle');
      setRequestId(null);
      setRequestSelection(null);
      setGeneratedUrl(null);
    },
    [clearTimer],
  );

  useEffect(() => {
    return () => {
      clearTimer();
      revokeIfFile(sourceRef.current);
    };
  }, [clearTimer]);

  function validateFile(file: File): string | null {
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      return 'Please choose a JPG, PNG, or WebP image.';
    }
    if (file.size > MAX_BYTES) {
      return 'Please choose an image under 10 MB.';
    }
    return null;
  }

  function handleFiles(files: FileList | null) {
    const file = files?.[0];
    if (!file) return;
    const message = validateFile(file);
    if (message) {
      setStatus('error');
      setErrorMessage(message);
      return;
    }
    replaceSource({
      kind: 'file',
      file,
      previewUrl: URL.createObjectURL(file),
      name: file.name,
    });
  }

  function handleTarget(next: TransformTarget) {
    clearTimer();
    setTarget(next);
    setVariant(undefined);
    setResult(null);
    if (status === 'result' || status === 'processing') setStatus('idle');
  }

  async function authorizedFetch(path: string, init: RequestInit): Promise<Response | null> {
    const token = await account.getToken();
    if (!token) return null;
    const headers = new Headers(init.headers);
    headers.set('Authorization', `Bearer ${token}`);
    return fetch(`${API_BASE_URL}${path}`, { ...init, headers });
  }

  async function persistCurrent(
    current: Source,
    currentTarget: TransformTarget,
    currentVariant: TransformVariant | undefined,
  ): Promise<string | null> {
    if (account.status !== 'authenticated') return null;
    const uploading = current.kind === 'file';
    if (uploading) setPipelinePhase('uploading');
    try {
      const headers: Record<string, string> = {};
      let body: BodyInit;
      if (current.kind === 'file') {
        const form = new FormData();
        form.append('target', API_TARGET[currentTarget]);
        if (currentVariant) form.append('variant', API_VARIANT[currentVariant]);
        form.append('source_kind', 'UPLOAD');
        form.append('file', current.file);
        body = form;
      } else {
        headers['Content-Type'] = 'application/json';
        body = JSON.stringify(persistenceBody(current, currentTarget, currentVariant));
      }
      const response = await authorizedFetch('/transform/requests', { method: 'POST', headers, body });
      if (!response?.ok) {
        if (uploading) setPipelinePhase('failed');
        return null;
      }
      const created = (await response.json()) as { id?: string };
      return created.id ?? null;
    } catch {
      if (uploading) setPipelinePhase('failed');
      return null;
    }
  }

  function selectionKey(currentTarget: TransformTarget, currentVariant: TransformVariant | undefined) {
    return `${currentTarget}:${currentVariant ?? ''}`;
  }

  async function configureRequest(
    id: string,
    currentTarget: TransformTarget,
    currentVariant: TransformVariant | undefined,
  ): Promise<boolean> {
    setPipelinePhase('configuring');
    const response = await authorizedFetch(`/transform/requests/${id}/configure`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target: API_TARGET[currentTarget],
        variant: currentVariant ? API_VARIANT[currentVariant] : null,
      }),
    });
    return Boolean(response?.ok);
  }

  async function generateRequest(id: string): Promise<{ url: string | null; notice: string | null }> {
    setPipelinePhase('processing');
    const response = await authorizedFetch(`/transform/requests/${id}/generate`, { method: 'POST' });
    if (!response) return { url: null, notice: GENERATION_FAILED };
    if (response.status === 409) return { url: null, notice: ALREADY_PROCESSING };
    if (!response.ok) return { url: null, notice: GENERATION_FAILED };
    const body = (await response.json()) as { result?: { public_url?: string | null } };
    const url = body.result?.public_url ?? null;
    return { url, notice: url ? null : GENERATION_FAILED };
  }

  function showDemonstration(
    current: Source,
    currentTarget: TransformTarget,
    currentVariant: TransformVariant | undefined,
  ) {
    const demo = getDemoResult(
      {
        target: currentTarget,
        variant: currentVariant,
        sourceKind: current.kind === 'file' ? 'upload' : 'sample',
        sampleId: current.kind === 'sample' ? current.id : undefined,
      },
      current.kind === 'file' ? current.previewUrl : current.image.src,
    );
    timerRef.current = window.setTimeout(() => {
      setGeneratedUrl(null);
      setResult(demo);
      setStatus('result');
      timerRef.current = null;
    }, 1100);
  }

  async function runAuthenticatedUpload(
    current: Extract<Source, { kind: 'file' }>,
    currentTarget: TransformTarget,
    currentVariant: TransformVariant | undefined,
  ) {
    const selection = selectionKey(currentTarget, currentVariant);
    if (pipelinePhase === 'completed' && requestId && requestSelection === selection) {
      setStatus('result');
      return;
    }
    let id = requestId;
    if (!id || (requestSelection !== null && requestSelection !== selection)) {
      setPipelinePhase('preparing');
      id = await persistCurrent(current, currentTarget, currentVariant);
      if (!id) {
        setSaveNotice(UPLOAD_FAILED);
        setStatus('idle');
        return;
      }
      setRequestId(id);
      setRequestSelection(null);
    }
    if (requestSelection !== selection) {
      const configured = await configureRequest(id, currentTarget, currentVariant);
      if (!configured) {
        setSaveNotice(GENERATION_FAILED);
        setPipelinePhase('failed');
        setStatus('idle');
        return;
      }
      setRequestSelection(selection);
    }
    const generated = await generateRequest(id);
    if (!generated.url) {
      setSaveNotice(generated.notice);
      setPipelinePhase('failed');
      setStatus('idle');
      return;
    }
    setGeneratedUrl(generated.url);
    setResult(null);
    setPipelinePhase('completed');
    setSaveNotice(null);
    setStatus('result');
  }

  async function handleVisualize() {
    if (!source || !target || busyRef.current) return;
    busyRef.current = true;
    clearTimer();
    setStatus('processing');
    setErrorMessage(null);
    setSaveNotice(null);
    try {
      if (account.status === 'authenticated' && source.kind === 'file') {
        await runAuthenticatedUpload(source, target, variant);
        return;
      }
      if (account.status === 'authenticated') {
        const saved = await persistCurrent(source, target, variant);
        setSaveNotice(saved ? null : SAVE_NOTICE);
      }
      showDemonstration(source, target, variant);
    } catch {
      setSaveNotice(source.kind === 'file' ? GENERATION_FAILED : SAVE_NOTICE);
      setPipelinePhase('failed');
      setStatus('idle');
    } finally {
      busyRef.current = false;
    }
  }

  async function retrySave() {
    if (!source || !target || busyRef.current) return;
    if (account.status === 'authenticated' && source.kind === 'file') {
      busyRef.current = true;
      setStatus('processing');
      setSaveNotice(null);
      try {
        await runAuthenticatedUpload(source, target, variant);
      } finally {
        busyRef.current = false;
      }
      return;
    }
    const saved = await persistCurrent(source, target, variant);
    setSaveNotice(saved ? null : SAVE_NOTICE);
  }

  function handleReset() {
    replaceSource(null);
    setTarget(null);
    setVariant(undefined);
    if (inputRef.current) inputRef.current.value = '';
  }

  const beforeLabel = 'Your space';
  const afterImage = result?.image;

  return (
    <Section className="pt-4 sm:pt-6 lg:pt-8" id="workspace">
      <Container>
        <FadeIn>
          <div className="rounded-md border border-border/80 bg-background/70 p-4 shadow-sm backdrop-blur-md sm:p-6 lg:p-8">
            <div className="grid gap-8 lg:grid-cols-12 lg:gap-10">
              <div className="lg:col-span-7">
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
                  Upload a photo
                </p>
                <h2 className="mt-2 font-display text-xl sm:text-2xl">Your space</h2>

                <input
                  ref={inputRef}
                  type="file"
                  accept={ACCEPT}
                  className="sr-only"
                  onChange={(event) => handleFiles(event.target.files)}
                />

                {source && previewSrc ? (
                  <div className="mt-6 overflow-hidden rounded-md border border-border">
                    <div className="relative">
                      <ArchitecturalImage
                        src={previewSrc}
                        alt={previewAlt ?? 'Uploaded space'}
                        aspect="video"
                        sizes="(max-width: 1024px) 100vw, 58vw"
                        className={source.kind === 'sample' && source.id === 'villa' ? MARK_CROP : undefined}
                      />
                      {status === 'processing' ? (
                        <div className="absolute inset-0 flex items-center justify-center bg-stone-925/45 backdrop-blur-[2px]">
                          <p className="text-sm uppercase tracking-[0.2em] text-stone-100">
                            {account.status === 'authenticated' && source.kind === 'file'
                              ? pipelinePhase === 'uploading'
                                ? 'Uploading image'
                                : pipelinePhase === 'configuring'
                                  ? 'Configuring'
                                  : pipelinePhase === 'processing'
                                    ? 'Processing'
                                    : 'Preparing'
                              : 'Preparing a demonstration preview'}
                          </p>
                        </div>
                      ) : null}
                    </div>
                    <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border px-4 py-3">
                      <p className="truncate text-sm text-muted-foreground">{sourceLabel}</p>
                      <div className="flex gap-2">
                        <Button type="button" variant="outline" size="sm" onClick={() => inputRef.current?.click()}>
                          Replace
                        </Button>
                        <Button type="button" variant="ghost" size="sm" onClick={handleReset}>
                          Remove
                        </Button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <button
                    type="button"
                    onClick={() => inputRef.current?.click()}
                    onDragEnter={(event) => {
                      event.preventDefault();
                      setDragging(true);
                    }}
                    onDragOver={(event) => {
                      event.preventDefault();
                      setDragging(true);
                    }}
                    onDragLeave={() => setDragging(false)}
                    onDrop={(event) => {
                      event.preventDefault();
                      setDragging(false);
                      handleFiles(event.dataTransfer.files);
                    }}
                    className={cn(
                      'mt-4 flex min-h-[200px] w-full flex-col items-center justify-center rounded-md border border-dashed px-6 py-10 text-center transition-colors sm:min-h-[260px]',
                      dragging
                        ? 'border-foreground bg-muted/40'
                        : 'border-border bg-muted/20 hover:border-foreground/40 hover:bg-muted/30',
                    )}
                  >
                    <Upload className="mb-4 h-6 w-6 text-muted-foreground" aria-hidden />
                    <p className="font-display text-xl">Upload your image</p>
                    <p className="mt-2 text-sm text-muted-foreground">Drag and drop or browse. JPG, PNG, or WebP.</p>
                  </button>
                )}

                {status === 'error' && errorMessage ? (
                  <p className="mt-3 text-sm text-muted-foreground">{errorMessage}</p>
                ) : null}

                <div className="mt-8">
                  <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
                    Or try a sample
                  </p>
                  <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                    {SAMPLES.map((sample) => {
                      const selected = source?.kind === 'sample' && source.id === sample.id;
                      return (
                        <button
                          key={sample.id}
                          type="button"
                          onClick={() => replaceSource({ kind: 'sample', id: sample.id, image: sample.image })}
                          className={cn(
                            'overflow-hidden rounded-md border text-left transition-colors',
                            selected ? 'border-foreground' : 'border-border hover:border-foreground/40',
                          )}
                        >
                          <ArchitecturalImage
                            src={sample.image.src}
                            alt={sample.image.alt}
                            aspect="video"
                            sizes="(max-width: 640px) 50vw, 15vw"
                            className={sample.id === 'villa' ? MARK_CROP : undefined}
                          />
                          <span className="block px-2 py-2 text-xs text-muted-foreground">{sample.label}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>

              <div className="lg:col-span-5">
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
                  Choose what to transform
                </p>
                <h2 className="mt-2 font-display text-xl sm:text-2xl">What should change?</h2>

                <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-2">
                  {TARGETS.map((item) => {
                    const Icon = item.icon;
                    const selected = target === item.id;
                    return (
                      <button
                        key={item.id}
                        type="button"
                        onClick={() => handleTarget(item.id)}
                        className={cn(
                          'flex flex-col items-start gap-3 rounded-md border px-4 py-4 text-left transition-colors',
                          selected
                            ? 'border-foreground bg-foreground text-background'
                            : 'border-border bg-background/80 hover:border-foreground/40',
                        )}
                      >
                        <Icon className="h-5 w-5" aria-hidden />
                        <span className="font-display text-lg">{item.label}</span>
                      </button>
                    );
                  })}
                </div>

                {variants ? (
                  <div className="mt-6">
                    <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Opening type</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {variants.map((item) => (
                        <button
                          key={item.id}
                          type="button"
                          onClick={() => setVariant(item.id)}
                          className={cn(
                            'rounded-full border px-4 py-1.5 text-xs uppercase tracking-wider transition-colors',
                            variant === item.id
                              ? 'border-foreground bg-foreground text-background'
                              : 'border-border text-muted-foreground hover:border-foreground/40 hover:text-foreground',
                          )}
                        >
                          {item.label}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : null}

                <Button
                  type="button"
                  size="lg"
                  className="mt-8 w-full rounded-full sm:w-auto"
                  disabled={!configured || status === 'processing'}
                  onClick={handleVisualize}
                >
                  Visualize My Space
                  <ArrowRight className="ml-1" />
                </Button>
                {!configured ? (
                  <p className="mt-3 text-sm text-muted-foreground">
                    Upload a photo and choose what you want to explore.
                  </p>
                ) : (
                  <p className="mt-3 text-sm text-muted-foreground">
                    This preview is a demonstration of the intended experience.
                  </p>
                )}
                {pipelinePhase === 'completed' ? (
                  <p className="mt-3 text-sm text-muted-foreground">Completed</p>
                ) : null}
                {saveNotice ? (
                  <div className="mt-4 max-w-xl" role="alert">
                    <p className="text-sm text-muted-foreground">{saveNotice}</p>
                    <button type="button" className="mt-3 text-sm tracking-wide" onClick={() => void retrySave()}>
                      Retry
                    </button>
                  </div>
                ) : null}
              </div>
            </div>

            {status === 'result' && source && (generatedUrl || (afterImage && currentSrc)) ? (
              <div className="mt-12 border-t border-border pt-10">
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
                  {generatedUrl ? 'Visualization' : 'Demonstration'}
                </p>
                <h3 className="mt-3 font-display text-2xl sm:text-3xl">Your space, then a possibility</h3>
                <p className="mt-3 max-w-xl text-sm leading-relaxed text-muted-foreground">
                  {generatedUrl
                    ? 'This visualization was prepared from your photograph.'
                    : 'This is demonstration content for the intended visualization — not a generated result from your photograph, and not a completed project.'}
                </p>

                <div className="mt-8 overflow-hidden rounded-md border border-border">
                  <div className="grid md:grid-cols-2">
                    <div className="relative">
                      <ArchitecturalImage
                        src={currentSrc ?? ''}
                        alt={previewAlt ?? beforeLabel}
                        aspect="video"
                        sizes="(max-width: 768px) 100vw, 50vw"
                        className={cn(
                          'grayscale-[15%] brightness-95',
                          source.kind === 'sample' && source.id === 'villa' && MARK_CROP,
                        )}
                      />
                      <span className="absolute left-3 top-3 rounded-full bg-background/90 px-3 py-1 text-[10px] uppercase tracking-[0.15em] text-muted-foreground backdrop-blur-sm">
                        Your space
                      </span>
                    </div>
                    <div className="relative border-t border-border md:border-l md:border-t-0">
                      {generatedUrl ? (
                        <div className="relative aspect-video overflow-hidden bg-stone-200">
                          {/* eslint-disable-next-line @next/next/no-img-element */}
                          <img src={generatedUrl} alt="Ecotech possibility" className="h-full w-full object-cover" />
                        </div>
                      ) : afterImage ? (
                        <ArchitecturalImage
                          src={afterImage.src}
                          alt={afterImage.alt}
                          aspect="video"
                          sizes="(max-width: 768px) 100vw, 50vw"
                        />
                      ) : null}
                      <span className="absolute left-3 top-3 rounded-full bg-foreground px-3 py-1 text-[10px] uppercase tracking-[0.15em] text-background">
                        Ecotech possibility
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Button type="button" variant="outline" className="rounded-full" onClick={handleReset}>
                    <X className="h-4 w-4" />
                    Start over
                  </Button>
                </div>
              </div>
            ) : null}
          </div>
        </FadeIn>
      </Container>
    </Section>
  );
}

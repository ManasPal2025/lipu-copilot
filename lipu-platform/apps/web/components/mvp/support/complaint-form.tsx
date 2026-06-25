'use client';

import { useEffect, useRef, useState } from 'react';
import { Camera, Loader2, X } from 'lucide-react';

import { ComplaintSuccess } from '@/components/mvp/support/complaint-success';
import { FadeIn } from '@/components/motion/fade-in';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  ISSUE_TYPES,
  PRODUCT_TYPES,
  saveComplaintLocally,
  type ComplaintSubmitResponse,
} from '@/lib/support-types';
import { cn } from '@/lib/utils';

const selectClassName =
  'flex h-12 w-full rounded-sm border border-input bg-background px-4 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';

export function ComplaintForm() {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<ComplaintSubmitResponse | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [formSnapshot, setFormSnapshot] = useState({
    productType: '',
    issueType: '',
    phone: '',
  });

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  function handleImageChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    if (previewUrl) URL.revokeObjectURL(previewUrl);

    setImageFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setError(null);
  }

  function clearImage() {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setImageFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    const form = e.currentTarget;
    const formData = new FormData(form);

    if (imageFile) {
      formData.set('image', imageFile);
    }

    const productType = String(formData.get('productType') ?? '');
    const issueType = String(formData.get('issueType') ?? '');
    const phone = String(formData.get('phone') ?? '');

    try {
      const res = await fetch('/api/support', {
        method: 'POST',
        body: formData,
      });

      const data = (await res.json()) as ComplaintSubmitResponse & { error?: string };

      if (!res.ok) {
        setError(data.error ?? 'Could not submit your message. Please try again.');
        return;
      }

      saveComplaintLocally({
        ticketNumber: data.ticketNumber,
        productType,
        issueType,
        createdAt: data.createdAt,
      });

      setFormSnapshot({ productType, issueType, phone });
      setResponse(data);
      form.reset();
      clearImage();
    } catch {
      setError('Network error. Check your connection and try again.');
    } finally {
      setSubmitting(false);
    }
  }

  function handleSubmitAnother() {
    setResponse(null);
    setError(null);
  }

  if (response) {
    return (
      <ComplaintSuccess
        response={response}
        productType={formSnapshot.productType}
        issueType={formSnapshot.issueType}
        phone={formSnapshot.phone}
        onSubmitAnother={handleSubmitAnother}
      />
    );
  }

  return (
    <FadeIn>
      <form
        onSubmit={handleSubmit}
        className="space-y-6 rounded-sm border border-border bg-card p-8 shadow-sm sm:p-10"
        aria-labelledby="support-form-title"
      >
        <div>
          <h2 id="support-form-title" className="font-display text-3xl">
            Tell us what went wrong
          </h2>
          <p className="mt-3 text-muted-foreground editorial-prose">
            We take every installation seriously. Share a few details and, if you can, a photo — our team will call
            you back within one business day.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="name" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Name
            </label>
            <Input id="name" name="name" autoComplete="name" required className="h-12" />
          </div>
          <div>
            <label htmlFor="phone" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Phone
            </label>
            <Input
              id="phone"
              name="phone"
              type="tel"
              autoComplete="tel"
              placeholder="+91 98765 43210"
              required
              className="h-12"
            />
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="productType" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Product type
            </label>
            <select id="productType" name="productType" className={selectClassName} defaultValue="" required>
              <option value="" disabled>
                Select product...
              </option>
              {PRODUCT_TYPES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="issueType" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Issue type
            </label>
            <select id="issueType" name="issueType" className={selectClassName} defaultValue="" required>
              <option value="" disabled>
                Select issue...
              </option>
              {ISSUE_TYPES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label htmlFor="description" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            Description
          </label>
          <Textarea
            id="description"
            name="description"
            placeholder="When did you notice the issue? Which room or opening is affected?"
            className="min-h-[140px]"
            required
            minLength={10}
          />
        </div>

        <div>
          <span className="mb-2 block text-xs font-medium uppercase tracking-wider">Upload image (optional)</span>
          <input
            ref={fileInputRef}
            id="image"
            name="image"
            type="file"
            accept="image/jpeg,image/png,image/webp"
            className="sr-only"
            onChange={handleImageChange}
          />

          {!previewUrl ? (
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className={cn(
                'flex w-full flex-col items-center justify-center rounded-sm border border-dashed border-border',
                'bg-muted/20 px-6 py-10 text-center transition-colors hover:border-foreground/30 hover:bg-muted/30',
              )}
            >
              <Camera className="h-8 w-8 text-muted-foreground" aria-hidden />
              <p className="mt-4 text-sm font-medium">Add a photo of the issue</p>
              <p className="mt-1 text-xs text-muted-foreground">JPG, PNG or WebP · Max 4 MB</p>
            </button>
          ) : (
            <div className="relative overflow-hidden rounded-sm border border-border">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={previewUrl} alt="Issue preview" className="max-h-64 w-full object-cover" />
              <Button
                type="button"
                variant="outline"
                size="icon"
                className="absolute right-3 top-3 bg-background/90"
                onClick={clearImage}
                aria-label="Remove photo"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          )}
        </div>

        {error && (
          <p className="text-sm text-destructive" role="alert">
            {error}
          </p>
        )}

        <Button type="submit" variant="accent" size="lg" disabled={submitting} className="w-full sm:w-auto">
          {submitting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Sending...
            </>
          ) : (
            'Submit support request'
          )}
        </Button>
      </form>
    </FadeIn>
  );
}

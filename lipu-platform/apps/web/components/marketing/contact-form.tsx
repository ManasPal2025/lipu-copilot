'use client';

import { useState } from 'react';
import { CheckCircle2, Clock, MessageSquare, Sparkles } from 'lucide-react';

import { useAccount } from '@/components/providers/account-provider';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { API_BASE_URL } from '@/lib/constants';

const steps = [
  { icon: MessageSquare, title: 'Share your vision', desc: 'Tell us about your home and what transformation means to you.' },
  { icon: Clock, title: 'Thoughtful response', desc: 'We reply within one business day — never a hard sell.' },
  { icon: Sparkles, title: 'Design consultation', desc: 'An in-studio or on-site conversation about light, space, and craft.' },
];

export function ContactForm() {
  const account = useAccount();
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (submitting) return;

    const form = e.currentTarget;
    const data = new FormData(form);
    const phone = String(data.get('phone') ?? '').trim();
    setError(null);
    setSubmitting(true);

    try {
      const token = await account.getToken();
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers.Authorization = `Bearer ${token}`;
      const response = await fetch(`${API_BASE_URL}/consultations`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          first_name: data.get('firstName'),
          last_name: data.get('lastName'),
          email: data.get('email'),
          phone: phone || null,
          city: data.get('city'),
          project_type: data.get('projectType'),
          message: data.get('message'),
        }),
      });
      if (!response.ok) {
        setError("We couldn't send your request. Please check the form and try again.");
        return;
      }
      setSubmitted(true);
    } catch {
      setError("We couldn't send your request. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (submitted) {
    return (
      <div className="flex flex-col items-center rounded-sm border border-border bg-muted/20 p-12 text-center sm:p-16">
        <CheckCircle2 className="h-14 w-14 text-accent" aria-hidden />
        <h2 className="mt-8 font-display text-3xl">Thank you</h2>
        <p className="mt-4 max-w-sm text-muted-foreground editorial-prose">
          Your consultation request has been received. Our team will respond within one business day with a thoughtful
          next step.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      <div className="grid gap-6 sm:grid-cols-3">
        {steps.map((step) => (
          <div key={step.title} className="border-t border-border pt-5">
            <step.icon className="h-5 w-5 text-accent" aria-hidden />
            <p className="mt-3 font-display text-lg">{step.title}</p>
            <p className="mt-2 text-sm text-muted-foreground">{step.desc}</p>
          </div>
        ))}
      </div>

      <form
        id="quote"
        key={account.user?.email ?? 'guest'}
        onSubmit={handleSubmit}
        className="space-y-6 rounded-sm border border-border bg-card p-8 shadow-sm sm:p-10"
        aria-labelledby="quote-form-title"
      >
        <div>
          <h2 id="quote-form-title" className="font-display text-3xl">
            Request a consultation
          </h2>
          <p className="mt-3 text-muted-foreground editorial-prose">
            Share your vision. No obligation — just an honest conversation about transformation.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="first-name" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              First name
            </label>
            <Input
              id="first-name"
              name="firstName"
              autoComplete="given-name"
              required
              className="h-12"
              defaultValue={account.user?.firstName ?? ''}
            />
          </div>
          <div>
            <label htmlFor="last-name" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Last name
            </label>
            <Input
              id="last-name"
              name="lastName"
              autoComplete="family-name"
              required
              className="h-12"
              defaultValue={account.user?.lastName ?? ''}
            />
          </div>
        </div>

        <div>
          <label htmlFor="email" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            Email
          </label>
          <Input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            className="h-12"
            defaultValue={account.user?.email ?? ''}
          />
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
            placeholder="+91"
            className="h-12"
            defaultValue={account.user?.phone ?? ''}
          />
        </div>

        <div>
          <label htmlFor="city" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            City / Project location
          </label>
          <Input id="city" name="city" required className="h-12" />
        </div>

        <div>
          <label htmlFor="project-type" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            Project type
          </label>
          <select
            id="project-type"
            name="projectType"
            className="flex h-12 w-full rounded-sm border border-input bg-background px-4 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            defaultValue=""
            required
          >
            <option value="" disabled>
              Select...
            </option>
            <option value="residential">Residential</option>
            <option value="renovation">Renovation</option>
            <option value="commercial">Commercial</option>
            <option value="architect">Architect / Designer</option>
          </select>
        </div>

        <div>
          <label htmlFor="message" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            Tell us about your home
          </label>
          <Textarea
            id="message"
            name="message"
            placeholder="What would transformation mean for your space?"
            className="min-h-[140px]"
            required
          />
        </div>

        {error ? (
          <p role="alert" className="text-sm text-muted-foreground">
            {error}
          </p>
        ) : null}

        <Button
          type="submit"
          variant="accent"
          size="lg"
          className="w-full tracking-wide sm:w-auto"
          disabled={submitting}
          aria-busy={submitting}
        >
          {submitting ? 'Sending request' : 'Submit request'}
        </Button>
      </form>
    </div>
  );
}

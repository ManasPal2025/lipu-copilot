'use client';

import { useState } from 'react';
import { CheckCircle2 } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

export function ContactForm() {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <div className="flex flex-col items-center rounded-sm border border-border p-10 text-center sm:p-12">
        <CheckCircle2 className="h-12 w-12 text-accent" aria-hidden />
        <h2 className="mt-6 font-display text-2xl">Thank you</h2>
        <p className="mt-3 max-w-sm text-muted-foreground">
          Your consultation request has been received. Our team will respond within one business day.
        </p>
      </div>
    );
  }

  return (
    <form
      id="quote"
      onSubmit={handleSubmit}
      className="space-y-6 rounded-sm border border-border p-6 sm:p-8"
      aria-labelledby="quote-form-title"
    >
      <div>
        <h2 id="quote-form-title" className="font-display text-2xl">
          Request a consultation
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Share your vision. No obligation — just an honest conversation about transformation.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="first-name" className="mb-2 block text-sm font-medium">
            First name
          </label>
          <Input id="first-name" name="firstName" autoComplete="given-name" required />
        </div>
        <div>
          <label htmlFor="last-name" className="mb-2 block text-sm font-medium">
            Last name
          </label>
          <Input id="last-name" name="lastName" autoComplete="family-name" required />
        </div>
      </div>

      <div>
        <label htmlFor="email" className="mb-2 block text-sm font-medium">
          Email
        </label>
        <Input id="email" name="email" type="email" autoComplete="email" required />
      </div>

      <div>
        <label htmlFor="phone" className="mb-2 block text-sm font-medium">
          Phone
        </label>
        <Input id="phone" name="phone" type="tel" autoComplete="tel" placeholder="+91" />
      </div>

      <div>
        <label htmlFor="city" className="mb-2 block text-sm font-medium">
          City / Project location
        </label>
        <Input id="city" name="city" required />
      </div>

      <div>
        <label htmlFor="project-type" className="mb-2 block text-sm font-medium">
          Project type
        </label>
        <select
          id="project-type"
          name="projectType"
          className="flex h-11 w-full rounded-sm border border-input bg-background px-4 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
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
        <label htmlFor="message" className="mb-2 block text-sm font-medium">
          Tell us about your home
        </label>
        <Textarea
          id="message"
          name="message"
          placeholder="What would transformation mean for your space?"
          required
        />
      </div>

      <Button type="submit" variant="accent" size="lg" className="w-full sm:w-auto">
        Submit request
      </Button>
    </form>
  );
}

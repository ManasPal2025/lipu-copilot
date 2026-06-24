'use client';

import { useState } from 'react';
import { CheckCircle2, Clock, MessageSquare, Sparkles } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

const steps = [
  { icon: MessageSquare, title: 'Share your vision', desc: 'Tell us about your home and what transformation means to you.' },
  { icon: Clock, title: 'Thoughtful response', desc: 'We reply within one business day — never a hard sell.' },
  { icon: Sparkles, title: 'Design consultation', desc: 'An in-studio or on-site conversation about light, space, and craft.' },
];

export function ContactForm() {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitted(true);
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
            <Input id="first-name" name="firstName" autoComplete="given-name" required className="h-12" />
          </div>
          <div>
            <label htmlFor="last-name" className="mb-2 block text-xs font-medium uppercase tracking-wider">
              Last name
            </label>
            <Input id="last-name" name="lastName" autoComplete="family-name" required className="h-12" />
          </div>
        </div>

        <div>
          <label htmlFor="email" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            Email
          </label>
          <Input id="email" name="email" type="email" autoComplete="email" required className="h-12" />
        </div>

        <div>
          <label htmlFor="phone" className="mb-2 block text-xs font-medium uppercase tracking-wider">
            Phone
          </label>
          <Input id="phone" name="phone" type="tel" autoComplete="tel" placeholder="+91" className="h-12" />
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

        <Button type="submit" variant="accent" size="lg" className="w-full tracking-wide sm:w-auto">
          Submit request
        </Button>
      </form>
    </div>
  );
}

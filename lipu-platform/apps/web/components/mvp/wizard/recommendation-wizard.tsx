'use client';

import { useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { RecommendationCard } from '@/components/mvp/wizard/recommendation-card';
import { StepProgress } from '@/components/mvp/wizard/step-progress';
import { WizardOption } from '@/components/mvp/wizard/wizard-option';
import { Button } from '@/components/ui/button';
import {
  getRecommendation,
  WIZARD_OPTIONS,
  WIZARD_STEPS,
  type BudgetRange,
  type HeatExposure,
  type NoiseLevel,
  type PropertyType,
  type RoomType,
  type WizardAnswers,
} from '@/lib/recommendation-engine';

type StepKey = keyof WizardAnswers;

const STEP_KEYS: StepKey[] = ['propertyType', 'roomType', 'noiseLevel', 'heatExposure', 'budget'];

const EMPTY_ANSWERS: Partial<WizardAnswers> = {};

export function RecommendationWizard() {
  const [stepIndex, setStepIndex] = useState(0);
  const [answers, setAnswers] = useState<Partial<WizardAnswers>>(EMPTY_ANSWERS);
  const [showResults, setShowResults] = useState(false);

  const currentStep = WIZARD_STEPS[stepIndex];
  const currentKey = STEP_KEYS[stepIndex];
  const currentValue = answers[currentKey];
  const isLastStep = stepIndex === WIZARD_STEPS.length - 1;

  const recommendation = useMemo(() => {
    if (!showResults || !isComplete(answers)) return null;
    return getRecommendation(answers);
  }, [answers, showResults]);

  function isComplete(value: Partial<WizardAnswers>): value is WizardAnswers {
    return STEP_KEYS.every((key) => value[key] !== undefined);
  }

  function handleSelect(value: WizardAnswers[StepKey]) {
    setAnswers((prev) => ({ ...prev, [currentKey]: value }));
  }

  function handleNext() {
    if (!currentValue) return;

    if (isLastStep) {
      setShowResults(true);
      return;
    }

    setStepIndex((prev) => prev + 1);
  }

  function handleBack() {
    if (showResults) {
      setShowResults(false);
      return;
    }
    setStepIndex((prev) => Math.max(0, prev - 1));
  }

  function handleStartOver() {
    setAnswers(EMPTY_ANSWERS);
    setStepIndex(0);
    setShowResults(false);
  }

  const options = WIZARD_OPTIONS[currentKey] as ReadonlyArray<{
    value: PropertyType | RoomType | NoiseLevel | HeatExposure | BudgetRange;
    label: string;
    description: string;
  }>;

  if (showResults && recommendation) {
    return (
      <FadeIn>
        <RecommendationCard recommendation={recommendation} onStartOver={handleStartOver} />
      </FadeIn>
    );
  }

  return (
    <div className="mx-auto max-w-2xl">
      <StepProgress
        current={stepIndex}
        total={WIZARD_STEPS.length}
        labels={WIZARD_STEPS.map((step) => step.title)}
      />

      <FadeIn key={currentStep.id}>
        <div className="mt-10">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Recommendation wizard</p>
          <h2 className="mt-3 font-display text-3xl sm:text-4xl">{currentStep.title}</h2>
          <p className="mt-4 text-muted-foreground editorial-prose">{currentStep.description}</p>
        </div>

        <div className="mt-8 space-y-3">
          {options.map((option) => (
            <WizardOption
              key={option.value}
              label={option.label}
              description={option.description}
              selected={currentValue === option.value}
              onSelect={() => handleSelect(option.value)}
            />
          ))}
        </div>

        <div className="mt-10 flex flex-wrap items-center justify-between gap-4 border-t border-border pt-8">
          <Button
            type="button"
            variant="ghost"
            onClick={handleBack}
            disabled={stepIndex === 0}
            className={stepIndex === 0 ? 'invisible' : undefined}
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Button>

          <Button type="button" variant="accent" onClick={handleNext} disabled={!currentValue}>
            {isLastStep ? 'See my recommendation' : 'Continue'}
            <ArrowRight className="h-4 w-4" />
          </Button>
        </div>
      </FadeIn>
    </div>
  );
}

import type { Metadata } from 'next';

import {
  TransformConsultation,
  TransformHero,
  TransformHowItWorks,
} from '@/components/marketing/transform-sections';
import { TransformWorkspace } from '@/components/marketing/transform-workspace';

export const metadata: Metadata = {
  title: 'Transform Your Space',
  description:
    'Upload a photo of your room, balcony, terrace, or facade and explore how Ecotech windows and doors could change it.',
};

export default function TransformPage() {
  return (
    <>
      <TransformHero />
      <TransformHowItWorks />
      <TransformWorkspace />
      <TransformConsultation />
    </>
  );
}

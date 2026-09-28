import type { Metadata } from 'next';

import {
  ServicesCommercial,
  ServicesConsultation,
  ServicesHero,
  ServicesHospitality,
  ServicesIntro,
  ServicesProcess,
  ServicesResidential,
  ServicesWindowsDoors,
} from '@/components/marketing/services-sections';

export const metadata: Metadata = {
  title: 'Services',
  description:
    'Architectural windows, doors, and space transformations — residential, commercial, and hospitality projects across Odisha.',
};

export default function ServicesPage() {
  return (
    <>
      <ServicesHero />
      <ServicesIntro />
      <ServicesWindowsDoors />
      <ServicesResidential />
      <ServicesCommercial />
      <ServicesHospitality />
      <ServicesProcess />
      <ServicesConsultation />
    </>
  );
}

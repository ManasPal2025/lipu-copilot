import type { Metadata } from 'next';

import {
  ProductsArchitectural,
  ProductsConsultation,
  ProductsCustom,
  ProductsDoors,
  ProductsHero,
  ProductsIntro,
  ProductsWindows,
} from '@/components/marketing/products-sections';

export const metadata: Metadata = {
  title: 'Products',
  description:
    'Window, door, and architectural glazing systems from Ecotech Window Systems — designed around how you live.',
};

export default function ProductsPage() {
  return (
    <>
      <ProductsHero />
      <ProductsIntro />
      <ProductsWindows />
      <ProductsDoors />
      <ProductsArchitectural />
      <ProductsCustom />
      <ProductsConsultation />
    </>
  );
}

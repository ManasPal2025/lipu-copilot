import pricingRules from '@/config/pricing-rules.json';

export interface PricingWindowType {
  id: string;
  label: string;
  description: string;
  baseRatePerSqFt: number;
  productSlug: string;
}

export interface PricingGlassType {
  id: string;
  label: string;
  description: string;
  modifier: number;
}

export interface PricingRules {
  currency: string;
  currencySymbol: string;
  dimensionUnit: string;
  areaUnit: string;
  gstRate: number;
  disclaimer: string;
  installation: {
    flatRate: number;
    perSqFt: number;
    label: string;
  };
  rangeVariance: {
    minFactor: number;
    maxFactor: number;
  };
  windowTypes: PricingWindowType[];
  glassTypes: PricingGlassType[];
}

export interface EstimateInput {
  width: number;
  height: number;
  windowTypeId: string;
  glassTypeId: string;
}

export interface EstimateLineItem {
  label: string;
  amount: number;
  detail?: string;
}

export interface EstimateResult {
  area: number;
  windowType: PricingWindowType;
  glassType: PricingGlassType;
  lineItems: EstimateLineItem[];
  subtotal: number;
  gst: number;
  total: number;
  minTotal: number;
  maxTotal: number;
  disclaimer: string;
}

export const rules = pricingRules as PricingRules;

export function getWindowType(id: string): PricingWindowType | undefined {
  return rules.windowTypes.find((type) => type.id === id);
}

export function getGlassType(id: string): PricingGlassType | undefined {
  return rules.glassTypes.find((type) => type.id === id);
}

export function formatInr(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: rules.currency,
    maximumFractionDigits: 0,
  }).format(Math.round(amount));
}

export function calculateEstimate(input: EstimateInput): EstimateResult | null {
  const { width, height, windowTypeId, glassTypeId } = input;

  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
    return null;
  }

  const windowType = getWindowType(windowTypeId);
  const glassType = getGlassType(glassTypeId);

  if (!windowType || !glassType) {
    return null;
  }

  const area = width * height;
  const materialRate = windowType.baseRatePerSqFt * glassType.modifier;
  const materialCost = area * materialRate;
  const installationCost = rules.installation.flatRate + area * rules.installation.perSqFt;
  const subtotal = materialCost + installationCost;
  const gst = subtotal * rules.gstRate;
  const total = subtotal + gst;

  const lineItems: EstimateLineItem[] = [
    {
      label: `${windowType.label} (${area.toFixed(1)} ${rules.areaUnit})`,
      amount: materialCost,
      detail: `${formatInr(materialRate)} per ${rules.areaUnit} incl. ${glassType.label.toLowerCase()}`,
    },
    {
      label: rules.installation.label,
      amount: installationCost,
      detail: `${formatInr(rules.installation.flatRate)} base + ${formatInr(rules.installation.perSqFt)}/${rules.areaUnit}`,
    },
    {
      label: `GST (${Math.round(rules.gstRate * 100)}%)`,
      amount: gst,
    },
  ];

  return {
    area,
    windowType,
    glassType,
    lineItems,
    subtotal,
    gst,
    total,
    minTotal: total * rules.rangeVariance.minFactor,
    maxTotal: total * rules.rangeVariance.maxFactor,
    disclaimer: rules.disclaimer,
  };
}

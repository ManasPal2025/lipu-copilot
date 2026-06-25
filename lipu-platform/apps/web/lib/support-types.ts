export const PRODUCT_TYPES = [
  { value: 'sliding-window', label: 'Sliding Window' },
  { value: 'casement-window', label: 'Casement Window' },
  { value: 'fixed-window', label: 'Fixed Window' },
  { value: 'french-door', label: 'French Door' },
  { value: 'sliding-door', label: 'Sliding Door' },
  { value: 'other', label: 'Other / Not sure' },
] as const;

export const ISSUE_TYPES = [
  { value: 'installation', label: 'Installation issue' },
  { value: 'glass-seal', label: 'Glass or seal problem' },
  { value: 'hardware', label: 'Hardware or locking' },
  { value: 'water-leakage', label: 'Water leakage' },
  { value: 'noise-draft', label: 'Noise or draft' },
  { value: 'warranty', label: 'Warranty request' },
  { value: 'other', label: 'Something else' },
] as const;

export type ProductType = (typeof PRODUCT_TYPES)[number]['value'];
export type IssueType = (typeof ISSUE_TYPES)[number]['value'];

export interface ComplaintImageMeta {
  name: string;
  type: string;
  size: number;
}

export interface ComplaintRecord {
  id: string;
  ticketNumber: string;
  name: string;
  phone: string;
  productType: string;
  issueType: string;
  description: string;
  image?: ComplaintImageMeta;
  createdAt: string;
}

export interface ComplaintSubmitResponse {
  ticketNumber: string;
  message: string;
  createdAt: string;
}

export const LOCAL_STORAGE_KEY = 'lipu-support-submissions';

export interface LocalComplaintSummary {
  ticketNumber: string;
  productType: string;
  issueType: string;
  createdAt: string;
}

export function saveComplaintLocally(summary: LocalComplaintSummary): void {
  if (typeof window === 'undefined') return;

  try {
    const existing = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) ?? '[]') as LocalComplaintSummary[];
    const updated = [summary, ...existing].slice(0, 5);
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
  } catch {
    // Ignore storage errors in mock flow
  }
}

export function getProductLabel(value: string): string {
  return PRODUCT_TYPES.find((item) => item.value === value)?.label ?? value;
}

export function getIssueLabel(value: string): string {
  return ISSUE_TYPES.find((item) => item.value === value)?.label ?? value;
}

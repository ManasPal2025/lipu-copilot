import { randomUUID } from 'crypto';

import type { ComplaintRecord } from '@/lib/support-types';

const globalStore = globalThis as unknown as {
  lipuSupportComplaints?: ComplaintRecord[];
};

function getComplaints(): ComplaintRecord[] {
  if (!globalStore.lipuSupportComplaints) {
    globalStore.lipuSupportComplaints = [];
  }
  return globalStore.lipuSupportComplaints;
}

function generateTicketNumber(): string {
  const suffix = Date.now().toString(36).toUpperCase().slice(-5);
  return `LIPU-${suffix}`;
}

export function addComplaint(
  input: Omit<ComplaintRecord, 'id' | 'ticketNumber' | 'createdAt'>,
): ComplaintRecord {
  const record: ComplaintRecord = {
    id: randomUUID(),
    ticketNumber: generateTicketNumber(),
    createdAt: new Date().toISOString(),
    ...input,
  };

  getComplaints().unshift(record);
  return record;
}

export function listComplaints(): ComplaintRecord[] {
  return [...getComplaints()];
}

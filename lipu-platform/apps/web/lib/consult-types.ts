import type { ChatSource, ConfidenceLevel } from '@/lib/rag-query';

export type ChatRole = 'user' | 'assistant';

export type ChatMessage = {
  id: string;
  role: ChatRole;
  content: string;
  sources?: ChatSource[];
  confidence?: ConfidenceLevel;
};

export type ChatResponse = {
  answer: string;
  sources: ChatSource[];
  confidence: ConfidenceLevel;
};

export const SUGGESTED_QUESTIONS = [
  'Which window is best for my balcony?',
  'Is double glazing worth it in Bhubaneswar?',
  'Which glass for a west-facing bedroom?',
  'How much noise reduction near NH16?',
] as const;

import { NextResponse } from 'next/server';

import { runRagQuery } from '@/lib/rag-query';

const MIN_QUESTION_LENGTH = 5;
const MAX_QUESTION_LENGTH = 500;

const GENERIC_ANSWER =
  "We're having trouble answering right now. Please try again in a moment, or request a consultation and our team will help you directly.";

export async function POST(request: Request) {
  let question = '';

  try {
    const body = (await request.json()) as { question?: string };
    question = String(body.question ?? '').trim();

    if (!question || question.length < MIN_QUESTION_LENGTH) {
      return NextResponse.json(
        { error: `Please enter a question of at least ${MIN_QUESTION_LENGTH} characters.` },
        { status: 400 },
      );
    }

    if (question.length > MAX_QUESTION_LENGTH) {
      return NextResponse.json(
        { error: `Question must be ${MAX_QUESTION_LENGTH} characters or fewer.` },
        { status: 400 },
      );
    }

    const result = await runRagQuery(question);

    return NextResponse.json({
      question: result.question,
      answer: result.answer?.trim() || GENERIC_ANSWER,
      fallback: result.fallback,
      confidence: result.confidence,
      mode: result.mode,
      sources: result.sources,
    });
  } catch (error) {
    console.error('[api/consult] unexpected error:', error);
    return NextResponse.json({
      question,
      answer: GENERIC_ANSWER,
      fallback: true,
      confidence: 'Low',
      mode: 'fallback',
      sources: [],
    });
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    message: 'POST JSON { "question": "..." } for UPVC consultant answers.',
  });
}

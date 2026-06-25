import { NextResponse } from 'next/server';

import { getRagServerEndpoints, runRagQuery } from '@/lib/rag-query';

const MIN_QUESTION_LENGTH = 5;
const MAX_QUESTION_LENGTH = 500;

const GENERIC_ANSWER =
  "We're having trouble answering right now. Please try again in a moment, or request a consultation and our team will help you directly.";

export async function POST(request: Request) {
  console.log('[CHAT API] Request received');

  let question = '';

  try {
    const body = (await request.json()) as { question?: string };
    question = String(body.question ?? '').trim();

    console.log('[CHAT API] Question length =', question.length);

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

    const endpoints = getRagServerEndpoints();
    console.log('[CHAT API] RAG endpoints =', endpoints);

    const result = await runRagQuery(question);

    console.log('[CHAT API] Result mode =', result.mode, 'sources =', result.sources.length);
    console.log('[CHAT API] Answer preview =', result.answer.slice(0, 80));

    return NextResponse.json({
      answer: result.answer?.trim() || GENERIC_ANSWER,
      sources: result.sources,
      confidence: result.confidence,
      mode: result.mode,
    });
  } catch (error) {
    console.error('[CHAT API] unexpected error:', error);
    return NextResponse.json({
      answer: GENERIC_ANSWER,
      sources: [],
      confidence: 'Low',
      mode: 'retrieval',
    });
  }
}

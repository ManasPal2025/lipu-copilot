'use client';

import { useEffect, useRef, useState } from 'react';
import { Loader2, MessageCircle, SendHorizonal, Sparkles } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import type { ConfidenceLevel } from '@/lib/rag-query';
import { SUGGESTED_QUESTIONS, type ChatMessage, type ChatResponse } from '@/lib/consult-types';
import { cn } from '@/lib/utils';

function createUserMessage(content: string): ChatMessage {
  return { id: crypto.randomUUID(), role: 'user', content };
}

function createAssistantMessage(data: ChatResponse): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role: 'assistant',
    content: data.answer,
    sources: data.sources,
    confidence: data.confidence,
  };
}

export function ConsultChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  async function sendQuestion(question: string) {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    setError(null);
    setInput('');
    setMessages((prev) => [...prev, createUserMessage(trimmed)]);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed }),
      });

      const data = (await res.json()) as ChatResponse & { error?: string };

      if (!res.ok) {
        throw new Error(data.error ?? 'Something went wrong. Please try again.');
      }

      if (!data.answer) {
        throw new Error('No answer received. Please try again.');
      }

      setMessages((prev) => [
        ...prev,
        createAssistantMessage({
          answer: data.answer,
          sources: data.sources ?? [],
          confidence: data.confidence ?? 'Low',
        }),
      ]);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
      setError(message);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    void sendQuestion(input);
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void sendQuestion(input);
    }
  }

  const hasHistory = messages.length > 0;

  return (
    <FadeIn>
      <div className="overflow-hidden rounded-sm border border-border bg-background shadow-sm">
        <div
          className="flex max-h-[min(520px,60vh)] min-h-[320px] flex-col gap-4 overflow-y-auto px-5 py-6 sm:px-6"
          aria-live="polite"
          aria-label="Chat messages"
        >
          {!hasHistory && !loading && (
            <div className="my-auto text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-accent/10">
                <Sparkles className="h-5 w-5 text-accent" aria-hidden />
              </div>
              <p className="mt-4 font-display text-xl">Ask about windows &amp; doors</p>
              <p className="mt-2 text-sm text-muted-foreground editorial-prose">
                Practical guidance for UPVC systems in Bhubaneswar and Odisha — glass, noise, heat, and monsoon
                performance.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-2">
                {SUGGESTED_QUESTIONS.map((question) => (
                  <button
                    key={question}
                    type="button"
                    onClick={() => void sendQuestion(question)}
                    className="rounded-sm border border-border bg-muted/40 px-3 py-2 text-left text-xs text-muted-foreground transition-colors hover:border-accent/40 hover:bg-accent/5 hover:text-foreground"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message) => (
            <ChatBubble key={message.id} message={message} />
          ))}

          {loading && (
            <div className="flex gap-3">
              <AssistantAvatar />
              <div className="flex max-w-[85%] items-center gap-2 rounded-sm border border-border bg-muted/30 px-4 py-3 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 shrink-0 animate-spin text-accent" aria-hidden />
                <span>Thinking…</span>
              </div>
            </div>
          )}

          <div ref={scrollRef} />
        </div>

        {error && (
          <div className="border-t border-destructive/20 bg-destructive/5 px-5 py-3 text-sm text-destructive sm:px-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="border-t border-border bg-muted/10 p-4 sm:p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <Textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about glazing, noise, ventilation, cyclone safety…"
              disabled={loading}
              rows={2}
              className="min-h-[72px] resize-none sm:flex-1"
              aria-label="Your question"
            />
            <Button
              type="submit"
              variant="accent"
              disabled={loading || input.trim().length < 5}
              className="shrink-0 sm:h-11"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Sending
                </>
              ) : (
                <>
                  <SendHorizonal className="h-4 w-4" />
                  Ask
                </>
              )}
            </Button>
          </div>
          <p className="mt-2 text-xs text-muted-foreground">
            Enter to send · Shift+Enter for a new line · Answers are for guidance only — not a formal quote
          </p>
        </form>
      </div>
    </FadeIn>
  );
}

function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user';

  return (
    <div className={cn('flex gap-3', isUser && 'flex-row-reverse')}>
      {isUser ? (
        <div
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground"
          aria-hidden
        >
          <MessageCircle className="h-4 w-4" />
        </div>
      ) : (
        <AssistantAvatar />
      )}

      <div className={cn('max-w-[85%]', isUser && 'flex flex-col items-end')}>
        <div
          className={cn(
            'rounded-sm px-4 py-3 text-sm leading-relaxed',
            isUser
              ? 'bg-primary text-primary-foreground'
              : 'border border-border bg-muted/30 text-foreground editorial-prose whitespace-pre-wrap',
          )}
        >
          {message.content}
        </div>

        {!isUser && (message.confidence || (message.sources && message.sources.length > 0)) && (
          <AssistantMeta confidence={message.confidence} sources={message.sources ?? []} />
        )}
      </div>
    </div>
  );
}

function AssistantMeta({
  confidence,
  sources,
}: {
  confidence?: ConfidenceLevel;
  sources: NonNullable<ChatMessage['sources']>;
}) {
  return (
    <div className="mt-2 w-full space-y-2 px-1">
      {confidence && (
        <p className="text-xs text-muted-foreground">
          Confidence:{' '}
          <span className={cn('font-medium', confidenceStyles(confidence))}>{confidence}</span>
        </p>
      )}

      {sources.length > 0 && (
        <div className="border-t border-border/60 pt-2">
          <p className="text-xs font-medium uppercase tracking-[0.12em] text-muted-foreground">Sources</p>
          <ul className="mt-1.5 space-y-1">
            {sources.map((source) => (
              <li key={source.id ?? source.name} className="flex gap-2 text-xs text-muted-foreground">
                <span className="text-accent" aria-hidden>
                  •
                </span>
                <span>{source.name}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function confidenceStyles(level: ConfidenceLevel): string {
  switch (level) {
    case 'High':
      return 'text-emerald-600 dark:text-emerald-400';
    case 'Medium':
      return 'text-amber-600 dark:text-amber-400';
    default:
      return 'text-muted-foreground';
  }
}

function AssistantAvatar() {
  return (
    <div
      className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent/15 text-accent"
      aria-hidden
    >
      <Sparkles className="h-4 w-4" />
    </div>
  );
}

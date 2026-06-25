import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export type ConfidenceLevel = 'High' | 'Medium' | 'Low';
export type AIConfigMode = 'retrieval' | 'gemini';
export type AIMode = 'retrieval' | 'gemini' | 'fallback' | 'disabled';

export type ChatSource = {
  name: string;
  id?: string;
};

export type ConsultSource = ChatSource & {
  label?: string;
  title?: string;
  section?: string;
  category?: string;
  score?: number;
};

export type ConsultResponse = {
  question: string;
  answer: string;
  fallback: boolean;
  confidence: ConfidenceLevel;
  mode: AIMode;
  sources: ChatSource[];
};

export type AIConfig = {
  enabled: boolean;
  mode: AIConfigMode;
};

const GENERIC_ANSWER =
  "We're having trouble answering right now. Please try again in a moment, or request a consultation and our team will help you directly.";

const CONSULTATION_FALLBACK_ANSWER =
  'AI consultant is temporarily unavailable. Please request a free consultation and our team will assist you.';

function isProductionEnv(): boolean {
  return process.env.VERCEL === '1' || process.env.NODE_ENV === 'production';
}

function parseBool(value: string | undefined, defaultValue: boolean): boolean {
  if (value === undefined || value.trim() === '') {
    return defaultValue;
  }
  const normalized = value.trim().toLowerCase();
  if (normalized === 'true' || normalized === '1' || normalized === 'yes') {
    return true;
  }
  if (normalized === 'false' || normalized === '0' || normalized === 'no') {
    return false;
  }
  return defaultValue;
}

/** Feature flags — local defaults AI on; production defaults AI off when unset. */
export function resolveAIConfig(): AIConfig {
  const enabled = parseBool(process.env.AI_ENABLED, !isProductionEnv());
  const rawMode = process.env.AI_MODE?.trim().toLowerCase();
  const mode: AIConfigMode = rawMode === 'gemini' ? 'gemini' : 'retrieval';
  return { enabled, mode };
}

function logEnv(ai: AIConfig): void {
  console.log(`[RAG] ENV=${isProductionEnv() ? 'production' : 'development'}`);
  console.log(`[RAG] AI_ENABLED=${ai.enabled}`);
  console.log(`[RAG] AI_MODE=${ai.mode}`);
  console.log('[RAG] RAG_SERVER_URL=', process.env.RAG_SERVER_URL ?? '(not set)');
}

/** Resolved lazily — only needed for local subprocess fallback. */
function resolveRagRoot(): string {
  const fromEnv = process.env.RAG_ROOT?.trim();
  if (fromEnv && existsSync(path.join(fromEnv, 'server.py'))) {
    return path.resolve(fromEnv);
  }

  const fromFile = path.resolve(
    path.dirname(fileURLToPath(import.meta.url)),
    '..',
    '..',
    '..',
    'rag',
  );
  if (existsSync(path.join(fromFile, 'server.py'))) {
    return fromFile;
  }

  const fromCwdAppsWeb = path.resolve(process.cwd(), '..', '..', 'rag');
  if (existsSync(path.join(fromCwdAppsWeb, 'server.py'))) {
    return fromCwdAppsWeb;
  }

  const fromCwdPlatform = path.resolve(process.cwd(), 'rag');
  if (existsSync(path.join(fromCwdPlatform, 'server.py'))) {
    return fromCwdPlatform;
  }

  return fromFile;
}

let ragRootCache: string | null = null;

function getRagRoot(): string {
  if (!ragRootCache) {
    ragRootCache = resolveRagRoot();
  }
  return ragRootCache;
}

function resolveRagServerUrl(): string | null {
  const fromEnv = process.env.RAG_SERVER_URL?.trim();
  if (fromEnv) {
    return fromEnv.replace(/\/$/, '');
  }
  if (isProductionEnv()) {
    return null;
  }
  return 'http://127.0.0.1:8100';
}

function pythonExecutable(ragRoot: string): string {
  return process.platform === 'win32'
    ? path.join(ragRoot, '.venv', 'Scripts', 'python.exe')
    : path.join(ragRoot, '.venv', 'bin', 'python');
}

function normalizeConfidence(value: unknown): ConfidenceLevel {
  if (value === 'High' || value === 'Medium' || value === 'Low') {
    return value;
  }
  return 'Low';
}

function normalizeMode(value: unknown): AIMode {
  if (value === 'gemini') {
    return 'gemini';
  }
  if (value === 'fallback') {
    return 'fallback';
  }
  if (value === 'disabled') {
    return 'disabled';
  }
  return 'retrieval';
}

function normalizeSources(value: unknown): ChatSource[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .map((item) => {
      if (typeof item === 'string') {
        return { name: item };
      }
      if (item && typeof item === 'object' && 'name' in item && typeof item.name === 'string') {
        return {
          name: item.name,
          id: typeof item.id === 'string' ? item.id : undefined,
        };
      }
      return null;
    })
    .filter((item): item is ChatSource => item !== null);
}

function parsePayload(parsed: Partial<ConsultResponse>, question: string): ConsultResponse {
  if (typeof parsed.answer === 'string' && parsed.answer.trim()) {
    return {
      question: parsed.question ?? question,
      answer: parsed.answer,
      fallback: parsed.fallback ?? false,
      confidence: normalizeConfidence(parsed.confidence),
      mode: normalizeMode(parsed.mode),
      sources: normalizeSources(parsed.sources),
    };
  }

  return genericResponse(question);
}

function genericResponse(question: string): ConsultResponse {
  return {
    question,
    answer: GENERIC_ANSWER,
    fallback: true,
    confidence: 'Low',
    mode: 'fallback',
    sources: [],
  };
}

function disabledResponse(question: string): ConsultResponse {
  console.log('[RAG] AI disabled - returning fallback');
  return {
    question,
    answer: CONSULTATION_FALLBACK_ANSWER,
    fallback: true,
    confidence: 'Low',
    mode: 'disabled',
    sources: [],
  };
}

function productionFallbackResponse(question: string): ConsultResponse {
  console.log('[RAG] Production fallback activated');
  return {
    question,
    answer: CONSULTATION_FALLBACK_ANSWER,
    fallback: true,
    confidence: 'Low',
    mode: 'fallback',
    sources: [],
  };
}

async function runRagQueryHttp(serverUrl: string, question: string): Promise<ConsultResponse> {
  const queryUrl = `${serverUrl}/query`;

  console.log('[RAG] Using HTTP endpoint');
  console.log('[RAG QUERY] Exact URL =', queryUrl);

  const response = await fetch(queryUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
    cache: 'no-store',
  });

  console.log('[RAG QUERY] Response =', response.status);

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new Error(`RAG server responded with ${response.status}${body ? `: ${body.slice(0, 200)}` : ''}`);
  }

  const parsed = (await response.json()) as Partial<ConsultResponse>;
  console.log('[RAG QUERY] HTTP success — mode =', parsed.mode, 'sources =', parsed.sources?.length ?? 0);
  return parsePayload(parsed, question);
}

function runRagQuerySpawn(question: string): Promise<ConsultResponse> {
  if (isProductionEnv()) {
    return Promise.resolve(productionFallbackResponse(question));
  }

  console.log('[RAG] Using subprocess fallback');

  const ragRoot = getRagRoot();
  const python = pythonExecutable(ragRoot);
  const script = path.join(ragRoot, 'query_json.py');

  console.log('[RAG QUERY] RAG_ROOT =', ragRoot);
  console.log('[RAG QUERY] Python =', python);

  return new Promise((resolve) => {
    if (!existsSync(python)) {
      console.error('[RAG QUERY] Error = Python executable not found at', python);
      resolve(genericResponse(question));
      return;
    }

    const child = spawn(python, [script, question], {
      cwd: ragRoot,
      env: process.env,
      windowsHide: true,
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk: Buffer) => {
      stdout += chunk.toString('utf8');
    });

    child.stderr.on('data', (chunk: Buffer) => {
      stderr += chunk.toString('utf8');
    });

    child.on('error', (error) => {
      console.error('[RAG QUERY] Error =', error);
      resolve(genericResponse(question));
    });

    child.on('close', (code) => {
      if (stderr.trim()) {
        console.error('[RAG QUERY] subprocess stderr:', stderr.trim().slice(0, 500));
      }

      if (code !== 0) {
        console.error('[RAG QUERY] Error = subprocess exit code', code);
        resolve(genericResponse(question));
        return;
      }

      try {
        const result = parsePayload(JSON.parse(stdout) as Partial<ConsultResponse>, question);
        console.log('[RAG QUERY] Subprocess success — mode =', result.mode, 'sources =', result.sources.length);
        resolve(result);
      } catch (error) {
        console.error('[RAG QUERY] Error = invalid subprocess JSON', error);
        resolve(genericResponse(question));
      }
    });
  });
}

async function runRagQueryWithBackend(question: string): Promise<ConsultResponse> {
  const serverUrl = resolveRagServerUrl();

  if (isProductionEnv()) {
    if (!serverUrl) {
      return productionFallbackResponse(question);
    }

    try {
      return await runRagQueryHttp(serverUrl, question);
    } catch (error) {
      console.error('[RAG QUERY] Error =', error);
      return productionFallbackResponse(question);
    }
  }

  const localUrl = serverUrl ?? 'http://127.0.0.1:8100';

  try {
    return await runRagQueryHttp(localUrl, question);
  } catch (error) {
    console.error('[RAG QUERY] Error =', error);
    return runRagQuerySpawn(question);
  }
}

export async function runRagQuery(question: string): Promise<ConsultResponse> {
  const ai = resolveAIConfig();
  logEnv(ai);

  if (!ai.enabled) {
    return disabledResponse(question);
  }

  if (ai.mode === 'gemini') {
    console.log('[RAG] Gemini mode');
  } else {
    console.log('[RAG] Retrieval mode');
  }

  return runRagQueryWithBackend(question);
}

/** For debugging — direct RAG server URLs. */
export function getRagServerEndpoints() {
  const ai = resolveAIConfig();
  const serverUrl = ai.enabled ? resolveRagServerUrl() : null;
  return {
    health: serverUrl ? `${serverUrl}/health` : null,
    query: serverUrl ? `${serverUrl}/query` : null,
    serverBase: serverUrl,
    ragRoot: isProductionEnv() || !ai.enabled ? null : getRagRoot(),
    aiEnabled: ai.enabled,
    aiMode: ai.mode,
  };
}

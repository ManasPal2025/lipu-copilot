import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export type ConfidenceLevel = 'High' | 'Medium' | 'Low';
export type AIMode = 'retrieval' | 'gemini';

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

const GENERIC_ANSWER =
  "We're having trouble answering right now. Please try again in a moment, or request a consultation and our team will help you directly.";

/** Resolved once at module load — not dependent on process.cwd() alone. */
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

function resolveRagServerUrl(): string {
  const fromEnv = process.env.RAG_SERVER_URL?.trim();
  if (fromEnv) {
    return fromEnv.replace(/\/$/, '');
  }
  return 'http://127.0.0.1:8100';
}

const RAG_ROOT = resolveRagRoot();
const RAG_SERVER_URL = resolveRagServerUrl();
const RAG_QUERY_URL = `${RAG_SERVER_URL}/query`;
const RAG_HEALTH_URL = `${RAG_SERVER_URL}/health`;

function pythonExecutable(): string {
  return process.platform === 'win32'
    ? path.join(RAG_ROOT, '.venv', 'Scripts', 'python.exe')
    : path.join(RAG_ROOT, '.venv', 'bin', 'python');
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
    mode: 'retrieval',
    sources: [],
  };
}

async function runRagQueryHttp(question: string): Promise<ConsultResponse> {
  console.log('[RAG QUERY] URL =', RAG_SERVER_URL);
  console.log('[RAG QUERY] Endpoint = POST /query');
  console.log('[RAG QUERY] Exact URL =', RAG_QUERY_URL);
  console.log('[RAG QUERY] Calling RAG server');

  const response = await fetch(RAG_QUERY_URL, {
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
  console.log('[RAG QUERY] Fallback path = subprocess spawn');
  console.log('[RAG QUERY] RAG_ROOT =', RAG_ROOT);
  console.log('[RAG QUERY] Python =', pythonExecutable());

  return new Promise((resolve) => {
    const python = pythonExecutable();
    const script = path.join(RAG_ROOT, 'query_json.py');

    if (!existsSync(python)) {
      console.error('[RAG QUERY] Error = Python executable not found at', python);
      resolve(genericResponse(question));
      return;
    }

    const child = spawn(python, [script, question], {
      cwd: RAG_ROOT,
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

export async function runRagQuery(question: string): Promise<ConsultResponse> {
  console.log('[RAG QUERY] RAG_ROOT =', RAG_ROOT);
  console.log('[RAG QUERY] process.cwd() =', process.cwd());
  console.log('[RAG QUERY] RAG_SERVER_URL env =', JSON.stringify(process.env.RAG_SERVER_URL ?? null));

  try {
    return await runRagQueryHttp(question);
  } catch (error) {
    console.error('[RAG QUERY] Error =', error);
    console.log('[RAG QUERY] HTTP failed — executing subprocess fallback');
    return runRagQuerySpawn(question);
  }
}

/** For debugging — direct RAG server URLs. */
export function getRagServerEndpoints() {
  return {
    health: RAG_HEALTH_URL,
    query: RAG_QUERY_URL,
    serverBase: RAG_SERVER_URL,
    ragRoot: RAG_ROOT,
  };
}

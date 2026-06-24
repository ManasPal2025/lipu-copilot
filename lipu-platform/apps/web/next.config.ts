import type { NextConfig } from 'next';
import path from 'node:path';

const projectRoot = __dirname;
const monorepoRoot = path.join(projectRoot, '../..');
const isVercel = process.env.VERCEL === '1';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  output: 'standalone',
  // Monorepo tracing for Docker; skip on Vercel (root dir is apps/web, parent paths need dashboard toggle)
  ...(!isVercel ? { outputFileTracingRoot: monorepoRoot } : {}),
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': projectRoot,
    };
    return config;
  },
  turbopack: {
    resolveAlias: {
      '@': projectRoot,
    },
  },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.lipu.com' },
      { protocol: 'http', hostname: 'localhost' },
    ],
  },
};

export default nextConfig;

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
  env: {
    NEXT_PUBLIC_CLERK_SIGN_IN_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL ?? '/sign-in',
    NEXT_PUBLIC_CLERK_SIGN_UP_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL ?? '/sign-up',
    NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL: process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL ?? '/profile',
    NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL: process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL ?? '/profile',
  },
  async headers() {
    const securityHeaders = [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
      { key: 'X-Frame-Options', value: 'DENY' },
    ];
    if (process.env.NODE_ENV === 'production') {
      securityHeaders.push({
        key: 'Strict-Transport-Security',
        value: 'max-age=63072000; includeSubDomains',
      });
    }
    return [{ source: '/:path*', headers: securityHeaders }];
  },
  images: {
    qualities: [75, 85, 90],
    deviceSizes: [640, 828, 1080, 1200, 1920, 2048, 2560, 3840],
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.lipu.com' },
      { protocol: 'http', hostname: 'localhost' },
    ],
  },
};

export default nextConfig;

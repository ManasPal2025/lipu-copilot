import type { NextConfig } from 'next';
import path from 'node:path';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  output: 'standalone',
  // Trace dependencies from monorepo root (required for workspace installs)
  outputFileTracingRoot: path.join(__dirname, '../..'),
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.lipu.com' },
      { protocol: 'http', hostname: 'localhost' },
    ],
  },
};

export default nextConfig;

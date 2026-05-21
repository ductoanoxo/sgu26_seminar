import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable polling for hot reload to work inside Docker on Windows
  // Without this, Next.js won't detect file changes via WSL2 volume mounts
  // NOTE: Do NOT add turbopack: {} here — it overrides webpack and breaks polling
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 1000,          // Check for changes every 1 second
        aggregateTimeout: 300, // Delay rebuild after first change
      };
    }
    return config;
  },
};

export default nextConfig;

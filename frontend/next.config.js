// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || '',
  images: {
    unoptimized: true,
  },
  // Remove assetPrefix as it's redundant with basePath
  webpack: (config) => {
    config.module.rules.push({
      test: /\.ya?ml$/,
      use: 'raw-loader'
    });
    return config;
  },
  trailingSlash: true,
  // Add this to properly handle static file serving
  experimental: {
    // This gives better error messages during static export
    instrumentationHook: true
  }
}

module.exports = nextConfig

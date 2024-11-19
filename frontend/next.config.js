/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || '',
  images: {
    unoptimized: true,
  },
  assetPrefix: process.env.NEXT_PUBLIC_BASE_PATH || '',
  pageExtensions: ['ts', 'tsx', 'js', 'jsx'],
  webpack: (config) => {
    config.module.rules.push({
      test: /\.ya?ml$/,
      use: 'raw-loader'
    });
    return config;
  },
}

module.exports = {
  ...nextConfig,
  // Configure source directory
  experimental: {
    appDir: true,
  },
  // Tell Next.js to look for pages in src/pages
  dir: 'src',
}

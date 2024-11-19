/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || '',
  images: {
    unoptimized: true,
  },
  assetPrefix: process.env.NEXT_PUBLIC_BASE_PATH || '',
  webpack: (config) => {
    config.module.rules.push({
      test: /\.ya?ml$/,
      use: 'raw-loader'
    });
    return config;
  },
}

module.exports = nextConfig;

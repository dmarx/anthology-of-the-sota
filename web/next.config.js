/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: '.next',
  images: {
    unoptimized: true
  },
  // Ensure we don't process existing static files
  webpack: (config, { isServer }) => {
    config.module.rules.push({
      test: /\.(html|css|js)$/,
      exclude: /src/,
      type: 'asset/resource'
    });
    return config;
  }
}

module.exports = nextConfig

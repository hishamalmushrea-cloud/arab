/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // نستخدم static export مع data bundle
  // لكن لـ dev نبقي server
  experimental: {
    // لدعم البيانات الكبيرة
  },
  // لدعم تحميل JSON كبير
  webpack: (config) => {
    config.module.rules.push({
      test: /\.json\.br$/,
      type: 'asset/resource'
    });
    return config;
  }
};

module.exports = nextConfig;

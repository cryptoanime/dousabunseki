/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost', 'api.softtennis-ai.com'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NODE_ENV === 'production' 
      ? 'https://api.softtennis-ai.com' 
      : 'http://localhost:8000',
  },
}

module.exports = nextConfig
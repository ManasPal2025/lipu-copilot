# Frontend - Next.js Application

Next.js frontend for LIPU platform.

## Setup

```bash
cd apps/web

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
```

## Development

```bash
# Run dev server
npm run dev

# Build
npm run build

# Start production server
npm run start

# Lint
npm run lint

# Type check
npm run type-check

# Tests
npm run test
npm run test:coverage
```

## Project Structure

- `app/` - Next.js App Router (pages and layouts)
- `components/` - React components (by domain)
- `lib/` - Utilities and hooks
- `store/` - Zustand state management
- `styles/` - Global CSS
- `public/` - Static assets

## Available Routes

- `/` - Homepage
- `/login` - Login page
- `/register` - Register page
- `/dashboard` - Customer dashboard
- `/admin` - Admin dashboard (protected)

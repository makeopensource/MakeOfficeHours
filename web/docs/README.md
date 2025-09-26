# MakeOfficeHours Web Application Documentation

## Overview
The MakeOfficeHours web application is a modern, full-stack office hours queue management system built with Next.js 15, TypeScript, and Tailwind CSS. It provides a seamless experience for students and instructors to manage office hours queues with real-time updates, authentication, and responsive design.

## 🏗️ Architecture

### Tech Stack
- **Framework**: Next.js 15.2.4 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom animations
- **Authentication**: NextAuth.js with OAuth (Autolab integration)
- **Database**: Supabase (PostgreSQL)
- **UI Components**: Radix UI primitives

### Project Structure
```
web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Authentication Screens
│   │   ├── (screens)/         # Main application screens
│   │   └── api/               # API routes
│   ├── components/            # Reusable components
│   │   ├── custom/           # Custom business components
│   │   ├── queue/            # Queue-specific components
│   │   └── ui/               # Base UI components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utility libraries and helpers
│   └── types/                # TypeScript type definitions
├── public/                   # Static assets
└── docs/                     # Documentation
```

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Docker (optional, for containerized development)
- SSL certificates (for HTTPS development)

### Installation

1. **Clone the repository and navigate to web directory**
   ```bash
   cd /path/to/MakeOfficeHours/web
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the web directory with the following variables:\
   __Important__: These secrets are not self-generated. Please request access from us to obtain the values.
   ```env
    # Next.js / NextAuth Configuration
    NEXTAUTH_URL="https://localhost:3000"
    NODE_ENV="development"
    NEXTAUTH_SECRET="your-secret-key"

    # Autolab OAuth Configuration
    AUTOLAB_CLIENT_ID="your-autolab-client-id"
    AUTOLAB_CLIENT_SECRET="your-autolab-client-secret"
    AUTOLAB_AUTHORIZE_ENDPOINT="https://autolab.cse.buffalo.edu/oauth/authorize"
    AUTOLAB_TOKEN_ENDPOINT="https://autolab.cse.buffalo.edu/oauth/token"
    AUTOLAB_USER_ENDPOINT="https://autolab.cse.buffalo.edu/api/v1/user"
    AUTOLAB_COURSE_ENDPOINT="https://autolab.cse.buffalo.edu/api/v1/courses?state=current"
    AUTOLAB_REDIRECT_URI="https://localhost:3000/api/auth/callback/autolab"

    # Supabase Configuration
    NEXT_PUBLIC_SUPABASE_URL="your-supabase-url"
    NEXT_PUBLIC_SUPABASE_ANON_KEY="your-supabase-anon-key"

    # JWT
    JWT_SECRET="your-jwt-secret"
   ```

4. **Set up SSL certificates (for https development as we can't run localhost over http due to autolab Oauth config)**
   ```bash
   # Install mkcert if not already installed
   brew install mkcert  # macOS
   # or
   choco install mkcert  # Windows
   
   # Generate certificates
   mkcert -install
   mkcert localhost
   ```

### Development

#### Option 1: Standard Development Server
```bash
npm run dev
```
This starts the development server with HTTPS on `https://localhost:3000`

#### Option 2: Custom HTTPS Server
```bash
npm run dev:https
```
This uses the custom `server.js` for HTTPS with SSL certificates.

#### Option 3: Docker Development
```bash
# Use the docker script for development
./docker-scripts.sh dev
```
## API Routes

### Authentication Routes
- `GET /api/auth/[...nextauth]` - NextAuth.js handler
- `GET /api/auth/callback` - OAuth callback handler
- `POST /api/jwt` - JWT token generation for Supabase

### Queue Management Routes
- `GET /api/queue/get` - Fetch queue data
- `POST /api/queue/join` - Join queue
- `POST /api/queue/leave` - Leave queue
- `POST /api/queue/session/update` - Update session status
- `POST /api/queue/session/validate` - Validate session

### User Management Routes
- `GET /api/users` - Fetch user data

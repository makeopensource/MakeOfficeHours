# Docker Setup for Queue Application

This document provides instructions for running the Queue application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```bash
# Database
DATABASE_URL=your_database_url_here

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret_here

# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here

# Autolab API
AUTOLAB_CLIENT_ID=your_autolab_client_id_here
AUTOLAB_CLIENT_SECRET=your_autolab_client_secret_here
AUTOLAB_REDIRECT_URI=http://localhost:3000/api/auth/callback/autolab

# JWT
JWT_SECRET=your_jwt_secret_here

# Environment
NODE_ENV=development
```

## Development Mode

To run the application in development mode with hot reloading:

```bash
# Build and start the development container
docker-compose --profile dev up --build

# Or run in detached mode
docker-compose --profile dev up --build -d
```

The application will be available at `http://localhost:3000`

## Production Mode

To run the application in production mode:

```bash
# Build and start the production container
docker-compose --profile prod up --build

# Or run in detached mode
docker-compose --profile prod up --build -d
```

## Production Mode with Environment File

To run with a specific environment file:

```bash
# Create .env.production file first
docker-compose --profile prod-env up --build
```

## Manual Docker Commands

### Development

```bash
# Build development image
docker build -f Dockerfile.dev -t queue-app:dev .

# Run development container
docker run -p 3000:3000 -v $(pwd):/app -v /app/node_modules -v /app/.next queue-app:dev
```

### Production

```bash
# Build production image
docker build -t queue-app:prod .

# Run production container
docker run -p 3000:3000 queue-app:prod
```

## Stopping Containers

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific profile
docker-compose --profile dev down
```

## Useful Commands

```bash
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app-dev

# Execute commands in running container
docker-compose exec app-dev sh

# Rebuild without cache
docker-compose build --no-cache
```

## Troubleshooting

### Port Already in Use
If port 3000 is already in use, change the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Maps host port 3001 to container port 3000
```

### Permission Issues
If you encounter permission issues on Linux/macOS:

```bash
# Fix ownership of node_modules
sudo chown -R $USER:$USER node_modules
```

### Build Issues
If you encounter build issues:

```bash
# Clean up Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

## Notes

- The development setup includes volume mounts for hot reloading
- The production setup uses multi-stage builds for optimized images
- Environment variables should be properly configured before running
- The application uses Next.js standalone output for production builds 
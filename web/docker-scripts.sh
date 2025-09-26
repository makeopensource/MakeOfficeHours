#!/bin/bash

# Docker scripts for Queue Application - Development Only

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if required files exist
check_files() {
    if [ ! -f "package.json" ]; then
        print_error "package.json not found. Please run this script from the project root."
        exit 1
    fi
    
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found. Please ensure Docker files are created."
        exit 1
    fi
}

# Development commands
dev() {
    print_status "Starting development environment..."
    check_docker
    check_files
    docker compose up --build
    print_success "Development environment started. Access at https://localhost:3000"
}

dev_detached() {
    print_status "Starting development environment in detached mode..."
    check_docker
    check_files
    docker compose up --build -d
    print_success "Development environment started in detached mode. Access at https://localhost:3000"
}

# Build commands
build_dev() {
    print_status "Building development image..."
    check_docker
    check_files
    docker build -f Dockerfile -t queue-app:dev .
    print_success "Development image built successfully"
}

# Utility commands
stop() {
    print_status "Stopping all containers..."
    check_docker
    docker compose down
    print_success "All containers stopped"
}

clean() {
    print_status "Cleaning up Docker resources..."
    check_docker
    docker compose down --volumes --remove-orphans
    docker system prune -f
    print_success "Docker cleanup completed"
}

logs() {
    print_status "Showing logs for development service..."
    check_docker
    docker compose logs -f
}

shell() {
    print_status "Opening shell in development container..."
    check_docker
    check_files
    
    # Check if container is running
    if ! docker compose ps | grep -q "Up"; then
        print_warning "No running containers found. Starting development environment first..."
        dev_detached
        sleep 5
    fi
    
    docker compose exec app sh
}

# Help function
show_help() {
    echo "Docker Development Scripts for Queue Application"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Development Commands:"
    echo "  dev             Start development environment"
    echo "  dev-detached    Start development environment in detached mode"
    echo "  build-dev       Build development image"
    echo ""
    echo "Utility Commands:"
    echo "  stop            Stop all containers"
    echo "  clean           Clean up Docker resources"
    echo "  logs            Show logs for development service"
    echo "  shell           Open shell in development container"
    echo ""
    echo "Examples:"
    echo "  $0 dev          # Start development environment"
    echo "  $0 build-dev    # Build development image"
    echo "  $0 logs         # Show logs"
    echo "  $0 shell        # Open shell in container"
}

# Main script logic
case "${1:-help}" in
    "dev")
        dev
        ;;
    "dev-detached")
        dev_detached
        ;;
    "build-dev")
        build_dev
        ;;
    "stop")
        stop
        ;;
    "clean")
        clean
        ;;
    "logs")
        logs
        ;;
    "shell")
        shell
        ;;
    "help"|*)
        show_help
        ;;
esac
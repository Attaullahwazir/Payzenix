#!/bin/bash

# Secure Payment Application - Kali Linux Quick Start Script
# This script automates the setup process for running on Kali Linux

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running on Kali Linux
check_kali() {
    if grep -qi "kali" /etc/os-release 2>/dev/null; then
        print_success "Kali Linux detected"
        return 0
    else
        print_warning "Not running on Kali Linux (but may still work)"
        return 0
    fi
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local missing=0
    
    # Check Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        print_success "Docker installed: $DOCKER_VERSION"
    else
        print_error "Docker not installed"
        missing=1
    fi
    
    # Check Docker Compose
    if command -v docker-compose &> /dev/null; then
        DC_VERSION=$(docker-compose --version)
        print_success "Docker Compose installed: $DC_VERSION"
    else
        print_error "Docker Compose not installed"
        missing=1
    fi
    
    # Check Python 3
    if command -v python3 &> /dev/null; then
        PY_VERSION=$(python3 --version)
        print_success "Python installed: $PY_VERSION"
    else
        print_error "Python 3 not installed"
        missing=1
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        print_success "Git installed: $GIT_VERSION"
    else
        print_warning "Git not installed (optional)"
    fi
    
    if [ $missing -eq 1 ]; then
        print_error "Some prerequisites are missing. Install them with:"
        echo "sudo apt update && sudo apt install -y docker.io docker-compose python3 python3-pip git"
        return 1
    fi
    
    return 0
}

# Setup Docker permissions
setup_docker_permissions() {
    print_header "Setting Up Docker Permissions"
    
    if groups $USER | grep -q docker; then
        print_success "User already in docker group"
    else
        print_warning "Adding user to docker group..."
        sudo usermod -aG docker $USER
        print_success "User added to docker group"
        print_warning "Please log out and log back in for changes to take effect"
        print_warning "Or run: newgrp docker"
    fi
}

# Create environment file
create_env_file() {
    print_header "Creating Environment File"
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists. Skipping..."
        return 0
    fi
    
    if [ ! -f ".env.example" ]; then
        print_error ".env.example not found. Please ensure you're in the correct directory."
        return 1
    fi
    
    cp .env.example .env
    print_success "Created .env file from .env.example"
    
    # Generate keys
    print_header "Generating Security Keys"
    
    echo "Generating SECRET_KEY..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    echo "Generating JWT_SECRET_KEY..."
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    echo "Generating AES_KEY..."
    AES_KEY=$(python3 -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())")
    
    # Update .env file
    sed -i "s|your-secret-key-here-change-in-production|$SECRET_KEY|g" .env
    sed -i "s|your-jwt-secret-key-here-change-in-production|$JWT_SECRET_KEY|g" .env
    sed -i "s|your-aes-key-here-change-in-production|$AES_KEY|g" .env
    
    print_success "Security keys generated and added to .env"
    print_warning "Review .env file and update email settings if needed: nano .env"
}

# Get local IP
get_local_ip() {
    hostname -I | awk '{print $1}'
}

# Update configuration for network access
update_network_config() {
    print_header "Network Configuration"
    
    LOCAL_IP=$(get_local_ip)
    echo -e "${YELLOW}Your local IP address: ${LOCAL_IP}${NC}"
    
    read -p "Will this be accessed locally only (localhost)? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_success "Configured for localhost access"
    else
        print_warning "To allow remote access, update .env:"
        echo "  WEBAUTHN_ORIGIN=http://${LOCAL_IP}:5000"
        echo "  ALLOWED_ORIGINS=http://${LOCAL_IP}:5000,http://localhost:5000"
        echo ""
        read -p "Do you want to update .env now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sed -i "s|WEBAUTHN_ORIGIN=.*|WEBAUTHN_ORIGIN=http://${LOCAL_IP}:5000|g" .env
            sed -i "s|ALLOWED_ORIGINS=.*|ALLOWED_ORIGINS=http://${LOCAL_IP}:5000,http://localhost:5000|g" .env
            print_success "Updated network configuration in .env"
        fi
    fi
}

# Build and start services
start_services() {
    print_header "Building and Starting Services"
    
    print_warning "This may take 2-5 minutes on first run..."
    
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        return 1
    fi
}

# Wait for services to be healthy
wait_for_services() {
    print_header "Waiting for Services to Be Ready"
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker-compose ps | grep -q "payment_db.*healthy"; then
            print_success "Database is healthy"
            break
        fi
        
        attempt=$((attempt + 1))
        echo -ne "${YELLOW}Waiting for database... ($attempt/$max_attempts)${NC}\r"
        sleep 2
    done
    
    if [ $attempt -eq $max_attempts ]; then
        print_error "Database failed to become healthy"
        print_warning "Check logs with: docker-compose logs db"
        return 1
    fi
    
    sleep 5
}

# Initialize database
init_database() {
    print_header "Initializing Database"
    
    docker-compose exec backend flask db upgrade
    
    if [ $? -eq 0 ]; then
        print_success "Database initialized successfully"
    else
        print_error "Database initialization failed"
        print_warning "Check logs with: docker-compose logs backend"
        return 1
    fi
}

# Test API
test_api() {
    print_header "Testing API"
    
    echo "Testing health check..."
    HEALTH_RESPONSE=$(curl -s http://localhost:5000)
    
    if echo "$HEALTH_RESPONSE" | grep -q "Payment Gateway API"; then
        print_success "API is running and responding"
        echo "Response: $HEALTH_RESPONSE"
    else
        print_error "API health check failed"
        print_warning "Try manually: curl http://localhost:5000"
        return 1
    fi
}

# Display access information
show_access_info() {
    print_header "Application Ready!"
    
    LOCAL_IP=$(get_local_ip)
    
    echo -e "${GREEN}Services are running at:${NC}"
    echo ""
    echo -e "  ${BLUE}Web Interface:${NC}     http://localhost:5000"
    echo -e "  ${BLUE}Login Page:${NC}        http://localhost:5000/login"
    echo -e "  ${BLUE}Register Page:${NC}     http://localhost:5000/register"
    echo -e "  ${BLUE}Checkout:${NC}          http://localhost:5000/checkout"
    echo ""
    
    if [ "$LOCAL_IP" != "127.0.0.1" ]; then
        echo -e "${GREEN}Remote Access (from other machines):${NC}"
        echo "  http://${LOCAL_IP}:5000"
        echo ""
    fi
    
    echo -e "${GREEN}Useful Commands:${NC}"
    echo "  View logs:              docker-compose logs -f backend"
    echo "  Stop services:          docker-compose stop"
    echo "  Start services:         docker-compose start"
    echo "  Restart services:       docker-compose restart"
    echo "  Remove all containers:  docker-compose down"
    echo ""
    echo -e "${YELLOW}Documentation:${NC}"
    echo "  Setup guide:            KALI_LINUX_SETUP.md"
    echo "  Improvements:           IMPROVEMENTS_AND_FIXES.md"
    echo "  README:                 README.md"
}

# Show service status
show_status() {
    print_header "Service Status"
    docker-compose ps
}

# Main execution
main() {
    print_header "Secure Payment Application - Kali Linux Setup"
    
    # Step 1: Check prerequisites
    if ! check_prerequisites; then
        print_error "Missing prerequisites. Please install them first."
        exit 1
    fi
    
    # Step 2: Check Kali
    check_kali
    
    # Step 3: Setup Docker permissions
    setup_docker_permissions
    
    # Step 4: Create environment file
    if ! create_env_file; then
        print_error "Failed to create environment file"
        exit 1
    fi
    
    # Step 5: Update network config
    update_network_config
    
    # Step 6: Start services
    if ! start_services; then
        print_error "Failed to start services"
        docker-compose logs
        exit 1
    fi
    
    # Step 7: Wait for services
    if ! wait_for_services; then
        print_error "Services failed to become healthy"
        exit 1
    fi
    
    # Step 8: Initialize database
    if ! init_database; then
        print_error "Failed to initialize database"
        exit 1
    fi
    
    # Step 9: Test API
    if ! test_api; then
        print_warning "API test failed, but services may still be starting"
    fi
    
    # Step 10: Show status
    show_status
    
    # Step 11: Show access information
    show_access_info
    
    print_success "Setup completed successfully!"
}

# Run main function
main

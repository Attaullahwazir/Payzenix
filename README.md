# Secure Payment Application

A production-ready Flask payment processing application with enterprise-grade security features including AES-256 encryption, JWT authentication, WebAuthn/FIDO2 biometric support, and AI-based fraud detection.

## Features

- **Payment Processing**: Secure transaction handling with PCI-DSS compliance considerations
- **Authentication**: JWT tokens, Two-Factor Authentication (2FA), and WebAuthn/FIDO2 biometric authentication
- **Security**: AES-256 encryption for sensitive data, bcrypt password hashing, rate limiting
- **Fraud Detection**: AI-based anomaly detection using Isolation Forest
- **Real-time Updates**: WebSocket support for live transaction notifications
- **Admin Dashboard**: Comprehensive system management and analytics
- **Data Export**: CSV and PDF export capabilities
- **Mobile API**: Optimized endpoints for mobile applications

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Git

### Installation

```bash
# Clone and navigate to project
cd secure_payment_application

# On Kali Linux / Linux
sudo ./kali_setup.sh

# Or manually
docker-compose up -d --build
docker-compose exec backend flask db upgrade
```

### Access Application
- **Dashboard**: http://localhost:5000/dashboard
- **Admin Panel**: http://localhost:5000/admin
- **API**: http://localhost:5000/api

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - User registration
- `POST /login` - User login
- `POST /logout` - User logout

### Payments (`/api/payment`)
- `POST /process` - Process payment transaction
- `GET /history` - Get transaction history

### Two-Factor Auth (`/api/2fa`)
- `POST /setup` - Setup 2FA
- `POST /verify` - Verify 2FA token

### WebAuthn (`/api/webauthn`)
- `POST /register/begin` - Start biometric registration
- `POST /register/complete` - Complete biometric registration
- `POST /authenticate/begin` - Start biometric authentication
- `POST /authenticate/complete` - Complete biometric authentication

### Analytics (`/api/analytics`)
- `GET /stats` - User statistics
- `GET /trends` - Transaction trends

### Admin (`/api/admin`)
- `GET /users` - List all users
- `GET /transactions` - View all transactions
- `GET /health` - System health

## Technology Stack

- **Backend**: Flask 3.0.0, Python 3.11+
- **Database**: MySQL 8.0, Redis 7.0
- **Containerization**: Docker, Docker Compose
- **Security**: Cryptography, bcrypt, PyJWT
- **ML**: scikit-learn (Isolation Forest)
- **Frontend**: TailwindCSS, Vanilla JavaScript, PWA

## Configuration

Create a `.env` file in the root directory:

```env
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://user:password@localhost/payment_app
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
WEBAUTHN_ORIGIN=http://localhost:5000
ALLOWED_ORIGINS=http://localhost:5000
```

## Security Features

- **Data Protection**: AES-256-GCM encryption for sensitive fields
- **Authentication**: JWT tokens with configurable expiration
- **Rate Limiting**: 10 requests/minute for payment endpoints
- **Password Security**: Bcrypt hashing with cost factor 12
- **Input Validation**: Comprehensive input sanitization
- **CORS**: Configurable CORS headers
- **Fraud Detection**: ML-based anomaly detection on transactions

## Development

```bash
# Run in development mode
export FLASK_ENV=development
docker-compose up -d
docker-compose exec backend flask run

# Run tests
docker-compose exec backend pytest

# View logs
docker-compose logs -f backend
```

## Database

Database migrations are managed with Flask-Migrate (Alembic):

```bash
# Create new migration
docker-compose exec backend flask db migrate -m "description"

# Apply migrations
docker-compose exec backend flask db upgrade

# Rollback migration
docker-compose exec backend flask db downgrade
```

## Deployment

For production deployment:

1. Update `.env` with production credentials
2. Use `Dockerfile.prod` for optimized image
3. Configure proper database and Redis instances
4. Enable HTTPS/TLS
5. Set up proper logging and monitoring
6. Configure email service for notifications
7. Set up automated backups

## Support

For issues or questions, refer to the application logs:

```bash
docker-compose logs backend
```

## License

Proprietary - All rights reserved

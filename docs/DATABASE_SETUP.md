# Database Setup Guide

## Prerequisites

### PostgreSQL Installation

#### macOS
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Windows
Download and install PostgreSQL from: https://www.postgresql.org/download/windows/

## Database Configuration

### 1. Create Database User
```bash
# Access PostgreSQL
psql -U postgres

# Create user with password
CREATE USER postgres WITH PASSWORD 'nh-challenge';

# Grant privileges
ALTER USER postgres CREATEDB;
```

### 2. Create Database
```sql
CREATE DATABASE nh_challenge;

# Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE nh_challenge TO postgres;

# Exit PostgreSQL
\q
```

### 3. Verify Connection
```bash
psql -U postgres -d nh_challenge -h localhost
```

## Database Schema

The application uses the following main tables:

- `users` - User authentication and profiles
- `senior_profiles_v2` - Senior farmer profiles with embedding data
- `youth_profiles_v2` - Youth farmer profiles with embedding data
- `matches` - Match results between seniors and youth
- `matching_scores` - Detailed compatibility scores

## Migration

Database tables are created automatically when the application starts.
For manual migration, see [MIGRATION.md](./MIGRATION.md)
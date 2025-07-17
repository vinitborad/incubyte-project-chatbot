# Environment Variables Configuration

This document explains the environment variables used in the Sweet Shop Chatbot project.

## Required Environment Variables

### Database Configuration
- **MONGO_URI**: MongoDB connection string
  - Example: `mongodb://127.0.0.1:27017/sweet-shop`
  - Used in: `database.py`

### Redis Configuration
- **REDIS_URL**: Redis connection string for chat history storage
  - Example: `redis://localhost:6379`
  - Example (cloud): `rediss://default:password@host:6379`
  - Used in: `main.py`, `chatbot.py`, tests

### API Configuration
- **API_BASE_URL**: Base URL for the Node.js backend API
  - Example: `http://localhost:5000`
  - Used in: `tools.py`

### Frontend Configuration
- **FRONTEND_URL**: Frontend application URL for CORS configuration
  - Example: `http://localhost:3000`
  - Used in: `main.py`

### OpenAI Configuration
- **OPENAI_API_KEY**: OpenAI API key for GPT models
  - Required for chatbot functionality
  - Used by: LangChain OpenAI integration

### Environment
- **ENVIRONMENT**: Deployment environment (development, staging, production)
  - Example: `development`
  - Optional: Used for environment-specific configurations

## Setup Instructions

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your actual values:
   - Replace `your_openai_api_key_here` with your actual OpenAI API key
   - Update database URLs if using different hosts/ports
   - Modify API and frontend URLs for your deployment

3. Make sure `.env` is in your `.gitignore` file (already configured)

## Files Updated

The following files were updated to use environment variables instead of hardcoded values:

- **tools.py**: Now uses `API_BASE_URL` from environment
- **main.py**: Now uses `FRONTEND_URL` for CORS configuration
- **chatbot.py**: Updated to better handle Redis URL from environment
- **run_tests.py**: Now uses environment variables for test configuration

## Fallback Values

Most environment variables have sensible defaults for local development:
- `API_BASE_URL` defaults to `http://localhost:5000`
- `FRONTEND_URL` defaults to `http://localhost:3000`
- `REDIS_URL` defaults to `redis://localhost:6379`

However, `MONGO_URI` and `OPENAI_API_KEY` are required and must be set.

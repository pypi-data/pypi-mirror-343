# CODE NIA: Nozomio Intelligent Assistant

NIA AI is an AI-powered code assistant that helps developers understand, navigate, and contribute to codebases more efficiently through natural language interaction.

## Features

- **AI-Powered Code Chat**: Interact with codebases through natural language
- **GitHub Integration**: Connect and index your GitHub repositories
- **Intelligent Code Search**: Find code with natural language queries
- **Project Management**: Organize work with projects and chats
- **API Access**: Integrate NIA AI capabilities into your workflow
- **Slack Integration**: Connect with your team's Slack workspace

## Tech Stack

- **Frontend**: Next.js 15, React 19, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI (Python) with async support
- **Authentication**: Clerk
- **Database**: PostgreSQL with SQLAlchemy
- **Vector Search**: For efficient code embeddings
- **Payment Processing**: Stripe for subscription management

## Getting Started

### Prerequisites

- Node.js 18+ and bun
- Python 3.10+
- PostgreSQL database
- LLM API access
- Clerk account
- Stripe account (for payments)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/nia-ai-app.git
   cd nia-ai-app
   ```

2. Install dependencies:
   ```bash
   bun install
   cd backend && pip install -r requirements.txt
   ```

3. Configure environment:
   - Create `.env.local` with required variables
   - Update `backend/configs/local.yaml` with your credentials

### Running Locally

1. Start backend:
   ```bash
   cd backend && python -m uvicorn main:app --reload
   ```

2. Start frontend:
   ```bash
   bun dev
   ```

3. Access at `http://localhost:3000`

## Development Commands

- **Frontend**: `bun dev`
- **Backend**: `cd backend && python -m uvicorn main:app --reload`
- **Lint**: `bun lint`
- **Build**: `bun build`

## Code Style Guidelines

### Frontend
- Use Server Components by default; `"use client"` only when necessary
- Follow import order: types → builtins → external → internal → parent → sibling
- Use shadcn/UI components following project conventions

### Backend
- Use `async def` for I/O operations, `def` for pure functions
- Use type hints and Pydantic models for validation
- Implement proper error handling with specific HTTP exceptions

## Contributing

Follow established patterns, write tests for new features, and document your code.


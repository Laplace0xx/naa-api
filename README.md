# naa-api

API for NAA membership onboarding and identity verification.

## Tech Stack
- FastAPI
- SQLAlchemy 
- Alembic
- PostgreSQL
- Pydantic v2

## Setup

1. Clone the repository
2. Install dependencies: `uv sync`
3. Create a `.env` file with:
   ```
   DB_URL=postgresql+psycopg://user:password@localhost:5432/naa
   HMAC_SECRET=your-secret-key-here
   ```
4. Run migrations: `uv run alembic upgrade head`
5. Start the server: `uv run uvicorn main:app --port 8001`
6. Visit `http://127.0.0.1:8001/docs` for interactive API documentation

## Architecture

- `app/api/v1/` -- route modules (auth, applications, membership, admin)
- `app/models/` -- SQLAlchemy ORM models
- `app/schemas/` -- Pydantic request/response schemas
- `app/services/` -- business logic layer
- `app/repositories/` -- data access layer
- `app/interfaces/` -- abstract interfaces (verification provider)
- `app/db/` -- engine, session, migrations

## Design Decisions

- **Verification provider pattern**: NIN/BVN verification goes through an abstract interface (`NINVerificationAdapterInterface`). The mock provider can be swapped for a real NIMC/NIBSS integration without changing service or route code.
- **PII protection**: Raw NIN/BVN values are never stored. Only HMAC-SHA256 hashes are persisted. API responses never include raw or verified names.
- **Layered architecture**: Routes -> Services -> Repositories -> Models. Each layer has a single responsibility.
- **Sync SQLAlchemy**: Chosen for simplicity. Can be migrated to async later by changing engine/session and adding `async def` to endpoints.

## Implemented

- User registration with password hashing (bcrypt)
- NIN verification via mock provider
- HMAC-based credential storage
- Database migrations with Alembic

## Stubs (not yet implemented)

- Login / JWT token issuance
- Password reset
- Application submission and update
- Admin bulk upload
- Admin application review
- Membership status

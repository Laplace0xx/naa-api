# naa-api

Secure backend API for NAA membership onboarding and identity verification.

## Tech Stack

- FastAPI
- SQLAlchemy 2.0+ (sync)
- Alembic (migrations)
- PostgreSQL + psycopg
- Pydantic v2
- passlib (bcrypt) + python-jose (JWT)

## Setup

1. Install dependencies:
   ```
   uv sync
   ```
2. Create a `.env` file:
   ```
   DB_URL=postgresql+psycopg://naa_user:password@localhost:5432/naa
   HMAC_SECRET=your-secret-key-here
   ```
3. Grant schema access on Postgres 15+ (as superuser):
   ```sql
   GRANT ALL ON SCHEMA public TO naa_user;
   ```
4. Run migrations:
   ```
   uv run alembic upgrade head
   ```
5. Start the server:
   ```
   uv run uvicorn main:app --port 8001
   ```
6. Open interactive docs at `http://127.0.0.1:8001/docs` (ReDoc at `/redoc`, raw schema at `/openapi.json`).

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | /v1/auth/create-account | Register an applicant |
| POST | /v1/auth/login | Authenticate, returns JWT bearer token |
| POST | /v1/auth/reset-password | Reset password by email |
| POST | /v1/applications/{id}/upload-nin | Verify NIN/BVN identity for an applicant |
| POST | /v1/applications/{id}/submit | Submit an application |
| PATCH | /v1/applications/{id}/update | Update application details |
| POST | /v1/admin/login | Admin login |
| GET | /v1/admin/applications | List all applications |
| PATCH | /v1/admin/applications/{id}/status | Approve or reject an application |
| POST | /v1/admin/bulk | Bulk onboarding via CSV or JSON files |
| POST | /v1/admin/notification/{id} | Send a user notification |
| GET | /v1/membership/status?user_id= | Get membership status for a user |

## Bulk Onboarding

`POST /v1/admin/bulk` accepts one or more `.csv` or `.json` files as multipart uploads.

Required columns/keys per row: `f_name`, `l_name`, `gender`, `email`, `phone_number`, `dob`, `password`, `business_name`, `business_address`, `tin_number`.

CSV example:

```csv
f_name,l_name,gender,email,phone_number,dob,password,business_name,business_address,tin_number
Ada,Obi,female,ada@example.com,08011112222,1990-04-12,secret123,Ada Ventures,12 Market St,12345678
```

JSON example (bare list or `{"data": [...]}`):

```json
[
  {
    "f_name": "Ada",
    "l_name": "Obi",
    "gender": "female",
    "email": "ada@example.com",
    "phone_number": "08011112222",
    "dob": "1990-04-12",
    "password": "secret123",
    "business_name": "Ada Ventures",
    "business_address": "12 Market St",
    "tin_number": "12345678"
  }
]
```

Each row is validated with Pydantic. Duplicates are detected by email and phone number, both within the uploaded files and against existing users in the database, and counted separately from failures. The response reports `successful`, `failed`, and `duplicates` counts plus per-row errors with file name and row number. A duplicate race on concurrent requests is still rejected by the database unique constraints on `users.email` and `users.phone_number`.

## Architecture

- `app/api/v1/` — route modules (auth, applications, membership, admin), wired once in `app/api/router.py`
- `app/models/` — SQLAlchemy ORM models
- `app/schemas/` — Pydantic request/response schemas
- `app/services/` — business logic (auth, application, membership, verification)
- `app/repositories/` — data access per entity
- `app/interfaces/` — abstract verification provider contract plus mock implementation
- `app/db/` — engine, `get_db` session dependency
- `main.py` — FastAPI app instance

## Design Decisions

- **Replaceable verification provider**: NIN/BVN verification goes through `NINVerificationAdapterInterface`. `MockVerificationProvider` accepts any 11-digit numeric value and is injected via the `get_verification_service` dependency, so swapping in a real NIMC/NIBSS client means changing one line with no changes to services or routes.
- **PII protection**: raw NIN/BVN values are never stored and never returned. The service HMAC-SHA256 hashes the value with `HMAC_SECRET` and persists only the hash in `user_identity.hmac_value`. Verification responses return status only. No request logging of credential values exists in the codebase.
- **Layered architecture**: routes handle HTTP, services hold business rules, repositories own queries. The bulk endpoint composes `AuthService` and `ApplicationService` so per-row behavior matches the single-record endpoints.
- **Sync SQLAlchemy**: chosen for simplicity. Migration to async means swapping the engine/session and making endpoints `async def`.
- **Duplicate strategy**: email and phone are checked per row against an in-file seen-set and the users table before insert, with DB unique constraints as the final guard.

## Security Notes

- Passwords are hashed with bcrypt; only `password_hash` is stored.
- Auth uses JWT bearer tokens (`HS256`, 30-minute expiry).
- `HMAC_SECRET` must be set in `.env`. There is no safe default.
- Admin review endpoints currently check the `admin` role on the JWT identity but have no dedicated auth dependency; add one before exposing this publicly.

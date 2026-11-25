# Docker User Management System

A learning project using FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker and Docker Compose.

## Prerequisites
Install Docker Desktop (Windows/macOS) or Docker Engine + Compose plugin (Linux). Python and PostgreSQL are not required on the host to run the application.

## Start (from this directory)
1. Copy `.env.example` to `.env`.
2. Replace `POSTGRES_PASSWORD` with a long random value. Keep `.env` private.
3. Run `docker compose up --build -d`.
4. Check with `docker compose ps` and `docker compose logs -f app`.
5. Open http://localhost:8000/docs and http://localhost:8000/health.

PowerShell copy command: `Copy-Item .env.example .env`
Linux/macOS copy command: `cp .env.example .env`

## API
- `POST /users/register`
- `GET /users`
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`
- `GET /health`

Example registration JSON:
```json
{
  "full_name": "Asha Patil",
  "email": "asha@example.com",
  "password": "StrongPassword123!",
  "phone_number": "+919876543210"
}
```

## Useful commands
```bash
docker compose ps
docker compose logs -f app
docker compose exec db psql -U appuser -d user_management
docker compose down
docker compose up -d
docker compose down -v
```
`docker compose down` preserves the named database volume. `docker compose down -v` deletes it and all stored database data.

## Tests
Tests use an isolated in-memory SQLite database. To run them locally, install Python 3.12 and `pip install -r requirements.txt`, then `pytest -q`. This is optional and is not needed to run the Dockerized application.

## Security note
This is an educational CRUD example, not a production-ready identity service. Add authentication/authorization, TLS, rate limiting, secret management, backups, audit logging and security review before production use. Do not expose user listing/update/delete endpoints to the public without access controls.

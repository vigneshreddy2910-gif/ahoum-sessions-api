# Ahoum Sessions API

A containerized REST API for managing sessions, developed as part of the learning devops.

The project demonstrates Python API development, SQLite database persistence, Docker containerization, Docker Compose, automated testing with pytest, and continuous integration using GitHub Actions.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Application server:** Gunicorn
- **Containerization:** Docker and Docker Compose
- **Testing:** pytest
- **CI:** GitHub Actions

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API and database readiness |
| GET | `/sessions` | Returns stored sessions |
| POST | `/sessions` | Creates a new session |

### Example: Create a Session

Send a POST request to `http://localhost:5000/sessions` with this JSON body:

```json
{
  "title": "Morning Meditation",
  "description": "A guided meditation for beginners",
  "category": "Meditation",
  "duration": 30
}
```

A successful request returns HTTP `201 Created`, including the newly assigned session ID.

The API validates required fields, non-empty text fields, and positive integer duration values. Invalid requests return HTTP `400 Bad Request` with an explanatory error message.

## Prerequisites

- Docker Desktop with Linux containers enabled
- Docker Compose
- Git

Python is only required for running the application and tests outside Docker.

## Running with Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/vigneshreddy2910-gif/ahoum-sessions-api.git
cd ahoum-sessions-api
```

### 2. Configure environment variables

Copy the example configuration to `.env`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

On Linux/macOS:

```bash
cp .env.example .env
```

Example configuration:

```dotenv
DATABASE_PATH=/app/data/sessions.db
PORT=5000
```

### 3. Build and start the application

```bash
docker compose up --build -d
```

The API is available at `http://localhost:5000`.

### 4. Check container status

```bash
docker compose ps
```

### 5. View application logs

```bash
docker compose logs --tail=50 api
```

To follow logs continuously:

```bash
docker compose logs -f api
```

### 6. Stop and remove the container

```bash
docker compose down
```

This removes the container and Compose network while retaining the named database volume.

## API Testing

Check readiness:

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

Retrieve sessions:

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/sessions" -Method GET
```

Create a session using PowerShell:

```powershell
$body = @{
    title = "Docker Meditation"
    description = "Testing SQLite persistence inside Docker"
    category = "Meditation"
    duration = 25
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/sessions" -Method POST -ContentType "application/json" -Body $body
```

## Automated Tests

The project contains seven pytest tests covering:

- Health endpoint
- Empty sessions list
- Session creation and retrieval
- Missing title validation
- Negative duration validation
- Empty title validation
- Boolean duration validation

Run locally after installing the Python dependencies:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

The seven tests passed during local verification.

## Docker Image, Container, Volume, and Network

**Docker image:** The packaged application, Python runtime, dependencies, and startup command created from the Dockerfile.

**Docker container:** A running instance of the image. Gunicorn serves the Flask API on port 5000.

**Docker volume:** The named volume `sessions_data` is mounted at `/app/data`, where SQLite stores `sessions.db`. This separates persistent database files from the container's disposable filesystem.

**Docker network:** Docker Compose creates a project network for its services. The API's container port 5000 is published to host port 5000 so clients can access it through localhost.

## SQLite Persistence Verification

Persistence was tested using these steps:

1. Started the API with Docker Compose.
2. Created a session named `Docker Meditation`.
3. Confirmed it appeared in `GET /sessions`.
4. Executed `docker compose down`, removing the container.
5. Recreated the container with `docker compose up -d`.
6. Called `GET /sessions` again.

**Result:** The previously created session remained available after container recreation, confirming persistence through the named Docker volume.

**Warning:** `docker compose down -v` also removes Compose-managed named volumes and can delete the stored database.

## Continuous Integration

GitHub Actions workflow: `.github/workflows/ci.yaml`

The workflow runs on pushes and pull requests and performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies from `requirements.txt`.
4. Executes the pytest suite.
5. Builds the Docker image.

The workflow was reported successful following the initial GitHub push.

The image is built on the GitHub Actions runner; it is not automatically published to a container registry or deployed.

## Troubleshooting

### Issue 1: Docker Compose could not find `.env`

**Error:** `env file ... .env not found`

**Investigation:** Docker Compose validation failed because `compose.yaml` referenced an environment file that was missing from the project directory.

**Fix:** Created `.env` using the values from `.env.example` and reran:

```bash
docker compose config --quiet
```

**Result:** Compose configuration validation succeeded.

### Issue 2: Pytest could not import the database module

**Error:** `ModuleNotFoundError: No module named 'database'`

**Investigation:** Pytest was executed from inside the `test` directory, while `database.py` was located in the project root.

**Fix:** Returned to the project root and executed:

```bash
python -m pytest -v
```

**Result:** All seven automated tests passed.

## Project Structure

```text
ahoum-sessions-api/
├── .github/
│   └── workflows/
│       └── ci.yaml
├── test/
│   └── test_app.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── app.py
├── compose.yaml
├── database.py
└── requirements.txt
```

## Assignment Outcome

The application demonstrates a working REST API, input validation, SQLite storage, Docker containerization, persistent data storage through Docker Compose, automated tests, and GitHub Actions continuous integration.

**Repository:** https://github.com/vigneshreddy2910-gif/ahoum-sessions-api

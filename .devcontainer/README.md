# DevContainer Setup

This devcontainer configuration provides a development environment that closely matches the Railway production environment.

## What's Included

- **Python 3.13 slim** (same as production)
- **Node.js 20** (for frontend development)
- **UV package manager** (fast Python dependency management)
- **Git, curl, vim, nano** (development tools)
- **VS Code extensions** (Python, ESLint, Docker, etc.)

## How to Use

### Option 1: VS Code (Recommended)

1. Install **"Dev Containers"** extension in VS Code
2. Open this project in VS Code
3. Press `F1` → "Dev Containers: Reopen in Container"
4. Wait for the container to build and setup to complete

### Option 2: Command Line

```bash
# Build and start the devcontainer
docker compose -f .devcontainer/docker-compose.yml up -d

# Attach to the container
docker compose -f .devcontainer/docker-compose.yml exec app bash
```

## Development Workflows

### Workflow 1: Separate Frontend & Backend (Hot Reload)

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access:
- Frontend: http://localhost:5173 (with hot reload)
- Backend API: http://localhost:8000/api/*

### Workflow 2: Production Build (Same as Railway)

```bash
docker compose -f docker-compose.dev.yml up
```

Access: http://localhost:8000 (frontend + backend together)

## Environment Variables

Set these in your local environment or in `.devcontainer/docker-compose.yml`:

```bash
ANTHROPIC_API_KEY=sk-ant-...     # Your Anthropic API key
TRUSTED_TOKENS=your_token         # Authentication token
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:5173
```

## Key Differences from Production

| Aspect | DevContainer | Railway Production |
|--------|-------------|-------------------|
| Base Image | Python 3.13-slim ✓ | Python 3.13-slim ✓ |
| Package Manager | UV (local) | pip (production) |
| File Access | Mounted volumes | Baked into image |
| Auto-reload | ✓ (--reload) | ✗ |
| Development Tools | ✓ (vim, git, etc.) | ✗ (minimal) |

## Benefits

✅ **Consistent Environment** - Same Python/Node versions as production
✅ **Isolated** - Won't affect your host machine
✅ **Pre-configured** - All tools and extensions ready
✅ **Fast Setup** - One command to get started
✅ **Team Ready** - Share exact environment with teammates

## Troubleshooting

**Container won't start:**
```bash
docker compose -f .devcontainer/docker-compose.yml down
docker compose -f .devcontainer/docker-compose.yml up --build
```

**Permission issues:**
```bash
sudo chown -R $USER:$USER .
```

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

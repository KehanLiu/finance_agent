# 📦 UV Package Manager Guide

Complete guide to using UV for dependency management in this project.

---

## 🎯 What is UV?

**UV** is an extremely fast Python package manager written in Rust:
- ⚡ 10-100x faster than pip
- 🔒 Reliable dependency resolution
- 🎯 Single tool for everything Python
- 📦 Compatible with pip and existing tools

### UV vs Other Tools

| Feature | UV | pip | poetry | conda |
|---------|----|----|--------|-------|
| **Speed** | ⚡⚡⚡ | ⚡ | ⚡⚡ | ⚡ |
| **Dependency Resolution** | ✅ Fast | ⚠️ Slow | ✅ Good | ✅ Good |
| **Python Version Management** | ✅ | ❌ | ❌ | ✅ |
| **Lockfiles** | ✅ | ❌ | ✅ | ✅ |
| **Compatibility** | ✅ pip-compatible | ✅ | ⚠️ | ⚠️ |

---

## 🚀 Installing UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Verify installation
uv --version
```

After install, restart your terminal or:
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

---

## 📁 Project Structure (This Project)

```
backend/
├── pyproject.toml       # ✅ Single source of truth for dependencies
├── .venv/              # Virtual environment (managed by uv)
├── main.py
└── auth.py
```

**Key file**: `pyproject.toml`
```toml
[project]
name = "finance-analysis-backend"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn>=0.24.0",
    "pandas>=2.1.3",
    "anthropic>=0.8.1",
    "python-dotenv>=1.0.0",
    "slowapi>=0.1.9",
]
```

---

## 🔧 Common UV Commands

### 1. Create Virtual Environment
```bash
cd backend
uv venv
```

This creates `.venv/` directory.

### 2. Install Project Dependencies
```bash
# Install from pyproject.toml
uv pip install -e .

# The -e flag means "editable mode" - changes to code reflect immediately
```

### 3. Install Individual Packages
```bash
# Install a package
uv pip install package-name

# Install specific version
uv pip install fastapi==0.115.0

# Install with version constraint
uv pip install "fastapi>=0.104.1"
```

### 4. Update Package
```bash
uv pip install --upgrade package-name
```

### 5. List Installed Packages
```bash
uv pip list
```

### 6. Remove Package
```bash
uv pip uninstall package-name
```

### 7. Freeze Dependencies
```bash
# Generate exact versions
uv pip freeze > requirements-lock.txt
```

---

## 🎓 How This Project Uses UV

### Development Workflow

**1. First Time Setup:**
```bash
cd backend

# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install project dependencies
uv pip install -e .
```

**2. Adding New Dependencies:**
```bash
# Install the package
uv pip install new-package

# Update pyproject.toml
# Add to dependencies array:
# "new-package>=1.0.0",
```

**3. Running the App:**
```bash
source .venv/bin/activate
python -m uvicorn main:app --reload
```

---

## 🚢 Railway Deployment

Railway uses **pip** by default (not uv), but reads from **pyproject.toml**.

### How Railway Installs Dependencies

**Step 1**: Railway detects `pyproject.toml`
```dockerfile
# Railway automatically runs:
pip install .
```

**Step 2**: Pip reads `pyproject.toml` and installs dependencies
```python
# From pyproject.toml:
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn>=0.24.0",
    # ... etc
]
```

**Step 3**: Railway builds and deploys

### Our Dockerfile (Dockerfile.production)

```dockerfile
# Copy dependency file
COPY backend/pyproject.toml ./backend/

# Install dependencies
RUN pip install --no-cache-dir ./backend/

# Copy rest of code
COPY backend/ ./backend/
```

**Why this works:**
- ✅ `pip` can read `pyproject.toml` (PEP 621 standard)
- ✅ No need for uv in production
- ✅ Single source of truth (pyproject.toml)
- ✅ Fast builds (pip caches layers)

---

## 📋 Dependency Management Best Practices

### 1. Version Constraints

**Use `>=` for flexibility:**
```toml
dependencies = [
    "fastapi>=0.104.1",  # ✅ Good - allows minor updates
    "fastapi==0.104.1",  # ⚠️ Strict - no updates
]
```

### 2. Keep pyproject.toml Updated

When you install a package:
```bash
# Install
uv pip install slowapi

# Update pyproject.toml manually
# Add: "slowapi>=0.1.9"
```

### 3. Python Version

Specify minimum Python version:
```toml
requires-python = ">=3.11"
```

Railway will use Python 3.11+.

### 4. Optional Dependencies

For dev-only packages:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
]
```

Install with:
```bash
uv pip install -e ".[dev]"
```

---

## 🔄 Migration from requirements.txt

**Old way** (requirements.txt):
```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
```

**New way** (pyproject.toml):
```toml
[project]
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn>=0.24.0",
    "pandas>=2.1.3",
]
```

### Why pyproject.toml is Better

| Feature | requirements.txt | pyproject.toml |
|---------|------------------|----------------|
| **Metadata** | ❌ None | ✅ Project info |
| **Build System** | ❌ No | ✅ Yes |
| **Standard** | ⚠️ Informal | ✅ PEP 621 |
| **Tools** | ❌ pip only | ✅ All modern tools |
| **Optional Deps** | ❌ No | ✅ Yes |

---

## 🐛 Troubleshooting

### "Command 'uv' not found"

**Solution:**
```bash
# Reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

### "No module named 'package_name'"

**Solution:**
```bash
# Make sure venv is activated
source .venv/bin/activate

# Reinstall dependencies
uv pip install -e .
```

### "Module not found in Railway"

**Solution:**
- Make sure package is in `pyproject.toml` dependencies
- Railway reads from `pyproject.toml`
- Check Railway logs for install errors

### Virtual Environment Issues

**Solution:**
```bash
# Delete and recreate
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## 📊 Summary

### Local Development (Use UV)
```bash
# Create environment
uv venv

# Install dependencies
uv pip install -e .

# Add new package
uv pip install package-name
# Then update pyproject.toml
```

### Production (Railway uses pip)
```dockerfile
# Railway automatically does:
COPY pyproject.toml ./
RUN pip install .
```

### Single Source of Truth
```
pyproject.toml  ← All dependencies here
└── Used by:
    ├── uv (local development)
    ├── pip (Railway deployment)
    └── Other tools (pytest, black, etc.)
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Create venv | `uv venv` |
| Install project | `uv pip install -e .` |
| Add package | `uv pip install pkg` |
| Update package | `uv pip install --upgrade pkg` |
| List packages | `uv pip list` |
| Remove package | `uv pip uninstall pkg` |
| Freeze deps | `uv pip freeze` |

**Remember**: Always update `pyproject.toml` after installing packages!

---

## ✅ Checklist

**Local Development:**
- [ ] UV installed
- [ ] Virtual environment created (`uv venv`)
- [ ] Dependencies installed (`uv pip install -e .`)
- [ ] pyproject.toml is up to date

**Before Deployment:**
- [ ] All packages listed in `pyproject.toml`
- [ ] Tested locally with `uv pip install -e .`
- [ ] No `requirements.txt` file (removed)
- [ ] Dockerfile uses `pyproject.toml`

---

**Official Docs**: https://github.com/astral-sh/uv
**PEP 621**: https://peps.python.org/pep-0621/

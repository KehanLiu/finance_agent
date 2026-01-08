# 📚 Finance Dashboard Documentation

Complete documentation for the Finance Analysis Dashboard.

---

## 📖 Documentation Index

### [🚀 Deployment Guide](DEPLOYMENT.md) ⭐ START HERE
**Complete Railway deployment guide (20-25 min)**

Detailed, step-by-step guide to deploy your Finance Dashboard to Railway.

**Includes**:
- ✅ Pre-deployment checklist
- 🔒 Security verification steps
- 📦 GitHub repository setup (private!)
- 🚂 Railway project creation ($5 trial credits)
- ⚙️ Environment variables configuration
- 📁 **CSV data upload via Railway CLI** (secure, never commits to Git!)
- 🌐 CORS configuration
- 🧪 Testing & verification
- 💰 Cost monitoring
- 🐛 Troubleshooting with solutions

**Start here if**: You want to deploy to the internet.

---

### [🔒 Security Guide](SECURITY.md)
**Complete security documentation**

Everything about security features, best practices, and incident response.

**Includes**:
- 🛡️ Security features explained
- 🔑 Token management
- 🔐 Authentication system
- 🌐 Production security
- 🔍 Security monitoring
- 📊 Security comparisons

**Start here if**: You want to understand the security measures or best practices.

---

### [🛠️ Development Guide](DEVELOPMENT.md)
**Local setup, architecture & API reference**

Complete guide for local development and contributing.

**Includes**:
- 🏗️ System architecture
- 🚀 Local development setup
- 🔌 API endpoints reference
- 🎨 Frontend components
- 📝 Adding features
- 🧪 Testing checklist

**Start here if**: You want to develop locally or understand the codebase.

---

### [📦 UV Package Manager Guide](UV_GUIDE.md)
**Fast Python dependency management**

Complete guide to using UV for managing Python dependencies.

**Includes**:
- ⚡ What is UV and why use it
- 🔧 Common UV commands
- 🎓 Project workflow
- 🚢 Railway deployment details
- 🐛 Troubleshooting

**Start here if**: You want to understand how dependencies are managed.

---

## 🎯 Quick Links

### Common Tasks

| I want to... | Go to... |
|--------------|----------|
| Deploy the app | [Deployment Guide - Quick Deploy](DEPLOYMENT.md#-quick-deploy-10-minutes) |
| Run locally | [Development Guide - Quick Start](DEVELOPMENT.md#-quick-start-local-development) |
| Understand security | [Security Guide - Overview](SECURITY.md#-security-overview) |
| Rotate tokens | [Security Guide - Token Management](SECURITY.md#-token-management) |
| Troubleshoot deployment | [Deployment Guide - Troubleshooting](DEPLOYMENT.md#-troubleshooting) |
| Add a feature | [Development Guide - Adding Features](DEVELOPMENT.md#-adding-features) |
| Share access | [Deployment Guide - Share Access](DEPLOYMENT.md#-share-access) |
| Monitor security | [Security Guide - Security Monitoring](SECURITY.md#-security-monitoring) |

---

## 📊 Documentation Structure

```
documentation/
├── README.md           # This file - Documentation index
├── DEPLOYMENT.md      # Deployment to Railway
├── SECURITY.md        # Security features & practices
└── DEVELOPMENT.md     # Local development & architecture
```

---

## 🆘 Getting Help

### For Deployment Issues
See [Deployment Guide - Troubleshooting](DEPLOYMENT.md#-troubleshooting)

### For Security Questions
See [Security Guide](SECURITY.md)

### For Development Help
See [Development Guide](DEVELOPMENT.md)

---

## 📝 Contributing

Want to improve the documentation?

1. Make your changes
2. Test that all links work
3. Ensure formatting is consistent
4. Submit a pull request

---

## 📌 Quick Reference

### Essential Commands

**Generate tokens**:
```bash
python backend/auth.py
```

**Run locally**:
```bash
# Backend
cd backend && python -m uvicorn main:app --reload

# Frontend
cd frontend && npm run dev
```

**Deploy to Railway**:
```bash
git push origin main  # Railway auto-deploys
```

### Essential Files

- `backend/.env` - Backend configuration (DO NOT COMMIT)
- `frontend/.env` - Frontend configuration (DO NOT COMMIT)
- `data/*.csv` - Financial data (DO NOT COMMIT)
- `.gitignore` - Files to never commit

### Essential URLs

**Local Development**:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Production** (Railway):
- App: https://your-app.up.railway.app
- Railway Dashboard: https://railway.app

---

**Last Updated**: 2026-01-07
**Version**: 2.0 (Production Ready)

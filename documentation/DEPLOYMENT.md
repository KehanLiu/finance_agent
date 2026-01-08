# 🚂 Railway Deployment Guide - Step by Step

Complete, detailed guide to deploy your Finance Analysis Dashboard to Railway.

---

## 📋 Pre-Deployment Checklist

Before you start, make sure you have:

- [ ] **GitHub account** - [github.com](https://github.com)
- [ ] **Railway account** - [railway.app](https://railway.app) - Sign up with GitHub
- [ ] **Anthropic API key** - [console.anthropic.com](https://console.anthropic.com)
- [ ] **Your CSV data** - Files in `data/` folder
- [ ] **Tested locally** - App works at http://localhost:3001

---

## 🎯 Step 1: Generate Authentication Tokens

**Time: 1 minute**

Open your terminal and run:

```bash
cd backend
python auth.py
```

You'll see output like this:
```
🔐 Generate secure tokens for you and your wife:
AUTH_TOKEN_1=Rt8G_xK2yP9vN4wL3mJ7hF6dS5aQ1zX9cV8bM2nK4pT0
AUTH_TOKEN_2=Pq4N_vL9wM2xY8jK3fH6gD5sA1zC0bV7nM4tR9pQ2oL6
```

**Action:**
1. ✅ Copy both tokens
2. ✅ Save them in a secure place (password manager or text file)
3. ✅ You'll need these in Step 5

---

## 🔒 Step 2: Security Check

**Time: 2 minutes**

### 2.1 Verify .gitignore

```bash
cat .gitignore | grep -E "(\.env|\.csv)"
```

**You should see:**
```
backend/.env
frontend/.env
data/*.csv
```

✅ If yes, proceed. ❌ If no, these files might be committed (dangerous!)

### 2.2 Check What Will Be Committed

```bash
git status
```

**Make sure these are NOT listed:**
- ❌ `backend/.env`
- ❌ `frontend/.env`
- ❌ `data/*.csv` (your financial data!)

**If they appear**, run:
```bash
git rm --cached backend/.env
git rm --cached frontend/.env
git rm --cached data/*.csv
```

---

## 📦 Step 3: Create Private GitHub Repository

**Time: 3 minutes**

### 3.1 Create Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `finance-dashboard` (or any name you want)
3. **⚠️ CRITICAL**: Select **"Private"** ← MUST BE PRIVATE!
4. ❌ Do NOT initialize with README (you already have one)
5. Click **"Create repository"**

### 3.2 Push Your Code

GitHub will show you commands. Use these:

```bash
# If you haven't initialized git yet:
git init
git add .
git commit -m "Initial commit - ready for deployment"

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/finance-dashboard.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### 3.3 Verify Repository is Private

1. Go to your repository on GitHub
2. Check for 🔒 **Private** badge next to repository name
3. ✅ If you see it, you're good!

---

## 🚂 Step 4: Create Railway Project

**Time: 3 minutes**

### 4.1 Sign Up / Login to Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Login"** (top right)
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your GitHub

**You'll get $5 in trial credits!** 💰

### 4.2 Create New Project

1. Click **"New Project"** (or **"Start a New Project"**)
2. Select **"Deploy from GitHub repo"**
3. You'll see a list of your repositories
4. ⚠️ **If you don't see your repo:**
   - Click **"Configure GitHub App"**
   - Grant Railway access to your private repository
   - Come back and refresh

5. **Select your `finance-dashboard` repository**
6. Railway will automatically detect the `Dockerfile.production`

### 4.3 Wait for Initial Build

You'll see:
- ⚙️ Building...
- 📦 Build logs scrolling
- ⏱️ Takes ~3-5 minutes first time

**This will FAIL** - that's okay! We need to add environment variables first.

---

## ⚙️ Step 5: Configure Environment Variables

**Time: 3 minutes**

### 5.1 Open Variables Tab

1. In Railway dashboard, click on your project
2. Click **"Variables"** tab
3. You'll see an empty list

### 5.2 Add Required Variables

Click **"New Variable"** for each of these:

**Variable 1:**
```
Name: AUTH_TOKEN_1
Value: [paste your first token from Step 1]
```

**Variable 2:**
```
Name: AUTH_TOKEN_2
Value: [paste your second token from Step 1]
```

**Variable 3:**
```
Name: ANTHROPIC_API_KEY
Value: [paste your Anthropic API key]
```

**Variable 4:**
```
Name: ENVIRONMENT
Value: production
```

**Variable 5:**
```
Name: CORS_ORIGINS
Value: https://finance-dashboard-production.up.railway.app
```

⚠️ **For CORS_ORIGINS**: Use a placeholder for now, we'll update it in Step 7!

### 5.3 Save Variables

Click **"Add"** or **"Save"** after entering all variables.

---

## 📁 Step 6: Upload Your CSV Data

**Time: 5 minutes**

**Why this is needed:** Your CSV files are in `.gitignore`, so Railway doesn't have them after Git deployment. You need to upload them separately.

### ⭐ Option A: Railway CLI (Recommended & Most Secure)

This is the **best way** - it uploads your data without committing to Git.

#### 6.1 Install Railway CLI

```bash
# macOS/Linux
curl -fsSL https://railway.app/install.sh | sh

# Or with npm (if you have Node.js)
npm install -g @railway/cli

# Verify installation
railway --version
```

#### 6.2 Login to Railway

```bash
railway login
```

This will:
- Open your browser
- Ask you to authorize the CLI
- ✅ You're logged in!

#### 6.3 Link to Your Project

```bash
# Make sure you're in your project root directory
cd /home/kehan-linux/projects/small_private/finance_analysis

# Link to Railway project
railway link
```

You'll see a list of your Railway projects. Select the one you just created.

#### 6.4 Deploy with Data

```bash
# This uploads EVERYTHING, including data/ folder
railway up
```

**What happens:**
- 📦 Uploads all files (including `.gitignore` files!)
- 🚀 Builds and deploys
- ✅ Your CSV data is now on Railway!

**Verify it worked:**
```bash
# SSH into your Railway container
railway run bash

# Check data folder
ls -lh /app/data/

# You should see your CSV files!
# Exit with: exit
```

---

### ⚠️ Option B: Temporarily Commit (Not Recommended)

**Only use if Railway CLI doesn't work for some reason.**

**Steps:**
1. Edit `.gitignore`:
```bash
# Comment out the CSV line
sed -i.bak 's/^data\/\*.csv/#data\/\*.csv/' .gitignore
```

2. Commit and push:
```bash
git add data/
git commit -m "Temporary: Add CSV for deployment"
git push
```

3. **IMPORTANT** - Restore `.gitignore`:
```bash
# Restore from backup
mv .gitignore.bak .gitignore

git add .gitignore
git commit -m "Restore .gitignore"
git push
```

**Downsides:**
- ❌ CSV in Git history forever (can't fully delete)
- ❌ Less secure
- ❌ File size limits on Git

---

### ✅ Recommended: Use Railway CLI

**Why Railway CLI is better:**
- ✅ CSV never touches Git
- ✅ More secure
- ✅ Easier to update data
- ✅ No file size limits
- ✅ Can upload large files

**Updating data later:**
```bash
# Just run this anytime you update your CSV files
railway up
```

---

## 🌐 Step 7: Get Your Railway URL & Update CORS

**Time: 2 minutes**

### 7.1 Find Your App URL

1. In Railway dashboard, click **"Settings"** tab
2. Scroll to **"Domains"** section
3. You'll see: `https://your-app-production-xxxx.up.railway.app`
4. ✅ Copy this URL

### 7.2 Update CORS_ORIGINS

1. Go back to **"Variables"** tab
2. Find **CORS_ORIGINS**
3. Click to edit
4. **Replace** with your actual URL:
```
https://your-actual-app.up.railway.app
```
5. Save

### 7.3 Redeploy

1. Go to **"Deployments"** tab
2. Click **"Redeploy"** on the latest deployment
3. OR just push a new commit:
```bash
git commit --allow-empty -m "Trigger redeploy"
git push
```

Wait ~2-3 minutes for redeployment.

---

## ✅ Step 8: Test Your Deployment

**Time: 3 minutes**

### 8.1 Open Your App

Visit your Railway URL: `https://your-app.up.railway.app`

### 8.2 Test Guest Mode

**You should see:**
- ✅ Dashboard loads
- ✅ Charts display (with obfuscated amounts)
- ✅ "Guest Mode" badge in top right
- ✅ Numbers appear (scaled by ~0.2-0.4 of real values)

**If you see errors:**
- Check Railway logs (Deployments → View Logs)
- Verify all environment variables are set
- Make sure CSV files uploaded

### 8.3 Test Login

1. Click **"Login"** button (top right)
2. Paste your `AUTH_TOKEN_1` value
3. Click **"Login"**

**You should see:**
- ✅ "Trusted Mode" badge appears
- ✅ Real financial amounts display
- ✅ AI Insights tab becomes clickable

### 8.4 Test AI Insights (Optional)

1. Click **"AI Insights"** tab
2. Ask a question: "What are my top spending categories?"
3. Wait 5-10 seconds
4. ✅ You should see Claude's analysis

### 8.5 Test Logout

1. Click **"Logout"** button
2. ✅ Returns to "Guest Mode"
3. ✅ Amounts change back to obfuscated values

---

## 🎊 Step 9: Share Access with Your Wife

**Time: 2 minutes**

Send her (via **Signal** or **WhatsApp** - encrypted!):

```
Finance Dashboard Access 💰

URL: https://your-app.up.railway.app

Your Login Token:
[paste AUTH_TOKEN_2 here]

How to login:
1. Open the URL
2. Click "Login" button (top right)
3. Paste the token above
4. Click "Login"
5. You'll now see our real financial data!

Note: Session expires after 30 minutes. Just login again if needed.
```

---

## 📊 Step 10: Monitor Usage & Costs

**Time: 1 minute**

### 10.1 Check Your Credits

1. Railway dashboard → **"Usage"** tab
2. See remaining trial credits
3. View current month usage

**You started with $5 trial credits.**

### 10.2 Set Up Alerts (Optional)

1. Go to **"Settings"** → **"Usage Limits"**
2. Set alert at **$4** (80% of trial)
3. You'll get email when approaching limit

### 10.3 Monitor Daily

- **$0.15-0.30/day** = Normal ✅
- **$1+/day** = Check for issues ⚠️

---

## 🔧 Maintenance & Updates

### Updating Your App

**When you change code:**
```bash
git add .
git commit -m "Update: describe your changes"
git push
```

Railway auto-deploys on push! ⚡

### Adding New CSV Data

**Option 1: Railway CLI**
```bash
railway up
```

**Option 2: Commit (if removed from .gitignore)**
```bash
git add data/
git commit -m "Update financial data"
git push
```

### Rotating Tokens

**Every 3-6 months:**
```bash
cd backend
python auth.py  # Generate new tokens
```

Then:
1. Update `AUTH_TOKEN_1` and `AUTH_TOKEN_2` in Railway Variables
2. Redeploy
3. Share new tokens with users

---

## 🐛 Troubleshooting

### Issue: "No CSV file found in data folder"

**Solution:**
- CSV data not uploaded
- Use Railway CLI: `railway up`
- Or temporarily commit CSV files

### Issue: "CORS Error" in Browser

**Solution:**
- Check `CORS_ORIGINS` matches your Railway URL exactly
- Include `https://`
- No trailing slash
- Redeploy after fixing

### Issue: "Invalid Token" When Logging In

**Solution:**
- Paste token value ONLY (not `AUTH_TOKEN_1=...`)
- Check token in Railway Variables matches
- Token should be 43 characters
- No spaces or line breaks

### Issue: App Shows "Application Error"

**Solution:**
1. Check Railway logs (Deployments → View Logs)
2. Look for error messages
3. Common issues:
   - Missing environment variable
   - CSV files not uploaded
   - Wrong Python version

### Issue: Build Failed

**Solution:**
1. Check build logs in Railway
2. Common causes:
   - Missing dependency in `pyproject.toml`
   - Syntax error in code
   - Dockerfile issue

**Check build logs:**
- Railway dashboard → Deployments → Latest deployment → Logs

---

## 💰 Cost Management

### Monitor Your Spending

**Week 1:**
- Expected: $1-2 used
- ✅ Trial: $3-4 remaining

**Week 2:**
- Expected: $2-4 used
- ✅ Trial: $1-3 remaining

**Week 3-4:**
- Expected: $4-6 used
- ⚠️ Trial: Running low

**After $5 Trial:**
- Railway will pause your app
- Add payment method to continue
- ~$5-10/month ongoing

### Reduce Costs

**Disable AI Insights:**
- Comment out AI-related code
- Saves ~$5/month on Anthropic API

**Use Render Instead:**
- Free tier (with 15-min sleep)
- Good if you don't mind delays

---

## 📸 Screenshots Reference

### Railway Dashboard

**What you should see:**

1. **Overview Tab:**
   - Green "Active" status
   - Latest deployment time
   - Domain URL

2. **Variables Tab:**
   - AUTH_TOKEN_1 ✅
   - AUTH_TOKEN_2 ✅
   - ANTHROPIC_API_KEY ✅
   - ENVIRONMENT ✅
   - CORS_ORIGINS ✅

3. **Deployments Tab:**
   - Green checkmark on latest
   - "Deployed" status
   - Build logs available

---

## ✅ Deployment Checklist

**Before Deployment:**
- [ ] Tokens generated
- [ ] Repository is PRIVATE on GitHub
- [ ] .env files NOT committed
- [ ] CSV files in data/ folder
- [ ] Tested locally

**During Deployment:**
- [ ] Railway project created
- [ ] All 5 environment variables added
- [ ] CSV data uploaded
- [ ] CORS_ORIGINS updated with real URL
- [ ] Redeployed after CORS update

**After Deployment:**
- [ ] App loads at Railway URL
- [ ] Guest mode works (obfuscated data)
- [ ] Login works with token
- [ ] Real data shows after login
- [ ] AI insights work (if enabled)
- [ ] Logout returns to guest mode
- [ ] Shared access with wife

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ App accessible at Railway URL
✅ HTTPS (lock icon in browser)
✅ Guest mode shows obfuscated amounts
✅ Login works with your token
✅ Real data displays after authentication
✅ Logout returns to obfuscated data
✅ No errors in Railway logs
✅ Using < $0.30/day of trial credits

---

## 🆘 Need Help?

**Railway Support:**
- Docs: [docs.railway.app](https://docs.railway.app)
- Discord: Railway Community
- Email: team@railway.app

**Check Your Logs:**
```
Railway Dashboard → Deployments → Latest → View Logs
```

**Common log errors:**
- "ModuleNotFoundError" → Missing dependency
- "No CSV file found" → Data not uploaded
- "CORS error" → Check CORS_ORIGINS variable

---

## 🎉 Congratulations!

Your Finance Analysis Dashboard is now:
- ✅ Deployed globally on Railway
- ✅ Secured with HTTPS
- ✅ Protected with httpOnly cookies
- ✅ Rate-limited against attacks
- ✅ Accessible from anywhere
- ✅ Data obfuscated for guests

**Next Steps:**
1. Bookmark your Railway URL
2. Add it to your phone home screen
3. Monitor usage in Railway dashboard
4. Enjoy your financial insights! 📊💰

---

**Deployment time:** 15-20 minutes
**Ongoing cost:** $0 (trial) → $5-10/month after
**Difficulty:** Medium 🟡

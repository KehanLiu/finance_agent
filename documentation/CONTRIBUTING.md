# Contributing to AI Financial Advisor Dashboard

Thank you for your interest in contributing! This project was built through "vibe coding" with Claude Code, and we welcome contributions of all kinds.

## 🎯 Ways to Contribute

### 🐛 Report Bugs
- Use [GitHub Issues](https://github.com/yourusername/finance-analysis/issues)
- Include steps to reproduce
- Describe expected vs actual behavior
- Share error messages and logs
- Mention your environment (OS, Python version, Node version)

### 💡 Suggest Features
- Open a GitHub Issue with the `enhancement` label
- Describe the feature and why it's useful
- Include mockups or examples if possible
- Consider if it fits the project's scope

### 📝 Improve Documentation
- Fix typos, clarify instructions
- Add troubleshooting tips
- Create video tutorials
- Translate documentation

### 💻 Submit Code
- Follow the guidelines below
- Keep changes focused (one feature per PR)
- Write clear commit messages
- Test your changes locally

## 🚀 Development Setup

### Prerequisites
- Python 3.13+ with uv
- Node.js 18+
- Git
- Anthropic API key (for testing AI features)

### Setup Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/finance-analysis.git
   cd finance-analysis
   git remote add upstream https://github.com/originalauthor/finance-analysis.git
   ```

2. **Backend Setup**
   ```bash
   cd backend

   # Install uv if needed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies
   uv pip install -e ".[dev]"

   # Create .env file
   cp .env.example .env
   # Edit .env with your keys

   # Generate auth tokens
   python auth.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uv run python main.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

5. **Test Your Changes**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## 📋 Code Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where possible
- Keep functions focused and small
- Add docstrings to public functions
- Use meaningful variable names

**Example:**
```python
def calculate_category_totals(df: pd.DataFrame, is_trusted: bool = True) -> dict:
    """
    Calculate total expenses per category.

    Args:
        df: DataFrame with expense data
        is_trusted: Whether to show real amounts

    Returns:
        Dictionary with category totals
    """
    # Implementation...
```

### JavaScript/React (Frontend)
- Use functional components with hooks
- Keep components small and focused
- Use descriptive component names
- Add PropTypes or TypeScript types
- Follow existing code style

**Example:**
```javascript
function ExpenseCard({ amount, category, date }) {
  return (
    <div className="expense-card">
      <h3>{category}</h3>
      <p>{amount}</p>
      <time>{date}</time>
    </div>
  )
}
```

### CSS
- Use existing CSS variables for colors
- Follow mobile-first responsive design
- Keep selectors specific but not too nested
- Use meaningful class names

## 🔀 Pull Request Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Use prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `style/` - Formatting, no code change

### 2. Make Changes
- Write clean, tested code
- Follow the style guidelines
- Keep commits atomic and focused
- Write clear commit messages

**Good commit messages:**
```
Add retirement projection to AI insights

- Implement savings rate calculation
- Add projection algorithm
- Update AI prompt with retirement context
```

### 3. Test Locally
- Backend: Verify all endpoints work
- Frontend: Test on desktop and mobile
- AI: Test with and without authentication
- Check console for errors

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- **Clear title**: "Add retirement projection feature"
- **Description**: Explain what and why
- **Screenshots**: For UI changes
- **Testing**: How you tested it
- **Related Issues**: Link related issues

### 5. Code Review
- Respond to feedback promptly
- Make requested changes
- Push updates to the same branch
- Mark conversations as resolved

### 6. Merge
Once approved:
- Squash commits if requested
- Maintainer will merge
- Delete your branch after merge

## 🧪 Testing Guidelines

### Manual Testing Checklist
Before submitting, test:
- [ ] Backend starts without errors
- [ ] Frontend loads correctly
- [ ] Login/logout works
- [ ] Guest mode shows obfuscated data
- [ ] Authenticated mode shows real data
- [ ] AI insights work (if changed)
- [ ] Charts render correctly
- [ ] Search functionality works
- [ ] Mobile responsive layout
- [ ] No console errors

### Future: Automated Tests
We plan to add:
- Backend: pytest unit tests
- Frontend: Vitest/React Testing Library
- E2E: Playwright tests
- CI/CD: GitHub Actions

## 🎨 Feature Ideas

Looking for something to work on? Try these:

### Easy (Good First Issues)
- Add more quick questions to AI chat
- Improve mobile styling
- Add dark mode toggle
- Create example CSV datasets
- Add more chart types

### Medium
- Budget tracking and alerts
- Export data to PDF reports
- Add expense categories autocomplete
- Implement data filtering by date range
- Multi-currency conversion improvements

### Advanced
- Direct Toshl API integration
- TradeRepublic / broker integration
- Automated monthly email reports
- Savings goals with progress tracking
- Machine learning for anomaly detection
- Real-time data sync
- Mobile app with React Native

## 🔒 Security

### Reporting Security Issues
**Do NOT open public issues for security vulnerabilities.**

Instead, email: [your-email@example.com]

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We'll respond within 48 hours.

### Security Best Practices
- Never commit `.env` files
- Never log sensitive data
- Use parameterized queries (SQL injection)
- Validate all user inputs
- Keep dependencies updated
- Use HTTPS in production
- Follow OWASP guidelines

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all.

### Expected Behavior
- Be respectful and inclusive
- Give and accept constructive feedback
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

### Enforcement
Violations may result in temporary or permanent ban from the project.

Report issues to: [your-email@example.com]

## 💬 Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Security concerns**: Email privately
- **Feature requests**: Open a GitHub Issue

## 🙏 Thank You!

Every contribution helps make this project better. Whether it's code, documentation, bug reports, or ideas - thank you for being part of this!

---

**Happy coding!** 🚀

*Built with Claude Code - embracing the future of AI-assisted development*

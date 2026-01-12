# Screenshots for GitHub README

This folder contains screenshots used in the main README.md.

## Required Screenshots

Add the following screenshots to make the README complete:

### 1. `dashboard-preview.png`
**Full dashboard view showing:**
- Summary cards (Total Expenses, Income, Net)
- Pie chart (spending by category)
- Bar chart (top tags)
- Line chart (monthly trends)
- Yearly summary table

**Recommended size**: 1200x800px or similar
**Format**: PNG with good compression
**Mode**: Use Guest Mode (randomized data for privacy)

---

### 2. `ai-chat.png`
**Desktop AI chat interface showing:**
- Chat header with "Clear Chat" button
- A few messages back and forth
- AI response with formatted markdown
- Input box with quick questions visible
- Example question like "When can I retire?"

**Recommended size**: 1000x700px
**Format**: PNG
**Mode**: Authenticated mode showing real chat

---

### 3. `ai-chat-mobile.png`
**Mobile view of AI chat:**
- Responsive layout on phone screen
- Compact quick question buttons (2-column grid)
- Chat bubbles optimized for mobile
- Virtual keyboard visible (optional)

**Recommended size**: 375x812px (iPhone size) or similar
**Format**: PNG
**Tip**: Use browser dev tools to simulate mobile

---

### 4. `search.png`
**Search functionality:**
- Search bar with query (e.g., "skiing" or "restaurant")
- Search results showing filtered transactions
- Both expense and income totals
- Transaction list below

**Recommended size**: 1000x600px
**Format**: PNG
**Mode**: Guest Mode for privacy

---

## How to Take Screenshots

### Option 1: Browser Built-in Tools
1. Open your deployed app or local dev server
2. Press `F12` to open DevTools
3. Use responsive mode for mobile screenshots
4. Take screenshot with browser screenshot tool

### Option 2: Screenshot Tools
- **macOS**: Cmd+Shift+4 (select area), Cmd+Shift+5 (full screen)
- **Windows**: Win+Shift+S (Snipping Tool)
- **Linux**: Flameshot, GNOME Screenshot, or `scrot`

### Option 3: Online Tools
- Use [Screely](https://screely.com/) for beautiful browser mockups
- [CleanShot](https://cleanshot.com/) for professional screenshots (macOS)

## Tips for Great Screenshots

1. **Use Guest Mode** for public screenshots (privacy)
2. **Clean data**: Use representative but clean example data
3. **Good contrast**: Ensure text is readable
4. **Proper sizing**: Not too large (slow loading) or small (blurry)
5. **Annotations**: Add arrows/highlights if explaining features
6. **Consistency**: Same browser and theme for all screenshots

## After Adding Screenshots

1. Place PNG files in this `docs/images/` folder
2. Verify they're referenced correctly in README.md:
   ```markdown
   ![Dashboard Preview](docs/images/dashboard-preview.png)
   ```
3. Test links by viewing README on GitHub
4. Compress images if needed: [TinyPNG](https://tinypng.com/)

## Optional: GIF Demos

Consider adding animated GIFs for:
- AI chat interaction (question → response)
- Search functionality
- Login flow
- Mobile responsive transition

**Tools**: [LICEcap](https://www.cockos.com/licecap/), [Kap](https://getkap.co/), [ScreenToGif](https://www.screentogif.com/)

---

**Note**: Screenshots with randomized guest data are perfectly fine and recommended for privacy when sharing publicly on GitHub.

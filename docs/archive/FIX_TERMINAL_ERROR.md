# 🔧 Fix Terminal "ource: command not found" Error

## 🐛 The Error:

```
ource /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH/.venv/bin/activate
zsh: command not found: ource
```

**This appears when you open a new terminal window.**

---

## ✅ THE ISSUE:

There's a typo: `ource` instead of `source` (missing the 's')

This typo is likely in one of these places:
1. Your shell history (found it in `.zsh_history`)
2. A terminal startup command
3. An iTerm2/Terminal profile startup script
4. A direnv configuration
5. A shell alias or function

---

## 🎯 QUICK FIX:

### Option 1: Clear the Problematic History Entry

```bash
# Edit your zsh history to remove the typo
cd ~
# Backup first
cp .zsh_history .zsh_history.backup

# Remove the bad line
sed -i '' '/^: [0-9]*:[0-9]*;ource /d' ~/.zsh_history

# Or manually edit it
nano ~/.zsh_history
# Search for "ource" and delete that line
# Save: Ctrl+O, Enter, Ctrl+X
```

### Option 2: Check Terminal Startup Commands

**If using iTerm2:**
1. Open iTerm2 Preferences (Cmd+,)
2. Go to Profiles → General
3. Look at "Send text at start"
4. Remove or fix any command with `ource`

**If using Terminal.app:**
1. Terminal → Preferences → Profiles
2. Select your profile → Shell
3. Check "Run command" or "Run inside shell"
4. Remove or fix any command with `ource`

### Option 3: Check for direnv

```bash
# Check if you have direnv configured
which direnv

# If yes, check for .envrc files
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai
find . -name ".envrc" -exec cat {} \;

# If any have "ource", edit them:
# nano AI_NEWS_LANGGRAPH/.envrc
```

---

## 🚀 PROPER WAY TO ACTIVATE VENV:

Instead of the typo, use the correct command:

```bash
# Navigate to project
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Activate virtual environment (correct spelling!)
source .venv/bin/activate

# Or create an alias in ~/.zshrc
echo 'alias activate-ai="cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH && source .venv/bin/activate"' >> ~/.zshrc

# Then reload
source ~/.zshrc

# Now just type:
activate-ai
```

---

## 📋 COMPREHENSIVE CHECK:

Run these commands to find where the typo might be:

```bash
# Check all shell config files
grep -r "ource" ~/.zshrc ~/.zprofile ~/.zshenv ~/.zlogin ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null

# Check project directory
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH
find . -name ".*" -type f -exec grep -l "ource" {} \; 2>/dev/null

# Check parent directories
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai
find . -name ".envrc" -o -name ".autoenv" -exec cat {} \; 2>/dev/null
```

---

## ✅ RECOMMENDED SETUP:

Create a clean alias for your project:

```bash
# Add to ~/.zshrc
cat >> ~/.zshrc << 'EOF'

# AI News LangGraph Project
alias ai-news='cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH && source .venv/bin/activate'
alias ai-streamlit='cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH && source .venv/bin/activate && streamlit run streamlit_newsletter_app.py'
EOF

# Reload
source ~/.zshrc

# Now use:
ai-news          # Go to project & activate venv
ai-streamlit     # Start Streamlit directly
```

---

## 🔍 IF ERROR PERSISTS:

### Check Terminal Application Settings:

**iTerm2:**
```
1. iTerm2 → Preferences (Cmd+,)
2. Profiles → General → Command
   - Make sure it's set to "Login shell" not "Command"
3. Profiles → General → Send text at start
   - Should be empty or correct
4. Profiles → Keys → Key Mappings
   - Check for any auto-execute keys
```

**Terminal.app:**
```
1. Terminal → Preferences
2. Profiles → (Your Profile)
3. Shell tab → Startup
   - Should be "Default login shell"
   - Check "Run command" is unchecked or correct
```

### Check for Auto-CD Tools:

```bash
# Check if you have z, autojump, or similar
which z
which autojump
which fasd

# These are fine, but might have configs
cat ~/.z 2>/dev/null
cat ~/.autojump 2>/dev/null
```

---

## 🎯 IMMEDIATE WORKAROUND:

If you can't find the source of the error but need to work now:

```bash
# Add this to ~/.zshrc to suppress the error
function ource() {
    echo "⚠️  Typo detected: 'ource' → 'source'"
    echo "✅  Fixing automatically..."
    source "$@"
}

# Reload
source ~/.zshrc
```

Now the typo will be auto-corrected! But you should still find and fix the root cause.

---

## 📊 MOST LIKELY CAUSES:

### 1. Terminal Startup Command (90% chance)
Your terminal emulator has a startup command with the typo.

**Fix:**
- Check iTerm2/Terminal preferences
- Look for "Run command" or "Send text at start"

### 2. Shell History Auto-Execute (5% chance)
Some tool is re-running the last command from history.

**Fix:**
- Remove from `.zsh_history`
- Check for auto-execute plugins

### 3. direnv or autoenv (5% chance)
A `.envrc` file has the typo.

**Fix:**
- Find and edit `.envrc` files
- Remove `ource`, replace with `source`

---

## ✅ VERIFICATION:

After fixing:

```bash
# Close all terminal windows
# Open a new terminal
# You should NOT see the error!

# If you still see it:
echo "Error persists, checking more locations..."
set -x  # Enable debug mode
# The next error will show exactly where it's coming from
```

---

## 📚 RELATED DOCS:

- `DATE_FIX_COMPLETE.md` - Date parsing fix
- `ERRORS_FIXED.md` - All error fixes
- `FINAL_SOLUTION.md` - Complete solution

---

## 💡 PREVENTION:

To avoid typos in the future:

```bash
# Add this to ~/.zshrc for safety
alias ource='echo "⚠️ Typo! Did you mean: source" && source'

# Tab completion will help
# Type: sou<TAB> and it completes to 'source'
```

---

**Most likely fix: Check your terminal's startup command settings!** 🎯

The typo is probably in iTerm2 Preferences → Profiles → General → "Send text at start"


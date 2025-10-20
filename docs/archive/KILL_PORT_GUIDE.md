# 🔧 How to Kill Processes on Port 8501 (or Any Port)

## 🎯 Quick Methods (Choose One)

### Method 1: One-Line Kill (Easiest) ⭐
```bash
kill -9 $(lsof -ti:8501)
```

### Method 2: Kill All Streamlit
```bash
pkill -9 streamlit
```

### Method 3: Kill Specific Processes
```bash
# First, find the PIDs
lsof -ti:8501

# Then kill them (replace XXXX with actual PIDs)
kill -9 XXXX YYYY
```

---

## 📋 Step-by-Step Guide

### Step 1: Find What's Running on Port 8501
```bash
lsof -ti:8501
```

**Output Example:**
```
82327
96156
```
These are Process IDs (PIDs).

---

### Step 2: Kill the Processes

#### Option A: Kill All at Once (Recommended)
```bash
kill -9 $(lsof -ti:8501)
```

#### Option B: Kill Individually
```bash
kill -9 82327
kill -9 96156
```

#### Option C: Kill All Streamlit Processes
```bash
pkill -9 streamlit
```

---

### Step 3: Verify Port is Free
```bash
lsof -ti:8501
```

**Expected Output:**
```
(nothing - port is free)
```

---

## 🛠️ Complete Commands

### All-in-One Command (Copy & Paste)
```bash
# Find, kill, and verify
echo "Finding processes on port 8501..." && \
lsof -ti:8501 && \
echo "Killing processes..." && \
kill -9 $(lsof -ti:8501) 2>/dev/null && \
sleep 1 && \
echo "Verifying port is free..." && \
if lsof -ti:8501 > /dev/null 2>&1; then \
  echo "❌ Port still occupied"; \
else \
  echo "✅ Port 8501 is now free!"; \
fi
```

---

## 🚨 If Processes Won't Die

### Nuclear Option 1: Kill by Name
```bash
pkill -9 -f streamlit
```

### Nuclear Option 2: Kill Python Processes
```bash
pkill -9 python
```
⚠️ **Warning**: This kills ALL Python processes!

### Nuclear Option 3: Use Activity Monitor (GUI)
1. Open **Activity Monitor** (Cmd + Space, type "Activity Monitor")
2. Search for "streamlit" or "python"
3. Select the process
4. Click the **X** button (Quit Process)
5. Choose "Force Quit"

### Nuclear Option 4: Restart Terminal
Close and reopen your terminal window.

---

## 💡 Best Practices

### Before Starting Streamlit:
```bash
# Always check if port is free first
lsof -ti:8501

# If occupied, kill it
kill -9 $(lsof -ti:8501)

# Then start Streamlit
streamlit run streamlit_newsletter_app.py
```

### Create an Alias (Optional):
Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Kill port 8501
alias kill8501='kill -9 $(lsof -ti:8501) 2>/dev/null && echo "✅ Port 8501 freed"'

# Kill all Streamlit
alias killstreamlit='pkill -9 streamlit && echo "✅ All Streamlit processes killed"'
```

Then reload:
```bash
source ~/.zshrc
```

Now you can just type:
```bash
kill8501
```

---

## 🔍 Understanding the Commands

### `lsof -ti:8501`
- `lsof` = List Open Files
- `-t` = Terse output (PIDs only)
- `-i:8501` = Network connections on port 8501

### `kill -9 PID`
- `kill` = Send signal to process
- `-9` = SIGKILL (force kill, cannot be ignored)
- `PID` = Process ID to kill

### `pkill -9 streamlit`
- `pkill` = Kill processes by name
- `-9` = Force kill signal
- `streamlit` = Match processes with "streamlit" in name

### `$(command)`
- Executes command and uses its output
- `$(lsof -ti:8501)` gets PIDs and passes them to kill

---

## 📊 Troubleshooting Decision Tree

```
Is port 8501 occupied?
│
├─ YES → Try Method 1: kill -9 $(lsof -ti:8501)
│   │
│   ├─ Still occupied? → Try Method 2: pkill -9 streamlit
│   │   │
│   │   ├─ Still occupied? → Restart terminal
│   │   └─ Free? ✅ Done!
│   │
│   └─ Free? ✅ Done!
│
└─ NO → Port is free, start Streamlit!
```

---

## 🎯 Quick Reference Card

| Task | Command |
|------|---------|
| **Check port** | `lsof -ti:8501` |
| **Kill port** | `kill -9 $(lsof -ti:8501)` |
| **Kill Streamlit** | `pkill -9 streamlit` |
| **Verify free** | `lsof -ti:8501` (should return nothing) |
| **Start Streamlit** | `streamlit run streamlit_newsletter_app.py` |

---

## 📝 Complete Workflow

### Safe Workflow (Copy-Paste This):
```bash
#!/bin/bash

echo "🔍 Checking port 8501..."
if lsof -ti:8501 > /dev/null 2>&1; then
  echo "❌ Port 8501 is occupied"
  echo "🔨 Killing processes..."
  kill -9 $(lsof -ti:8501) 2>/dev/null
  sleep 1
  
  if lsof -ti:8501 > /dev/null 2>&1; then
    echo "⚠️  Still occupied, trying pkill..."
    pkill -9 streamlit
    sleep 1
  fi
fi

echo "✅ Port 8501 is free!"
echo "🚀 Starting Streamlit..."
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH
streamlit run streamlit_newsletter_app.py
```

Save as `start_streamlit.sh`, then:
```bash
chmod +x start_streamlit.sh
./start_streamlit.sh
```

---

## 💻 For Your Specific Case

### Right Now, Run This:
```bash
# Kill processes on port 8501
kill -9 $(lsof -ti:8501) 2>/dev/null

# Kill all Streamlit processes
pkill -9 streamlit 2>/dev/null

# Wait a moment
sleep 2

# Verify port is free
if lsof -ti:8501 > /dev/null 2>&1; then
  echo "❌ Port still occupied - restart terminal"
else
  echo "✅ Port 8501 is free! Start Streamlit now:"
  echo "   streamlit run streamlit_newsletter_app.py"
fi
```

---

## 🚀 Ready to Start

Once port is free:
```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH
streamlit run streamlit_newsletter_app.py
```

Open browser at: http://localhost:8501

---

## ⚡ TL;DR (Too Long, Didn't Read)

**Just run these 3 commands:**
```bash
# 1. Kill port 8501
kill -9 $(lsof -ti:8501)

# 2. Kill all Streamlit
pkill -9 streamlit

# 3. Start app
streamlit run streamlit_newsletter_app.py
```

**Done!** 🎉


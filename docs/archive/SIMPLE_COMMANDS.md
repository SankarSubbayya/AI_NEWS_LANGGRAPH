# 🚀 Simple Commands for Streamlit App

## ⚡ Kill Port 8501 (One-Liner with Pipe)

### **Simplest Method:**
```bash
lsof -ti:8501 | xargs kill -9
```

### **With Success Message:**
```bash
lsof -ti:8501 | xargs kill -9 && echo "✅ Port 8501 is free!"
```

### **With Error Handling:**
```bash
lsof -ti:8501 | xargs kill -9 2>/dev/null && echo "✅ Killed!" || echo "✅ Already free"
```

---

## 🎯 Complete Workflow (Copy & Paste)

```bash
# Kill port 8501
lsof -ti:8501 | xargs kill -9

# Start Streamlit
streamlit run streamlit_newsletter_app.py
```

---

## 📋 How the Pipe Works

```
lsof -ti:8501    →    82327    →    xargs kill -9
                      96156
```

**Breakdown:**
1. `lsof -ti:8501` → Finds PIDs on port 8501
2. `|` (pipe) → Passes output to next command
3. `xargs` → Takes input and uses it as arguments
4. `kill -9` → Kills each PID

---

## 🔄 Alternative One-Liners

### Method 1: Using Pipe (Recommended)
```bash
lsof -ti:8501 | xargs kill -9
```

### Method 2: Using Command Substitution
```bash
kill -9 $(lsof -ti:8501)
```

### Method 3: Kill All Streamlit
```bash
pkill -9 streamlit
```

---

## ✅ The Fix Applied

**Error Fixed:**
```
NameError: name 'use_sample_data' is not defined
```

**What Changed:**
- Removed references to old `use_sample_data` variable
- Now uses `data_source` radio button instead
- App is ready to run!

---

## 🚀 Start App Now

```bash
# 1. Kill port (if needed)
lsof -ti:8501 | xargs kill -9

# 2. Start app
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH
streamlit run streamlit_newsletter_app.py
```

**Opens at:** http://localhost:8501

---

## 🎯 What You'll See

**In Sidebar:**
- **Data Source Options:**
  1. ✅ **Config File Topics (Real)** - Your 5 topics from JSON
  2. Sample Demo Data - 3 quick demo topics  
  3. Custom Input - Manual entry

**Your 5 Real Topics:**
1. 🔬 Cancer Research
2. 🛡️ Cancer Prevention
3. 🔍 Early Detection and Diagnosis
4. 💊 Treatment Planning
5. 🧪 Clinical Trials

---

## 💡 Quick Tips

**Check if port is free:**
```bash
lsof -ti:8501
```
- Returns nothing → Port is free ✅
- Returns numbers → Port is occupied, run kill command

**Stop Streamlit:**
```
Press Ctrl+C in terminal
```

**Force quit everything:**
```bash
pkill -9 streamlit
```

---

## 📝 Summary

| Task | Command |
|------|---------|
| **Kill port** | `lsof -ti:8501 \| xargs kill -9` |
| **Start app** | `streamlit run streamlit_newsletter_app.py` |
| **Check port** | `lsof -ti:8501` |
| **Stop app** | `Ctrl+C` |

---

**Ready! Run this now:**
```bash
lsof -ti:8501 | xargs kill -9 && streamlit run streamlit_newsletter_app.py
```

This kills the port AND starts the app in one command! 🚀


# 🧹 Code Cleanup Recommendations

Based on unused function analysis performed on October 19, 2025.

---

## ✅ Confirmed Unused Functions (Safe to Remove)

### `src/ai_news_langgraph/tools.py`

#### 1. `search_academic_papers()` (Line ~310)
**Status:** ❌ **CONFIRMED UNUSED**

**Evidence:**
```bash
$ grep -r "search_academic_papers" src/ tests/
# Result: 0 matches (except definition)
```

**Recommendation:** **REMOVE**

**Reason:** This function has zero references in the codebase. It's likely been replaced by newer implementations in `tools_cancer_news.py` or `tools_direct.py`.

---

#### 2. `search_news()` (Line ~295)
**Status:** ⚠️ **LIKELY UNUSED**

**Evidence:**
```bash
$ grep -rn "search_news" src/ tests/
# Results: Only found in:
#  - String literals (tool names)
#  - _search_newsapi (different function)
#  - No actual function calls
```

**Recommendation:** **REVIEW THEN REMOVE**

**Reason:** No actual calls to this function. The matches are:
- Tool name strings: `"search_news"` (metadata, not calls)
- Different function: `_search_newsapi()` (internal method)

**Action:**
1. Confirm it's not used in any configuration
2. Check if it's part of a tool interface
3. If confirmed, remove it

---

#### 3. `save_output_file()` (Line ~340)
**Status:** ⚠️ **POTENTIALLY UNUSED**

**Recommendation:** **REVIEW**

**Reason:** Utility function that may be used in:
- Scripts (outside main codebase)
- Debugging
- Manual testing

**Action:**
- Check if used in any scripts in root directory
- If not, remove it

---

#### 4. `load_json()` (Line ~285)
**Status:** ⚠️ **POTENTIALLY UNUSED**

**Recommendation:** **REVIEW**

**Reason:** Static utility method. May be:
- Part of a base class interface
- Used for testing
- Reserved for future use

**Action:**
- Check if it's implementing an interface
- If standalone utility, consider removing

---

## ✅ Functions to KEEP (False Positives)

### Property Methods (Keep All)

1. **`nodes_v2.py: llm()`** ✅
   - `@property` method - called as `self.llm` not `self.llm()`
   
2. **`task_loader.py: tasks()`** ✅
   - `@property` method - called as `obj.tasks`

### API Functions (Keep All)

3. **`observability.py: start_observability()`** ✅
   - Public API function
   - May be called dynamically or from config

4. **`visualizations.py: create_timeline_chart()`** ✅
   - Feature function
   - May be called dynamically

### Test Fixtures (Keep All)

5. **All `@pytest.fixture` functions** ✅
   - `test_nodes_v2.py: mock_llm()`
   - `test_nodes_v2.py: mock_news_tool()`
   - `test_nodes_v2.py: workflow_nodes()`
   - `test_prompts.py: optimizer()`

---

## 🎯 Recommended Cleanup Steps

### Step 1: Safe Removal (Immediate)

```python
# In src/ai_news_langgraph/tools.py

# ❌ REMOVE THIS:
def search_academic_papers(query: str, ...):
    """Search academic papers."""
    # ... implementation ...
    pass
```

**Why:** Zero references in codebase.

---

### Step 2: Verify and Remove

```bash
# Double-check these functions aren't used in configs
grep -r "search_news" . --include="*.yaml" --include="*.json"
grep -r "save_output_file" . --include="*.yaml" --include="*.json"
grep -r "load_json" . --include="*.yaml" --include="*.json"
```

If no matches, remove:
- `search_news()`
- `save_output_file()`
- `load_json()`

---

### Step 3: Test After Removal

```bash
# Run all tests to ensure nothing breaks
pytest tests/ -v

# Run the main workflow
python -m ai_news_langgraph.workflow
```

---

## 📊 Expected Impact

**Lines to Remove:** ~60-80 lines

**Files Affected:** 1 file (`tools.py`)

**Risk Level:** 🟢 **LOW**

**Benefits:**
- ✅ Cleaner codebase
- ✅ Reduced maintenance
- ✅ Less confusion for new developers
- ✅ Faster code navigation

---

## 🔍 Why These Functions Became Unused

### Evolution of the Codebase

The codebase has evolved from:

**Old architecture:**
```python
# tools.py (old)
def search_news(query):
    # Generic news search
    pass

def search_academic_papers(query):
    # Generic academic search
    pass
```

**New architecture:**
```python
# tools_cancer_news.py (new)
class CancerNewsSearchTool:
    def fetch_cancer_news(self, topic):
        # Specialized cancer news search
        pass

# tools_direct.py (new)
class DirectNewsSearchTool:
    # More focused implementation
    pass
```

**Result:** Old generic functions in `tools.py` became obsolete.

---

## ✅ Cleanup Checklist

- [ ] **Backup current code** (git commit)
- [ ] **Remove `search_academic_papers()`** from `tools.py`
- [ ] **Verify `search_news()` not in configs**
- [ ] **Remove `search_news()`** if confirmed unused
- [ ] **Review `save_output_file()`** usage
- [ ] **Remove `save_output_file()`** if unused
- [ ] **Review `load_json()`** usage
- [ ] **Remove `load_json()`** if unused
- [ ] **Run full test suite**
- [ ] **Update documentation** if needed
- [ ] **Commit changes** with clear message

---

## 📝 Git Commit Message Template

```bash
git commit -m "refactor: remove unused functions from tools.py

Removed:
- search_academic_papers() - replaced by specialized tools
- search_news() - replaced by tools_cancer_news.py
- save_output_file() - unused utility function
- load_json() - unused utility function

Impact: Low risk - these functions have zero references in codebase
Tests: All tests passing after removal

Closes #XXX"
```

---

## 🎓 Lessons Learned

**To prevent unused code accumulation:**

1. **Regular Code Audits**
   - Run `find_unused_functions.py` quarterly
   - Review before major releases

2. **Deprecation Process**
   - Mark old functions as deprecated
   - Add warnings before removal
   - Document migration path

3. **Better Testing**
   - Maintain high test coverage
   - Tests will fail if removing used code

4. **Documentation**
   - Keep API docs current
   - Document when functions are replaced

5. **Code Reviews**
   - Flag unused code in PRs
   - Ask "Is this still needed?" regularly

---

## 📈 Future Maintenance

**Schedule:**
- **Monthly:** Quick scan for obvious unused code
- **Quarterly:** Run full `find_unused_functions.py` analysis
- **Before major releases:** Thorough cleanup review

**Tools:**
```bash
# Quick scan
./find_unused_functions.py > unused_report.txt

# Detailed analysis
python -m coverage report
python -m vulture src/
```

---

**Analysis Date:** October 19, 2025

**Next Review:** January 2026

**Status:** Ready for cleanup


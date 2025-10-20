# 🔍 Unused Functions Analysis Report

Generated: October 19, 2025

---

## 📊 Summary

| Metric | Count |
|--------|-------|
| **Total Functions** | 396 |
| **Special Methods** | 31 (skipped) |
| **Used Functions** | 351 |
| **Unused Functions** | 14 |

---

## ⚠️ Potentially Unused Functions (14)

### 1. `src/ai_news_langgraph/nodes_v2.py`

#### `llm()` (Line 104) - **KEEP**
```python
@property
def llm(self):
    """Lazy initialization of LLM (only when needed)."""
```

**Status:** ✅ **KEEP - Property Method**

**Reason:** This is a `@property` decorator method. It's called as `self.llm` (without parentheses), so the pattern search doesn't detect it. This is actively used for lazy LLM initialization.

**Action:** No action needed.

---

### 2. `src/ai_news_langgraph/observability.py`

#### `start_observability()` (Line 432) - **KEEP**
```python
def start_observability():
    """Start observability system."""
```

**Status:** ✅ **KEEP - API Function**

**Reason:** This is a public API function that may be called dynamically or from configuration. Phoenix observability can be started manually.

**Action:** No action needed. Consider adding to `__all__` export list.

---

### 3. `src/ai_news_langgraph/task_loader.py`

#### `tasks()` (Line 41) - **KEEP**
```python
@property
def tasks(self):
    """Get tasks configuration."""
```

**Status:** ✅ **KEEP - Property Method**

**Reason:** Another `@property` method. Called as `obj.tasks` not `obj.tasks()`.

**Action:** No action needed.

---

### 4. `src/ai_news_langgraph/tools.py`

#### `load_json()` (Line 285) - **REVIEW**
```python
@staticmethod
def load_json(file_path: str) -> Dict:
```

**Status:** ⚠️ **REVIEW**

**Reason:** Utility method that might be used indirectly or reserved for future use.

**Action:** 
- Check if this is part of a base class interface
- If truly unused, consider removing
- Alternative: Mark as deprecated

---

#### `search_news()` (Line 295) - **LIKELY UNUSED**
```python
def search_news(query: str, ...):
```

**Status:** ❌ **LIKELY UNUSED**

**Reason:** This appears to be an old implementation that's been replaced by other search tools.

**Action:** 
- Verify it's not imported/used anywhere
- If unused, remove it
- Check git history to confirm it's replaced

---

#### `search_academic_papers()` (Line 310) - **LIKELY UNUSED**
```python
def search_academic_papers(query: str, ...):
```

**Status:** ❌ **LIKELY UNUSED**

**Reason:** Similar to `search_news`, this may be an old implementation.

**Action:**
- Check if there's a newer implementation
- If replaced, remove this function
- Document the replacement if removing

---

#### `save_output_file()` (Line 340) - **REVIEW**
```python
def save_output_file(content: str, ...):
```

**Status:** ⚠️ **REVIEW**

**Reason:** Utility function for saving outputs. May be used in scripts or CLI.

**Action:**
- Check if used in any scripts outside main codebase
- Consider if it's needed for debugging
- If unused, remove it

---

### 5. `src/ai_news_langgraph/visualizations.py`

#### `create_timeline_chart()` (Line 169) - **KEEP**
```python
@staticmethod
def create_timeline_chart(articles, ...):
```

**Status:** ✅ **KEEP - Feature Function**

**Reason:** This is a chart generation feature that may be called dynamically or used in different modes.

**Action:** 
- Add usage example in docs
- Consider exposing in API if not already
- No removal needed

---

### 6. Test Files

#### `tests/test_nodes_v2.py`

**`mock_llm()` (Line 22) - KEEP**
```python
@pytest.fixture
def mock_llm(self):
```

**Status:** ✅ **KEEP - Pytest Fixture**

**Reason:** This is a pytest fixture. Fixtures are used by pytest automatically when named in test function parameters. The script doesn't detect this pattern.

**Action:** No action needed.

---

**`mock_news_tool()` (Line 29) - KEEP**
```python
@pytest.fixture
def mock_news_tool(self):
```

**Status:** ✅ **KEEP - Pytest Fixture**

**Reason:** Another pytest fixture.

**Action:** No action needed.

---

**`workflow_nodes()` (Line 51) - KEEP**
```python
@pytest.fixture
def workflow_nodes(self):
```

**Status:** ✅ **KEEP - Pytest Fixture**

**Reason:** Pytest fixture.

**Action:** No action needed.

---

#### `tests/test_prompts.py`

**`optimizer()` (Line 182) - KEEP**
```python
@pytest.fixture
def optimizer(self):
```

**Status:** ✅ **KEEP - Pytest Fixture**

**Reason:** Pytest fixture.

**Action:** No action needed.

---

#### `tests/test_state.py`

**`sample_workflow_state()` (Line 292) - REVIEW**
```python
def sample_workflow_state():
```

**Status:** ⚠️ **REVIEW**

**Reason:** May be a test utility or unused fixture.

**Action:** 
- Check if it's a fixture without decorator
- If unused in tests, consider removing
- Or add `@pytest.fixture` if it should be a fixture

---

**`sample_articles()` (Line 306) - REVIEW**
```python
def sample_articles():
```

**Status:** ⚠️ **REVIEW**

**Reason:** Test utility function.

**Action:**
- Similar to above - check usage
- Add fixture decorator if needed
- Remove if truly unused

---

## 🎯 Recommended Actions

### High Priority (Remove if Confirmed Unused)

1. **`tools.py`:**
   - ❌ Remove `search_news()` (line 295)
   - ❌ Remove `search_academic_papers()` (line 310)
   - ⚠️ Review `save_output_file()` (line 340)
   - ⚠️ Review `load_json()` (line 285)

### Medium Priority (Review)

2. **Test files:**
   - Review `sample_workflow_state()` - add fixture decorator or remove
   - Review `sample_articles()` - add fixture decorator or remove

### Low Priority (Keep)

3. **Property methods:**
   - ✅ Keep `nodes_v2.py: llm()`
   - ✅ Keep `task_loader.py: tasks()`

4. **API/Feature functions:**
   - ✅ Keep `observability.py: start_observability()`
   - ✅ Keep `visualizations.py: create_timeline_chart()`

5. **Test fixtures:**
   - ✅ Keep all `@pytest.fixture` decorated functions

---

## 📝 Action Plan

### Step 1: Verify Unused Functions

```bash
# Search for each function to confirm it's not used
grep -r "search_news" src/ tests/
grep -r "search_academic_papers" src/ tests/
grep -r "save_output_file" src/ tests/
grep -r "load_json" src/ tests/
```

### Step 2: Check Git History

```bash
# See when these functions were last modified
git log --oneline -- src/ai_news_langgraph/tools.py
```

### Step 3: Safe Removal

For confirmed unused functions:

1. **Add deprecation warning first** (if public API):
   ```python
   import warnings
   
   def search_news(...):
       warnings.warn(
           "search_news is deprecated and will be removed",
           DeprecationWarning
       )
   ```

2. **Wait one release cycle**

3. **Remove completely**

---

## 🔍 False Positives Explained

**Why some functions appear unused but aren't:**

1. **Property Methods** (`@property`)
   - Called without parentheses: `obj.llm` not `obj.llm()`
   - Script searches for `function_name()` pattern

2. **Pytest Fixtures** (`@pytest.fixture`)
   - Used by pytest framework automatically
   - Not called explicitly in code

3. **Dynamic Calls**
   - `getattr(obj, 'function_name')()`
   - Loaded via configuration
   - Called through reflection

4. **Public API Functions**
   - May be imported by external code
   - Entry points for CLI or plugins

---

## ✅ Clean Up Checklist

- [ ] Review `tools.py` functions
- [ ] Check `search_news()` usage
- [ ] Check `search_academic_papers()` usage
- [ ] Check `save_output_file()` usage
- [ ] Check `load_json()` usage
- [ ] Review test utility functions
- [ ] Add fixture decorators if needed
- [ ] Update documentation if removing functions
- [ ] Run all tests after removal
- [ ] Update `__all__` exports if needed

---

## 📊 Impact Assessment

**If you remove the 4 main candidates:**

| Function | Lines | Impact |
|----------|-------|--------|
| `search_news()` | ~15 | Low - likely replaced |
| `search_academic_papers()` | ~30 | Low - likely replaced |
| `save_output_file()` | ~10 | Low - utility function |
| `load_json()` | ~5 | Low - utility function |
| **Total** | **~60 lines** | **Low risk** |

**Benefits:**
- ✅ Cleaner codebase
- ✅ Reduced maintenance burden
- ✅ Less confusion for developers
- ✅ Faster code navigation

---

## 🎓 Best Practices

**To prevent unused code accumulation:**

1. **Regular audits** - Run this analysis quarterly
2. **Code reviews** - Flag unused code in PRs
3. **Deprecation process** - Deprecate before removing
4. **Documentation** - Keep API docs in sync
5. **Testing** - Remove tests for removed functions

---

**Generated by:** `find_unused_functions.py`

**Next Review:** January 2026


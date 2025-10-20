#!/usr/bin/env python3
"""Find unused functions in the codebase."""

import os
import re
from pathlib import Path
from collections import defaultdict

def find_python_files(directory):
    """Find all Python files in directory."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip common directories
        dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', '__pycache__', '.git', 'site', 'node_modules']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_functions(file_path):
    """Extract function definitions from a Python file."""
    functions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match function definitions: def function_name(
            # Capture: function name, whether it's a method (has self/cls), and line number
            for match in re.finditer(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content, re.MULTILINE):
                func_name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                
                # Check if it's a special method
                is_special = func_name.startswith('__') and func_name.endswith('__')
                
                # Get the line to check if it's a method
                lines = content.split('\n')
                func_line = lines[line_num - 1] if line_num <= len(lines) else ""
                
                # Check indentation to determine if it's a method
                is_method = bool(re.match(r'\s+def\s+', func_line))
                
                functions.append({
                    'name': func_name,
                    'file': file_path,
                    'line': line_num,
                    'is_special': is_special,
                    'is_method': is_method
                })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return functions

def search_function_usage(func_name, all_files, exclude_file=None):
    """Search for function usage across all files."""
    usages = []
    # Pattern to match function calls
    patterns = [
        rf'\b{func_name}\s*\(',  # Direct call: func_name(
        rf'\.{func_name}\s*\(',  # Method call: obj.func_name(
        rf'import\s+.*{func_name}',  # Import: from x import func_name
        rf'from\s+\S+\s+import\s+.*{func_name}',  # Import
    ]
    
    for file_path in all_files:
        if file_path == exclude_file:
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern in patterns:
                    if re.search(pattern, content):
                        # Count occurrences
                        matches = re.findall(pattern, content)
                        usages.append({
                            'file': file_path,
                            'count': len(matches)
                        })
                        break  # Found usage in this file
        except Exception as e:
            pass
    return usages

def main():
    """Main analysis function."""
    print("=" * 80)
    print("UNUSED FUNCTION ANALYSIS")
    print("=" * 80)
    print()
    
    # Find all Python files
    src_dir = "src/ai_news_langgraph"
    all_files = find_python_files(".")
    
    print(f"📁 Scanning {len(all_files)} Python files...")
    print()
    
    # Extract all functions
    all_functions = []
    for file_path in all_files:
        functions = extract_functions(file_path)
        all_functions.extend(functions)
    
    print(f"🔍 Found {len(all_functions)} function definitions")
    print()
    
    # Categorize functions
    unused_functions = []
    used_functions = []
    special_methods = []
    
    for func in all_functions:
        # Skip special methods (__init__, __str__, etc.)
        if func['is_special']:
            special_methods.append(func)
            continue
        
        # Search for usage
        usages = search_function_usage(func['name'], all_files, exclude_file=func['file'])
        
        # Also check usage in the same file (but different location)
        try:
            with open(func['file'], 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                # Remove the definition line
                lines[func['line'] - 1] = ''
                content_without_def = '\n'.join(lines)
                # Check if function is called elsewhere in the same file
                if re.search(rf'\b{func["name"]}\s*\(', content_without_def):
                    usages.append({'file': func['file'], 'count': 1})
        except:
            pass
        
        if usages:
            used_functions.append({'func': func, 'usages': usages})
        else:
            unused_functions.append(func)
    
    # Report unused functions
    if unused_functions:
        print("=" * 80)
        print(f"⚠️  POTENTIALLY UNUSED FUNCTIONS ({len(unused_functions)})")
        print("=" * 80)
        print()
        
        # Group by file
        by_file = defaultdict(list)
        for func in unused_functions:
            by_file[func['file']].append(func)
        
        for file_path in sorted(by_file.keys()):
            funcs = by_file[file_path]
            rel_path = os.path.relpath(file_path)
            print(f"📄 {rel_path}")
            for func in funcs:
                method_type = " (method)" if func['is_method'] else ""
                print(f"   Line {func['line']:4d}: {func['name']}(){method_type}")
            print()
    else:
        print("✅ No unused functions found!")
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total functions:       {len(all_functions)}")
    print(f"Special methods:       {len(special_methods)} (skipped)")
    print(f"Used functions:        {len(used_functions)}")
    print(f"Unused functions:      {len(unused_functions)}")
    print()
    
    if unused_functions:
        print("⚠️  Note: Some 'unused' functions may be:")
        print("  • API/public interface functions")
        print("  • Callback functions")
        print("  • Dynamically called via getattr/import")
        print("  • Entry points or CLI commands")
        print("  • Test utility functions")
        print()
        print("Review each before removing!")
    
    print("=" * 80)

if __name__ == "__main__":
    main()


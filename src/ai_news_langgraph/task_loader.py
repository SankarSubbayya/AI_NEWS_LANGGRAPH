"""Utility for loading task configurations from YAML."""

import os
import yaml
import time
import signal
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from functools import wraps
from .schemas import TaskConfig


class TimeoutError(Exception):
    """Raised when task execution times out."""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeout."""
    raise TimeoutError("Task execution timed out")


class TaskLoader:
    """Loads and manages task configurations from YAML."""
    
    def __init__(self, tasks_file: Optional[str] = None):
        """Initialize task loader.
        
        Args:
            tasks_file: Path to tasks YAML file. If None, uses default location.
        """
        if tasks_file is None:
            # Default to tasks.yaml in config directory
            config_dir = Path(__file__).parent / "config"
            tasks_file = config_dir / "tasks.yaml"
        
        self.tasks_file = Path(tasks_file)
        self._tasks = None
    
    @property
    def tasks(self) -> Dict:
        """Lazy load tasks from YAML file."""
        if self._tasks is None:
            self._tasks = self._load_tasks()
        return self._tasks
    
    def _load_tasks(self) -> Dict:
        """Load tasks from YAML file."""
        if not self.tasks_file.exists():
            raise FileNotFoundError(f"Tasks file not found: {self.tasks_file}")
        
        with open(self.tasks_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_task_config(self, task_name: str) -> TaskConfig:
        """Get TaskConfig for a specific task.
        
        Args:
            task_name: Name of the task
        
        Returns:
            TaskConfig object
        
        Raises:
            KeyError: If task not found
        """
        if task_name not in self.tasks:
            available = list(self.tasks.keys())
            raise KeyError(
                f"Task '{task_name}' not found in configuration. "
                f"Available tasks: {available}"
            )
        
        task_data = self.tasks[task_name]
        
        # Build TaskConfig from YAML data
        return TaskConfig(
            name=task_name,
            description=task_data.get('description', ''),
            agent=task_data.get('agent', 'unknown'),
            agent_class=task_data.get('agent_class'),
            dependencies=task_data.get('dependencies', []),
            expected_output=task_data.get('expected_output', ''),
            timeout_seconds=task_data.get('timeout_seconds', 300),
            retry_count=task_data.get('retry_count', 1)
        )
    
    def get_description(self, task_name: str) -> str:
        """Get task description.
        
        Args:
            task_name: Name of the task
        
        Returns:
            Description string
        """
        try:
            return self.tasks[task_name].get('description', 'No description available')
        except KeyError:
            return f"Task '{task_name}' not found"
    
    def get_agent(self, task_name: str) -> str:
        """Get agent responsible for task.
        
        Args:
            task_name: Name of the task
        
        Returns:
            Agent name
        """
        try:
            return self.tasks[task_name].get('agent', 'unknown')
        except KeyError:
            return 'unknown'
    
    def get_dependencies(self, task_name: str) -> List[str]:
        """Get task dependencies.
        
        Args:
            task_name: Name of the task
        
        Returns:
            List of dependency task names
        """
        try:
            return self.tasks[task_name].get('dependencies', [])
        except KeyError:
            return []
    
    def get_timeout(self, task_name: str) -> int:
        """Get task timeout in seconds.
        
        Args:
            task_name: Name of the task
        
        Returns:
            Timeout in seconds
        """
        try:
            return self.tasks[task_name].get('timeout_seconds', 300)
        except KeyError:
            return 300
    
    def get_node_function(self, task_name: str) -> Optional[str]:
        """Get the node function name that implements this task.
        
        Args:
            task_name: Name of the task
        
        Returns:
            Node function name or None
        """
        try:
            return self.tasks[task_name].get('node_function')
        except KeyError:
            return None
    
    def list_tasks(self) -> List[str]:
        """List all available tasks.
        
        Returns:
            List of task names
        """
        return list(self.tasks.keys())
    
    def get_execution_order(self) -> List[str]:
        """Get tasks in dependency order (topological sort).
        
        Returns:
            List of task names in execution order
        """
        visited = set()
        order = []
        
        def visit(task_name: str):
            if task_name in visited:
                return
            visited.add(task_name)
            
            # Visit dependencies first
            deps = self.get_dependencies(task_name)
            for dep in deps:
                visit(dep)
            
            order.append(task_name)
        
        # Visit all tasks
        for task_name in self.tasks.keys():
            visit(task_name)
        
        return order
    
    def validate_dependencies(self) -> Dict[str, List[str]]:
        """Validate that all task dependencies exist.
        
        Returns:
            Dict mapping task names to list of missing dependencies
        """
        issues = {}
        all_tasks = set(self.tasks.keys())
        
        for task_name in self.tasks.keys():
            deps = self.get_dependencies(task_name)
            missing = [d for d in deps if d not in all_tasks]
            if missing:
                issues[task_name] = missing
        
        return issues
    
    def reload(self):
        """Reload tasks from file."""
        self._tasks = None


class TaskExecutor:
    """Wraps task execution with timeout, retry, and error handling."""
    
    def __init__(self, task_loader: Optional[TaskLoader] = None):
        """Initialize task executor.
        
        Args:
            task_loader: TaskLoader instance. If None, creates default.
        """
        self.task_loader = task_loader or get_task_loader()
    
    def execute_with_config(
        self,
        task_name: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Execute a function with task configuration (timeout, retry).
        
        Args:
            task_name: Name of the task for config lookup
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func
        
        Returns:
            Result from func
        
        Raises:
            TimeoutError: If execution times out
            Exception: If execution fails after retries
        """
        config = self.task_loader.get_task_config(task_name)
        
        last_error = None
        for attempt in range(config.retry_count):
            try:
                # Execute with timeout
                result = self._execute_with_timeout(
                    func,
                    config.timeout_seconds,
                    *args,
                    **kwargs
                )
                return result
            except TimeoutError as e:
                last_error = e
                print(f"⚠️  Task '{task_name}' timed out (attempt {attempt + 1}/{config.retry_count})")
                if attempt < config.retry_count - 1:
                    time.sleep(2)  # Brief pause before retry
            except Exception as e:
                last_error = e
                print(f"⚠️  Task '{task_name}' failed: {e} (attempt {attempt + 1}/{config.retry_count})")
                if attempt < config.retry_count - 1:
                    time.sleep(2)
        
        # All retries failed
        raise last_error
    
    def _execute_with_timeout(
        self,
        func: Callable,
        timeout_seconds: int,
        *args,
        **kwargs
    ) -> Any:
        """Execute function with timeout.
        
        Args:
            func: Function to execute
            timeout_seconds: Timeout in seconds
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Function result
        
        Raises:
            TimeoutError: If execution exceeds timeout
        """
        # Note: signal.alarm only works on Unix systems
        # For cross-platform, consider using threading.Timer or concurrent.futures
        
        try:
            # Set up timeout signal (Unix only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout_seconds)
            
            result = func(*args, **kwargs)
            
            # Cancel alarm
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
            return result
        except TimeoutError:
            raise
        except Exception as e:
            # Cancel alarm on error
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            raise


def task_metadata(task_name: str):
    """Decorator to attach task metadata to a function.
    
    Args:
        task_name: Name of the task in tasks.yaml
    
    Example:
        @task_metadata('fetch_ai_news')
        def fetch_news_for_topic(state):
            # Implementation
            return state
    """
    def decorator(func: Callable) -> Callable:
        loader = get_task_loader()
        config = loader.get_task_config(task_name)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"📋 Task: {task_name}")
            print(f"   Agent: {config.agent}")
            print(f"   Description: {config.description[:100]}...")
            
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            print(f"   ✅ Completed in {execution_time:.2f}s")
            return result
        
        # Attach metadata
        wrapper.task_name = task_name
        wrapper.task_config = config
        
        return wrapper
    return decorator


# Global singleton instance
_default_loader: Optional[TaskLoader] = None


def get_task_loader(tasks_file: Optional[str] = None) -> TaskLoader:
    """Get the default task loader instance.
    
    Args:
        tasks_file: Optional path to tasks file. Only used on first call.
    
    Returns:
        TaskLoader instance
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = TaskLoader(tasks_file)
    return _default_loader


def load_task_config(task_name: str) -> TaskConfig:
    """Convenience function to load a task configuration.
    
    Args:
        task_name: Name of the task
    
    Returns:
        TaskConfig object
    
    Example:
        >>> config = load_task_config('fetch_ai_news')
        >>> print(config.description)
        >>> print(config.timeout_seconds)
    """
    loader = get_task_loader()
    return loader.get_task_config(task_name)


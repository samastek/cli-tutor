"""Progress tracking system for CLI Tutor."""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime


class ProgressTracker:
    """Manages user progress across CLI learning sessions."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize progress tracker with SQLite database."""
        if db_path is None:
            # Store in user's home directory under .cli_tutor
            home_dir = Path.home()
            cli_tutor_dir = home_dir / ".cli_tutor"
            cli_tutor_dir.mkdir(exist_ok=True)
            db_path = cli_tutor_dir / "progress.db"
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table for tracking completed tasks
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS completed_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plugin_name TEXT NOT NULL,
                    task_id INTEGER NOT NULL,
                    task_title TEXT NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    attempts INTEGER DEFAULT 1,
                    UNIQUE(plugin_name, task_id)
                )
            """)
            
            # Table for tracking plugin progress
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS plugin_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plugin_name TEXT UNIQUE NOT NULL,
                    total_tasks INTEGER NOT NULL,
                    completed_tasks INTEGER DEFAULT 0,
                    current_task_index INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_completed BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Table for tracking user preferences and stats
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_sessions INTEGER DEFAULT 0,
                    total_tasks_completed INTEGER DEFAULT 0,
                    total_commands_learned INTEGER DEFAULT 0,
                    last_session TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def mark_task_completed(self, plugin_name: str, task_id: int, task_title: str) -> bool:
        """Mark a specific task as completed."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            try:
                # Check if task is already completed
                cursor.execute("""
                    SELECT attempts FROM completed_tasks 
                    WHERE plugin_name = ? AND task_id = ?
                """, (plugin_name, task_id))
                
                result = cursor.fetchone()
                
                if result:
                    # Task already completed, increment attempts
                    attempts = result[0] + 1
                    cursor.execute("""
                        UPDATE completed_tasks 
                        SET attempts = ?, completed_at = CURRENT_TIMESTAMP
                        WHERE plugin_name = ? AND task_id = ?
                    """, (attempts, plugin_name, task_id))
                else:
                    # First time completing this task
                    cursor.execute("""
                        INSERT INTO completed_tasks (plugin_name, task_id, task_title)
                        VALUES (?, ?, ?)
                    """, (plugin_name, task_id, task_title))
                
                conn.commit()
                return True
                
            except sqlite3.Error:
                return False
    
    def is_task_completed(self, plugin_name: str, task_id: int) -> bool:
        """Check if a specific task has been completed."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM completed_tasks 
                WHERE plugin_name = ? AND task_id = ?
            """, (plugin_name, task_id))
            
            return cursor.fetchone() is not None
    
    def get_completed_task_ids(self, plugin_name: str) -> Set[int]:
        """Get set of completed task IDs for a plugin."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT task_id FROM completed_tasks 
                WHERE plugin_name = ?
            """, (plugin_name,))
            
            return {row[0] for row in cursor.fetchall()}
    
    def update_plugin_progress(self, plugin_name: str, total_tasks: int, 
                             completed_tasks: int, current_task_index: int):
        """Update progress for a specific plugin."""
        is_completed = completed_tasks >= total_tasks
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO plugin_progress 
                (plugin_name, total_tasks, completed_tasks, current_task_index, 
                 last_accessed, is_completed)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
            """, (plugin_name, total_tasks, completed_tasks, current_task_index, is_completed))
            
            conn.commit()
    
    def get_plugin_progress(self, plugin_name: str) -> Dict:
        """Get progress information for a specific plugin."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT total_tasks, completed_tasks, current_task_index, 
                       last_accessed, is_completed
                FROM plugin_progress 
                WHERE plugin_name = ?
            """, (plugin_name,))
            
            result = cursor.fetchone()
            if result:
                return {
                    "total_tasks": result[0],
                    "completed_tasks": result[1],
                    "current_task_index": result[2],
                    "last_accessed": result[3],
                    "is_completed": result[4]
                }
            return {}
    
    def get_next_incomplete_task_index(self, plugin_name: str, total_tasks: int) -> int:
        """Get the index of the next incomplete task for a plugin."""
        completed_ids = self.get_completed_task_ids(plugin_name)
        
        # Find the first task that hasn't been completed
        for task_index in range(total_tasks):
            task_id = task_index + 1  # Task IDs are 1-based
            if task_id not in completed_ids:
                return task_index
        
        # All tasks completed
        return total_tasks
    
    def get_overall_stats(self) -> Dict:
        """Get overall user statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count total completed tasks
            cursor.execute("SELECT COUNT(*) FROM completed_tasks")
            total_tasks_completed = cursor.fetchone()[0]
            
            # Count total commands with completed tasks
            cursor.execute("SELECT COUNT(DISTINCT plugin_name) FROM completed_tasks")
            commands_started = cursor.fetchone()[0]
            
            # Count fully completed plugins
            cursor.execute("SELECT COUNT(*) FROM plugin_progress WHERE is_completed = TRUE")
            commands_completed = cursor.fetchone()[0]
            
            return {
                "total_tasks_completed": total_tasks_completed,
                "commands_started": commands_started,
                "commands_completed": commands_completed
            }
    
    def get_plugin_summary(self) -> List[Dict]:
        """Get summary of all plugins with progress."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT plugin_name, total_tasks, completed_tasks, 
                       is_completed, last_accessed
                FROM plugin_progress 
                ORDER BY last_accessed DESC
            """)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "plugin_name": row[0],
                    "total_tasks": row[1],
                    "completed_tasks": row[2],
                    "is_completed": bool(row[3]),
                    "last_accessed": row[4],
                    "progress_percentage": (row[2] / row[1] * 100) if row[1] > 0 else 0
                })
            
            return results
    
    def reset_plugin_progress(self, plugin_name: str):
        """Reset all progress for a specific plugin."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Remove completed tasks for this plugin
            cursor.execute("""
                DELETE FROM completed_tasks WHERE plugin_name = ?
            """, (plugin_name,))
            
            # Reset plugin progress
            cursor.execute("""
                DELETE FROM plugin_progress WHERE plugin_name = ?
            """, (plugin_name,))
            
            conn.commit()
    
    def reset_all_progress(self):
        """Reset all user progress (nuclear option)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM completed_tasks")
            cursor.execute("DELETE FROM plugin_progress")
            cursor.execute("DELETE FROM user_stats")
            
            conn.commit()
    
    def export_progress(self) -> Dict:
        """Export all progress data for backup purposes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Export completed tasks
            cursor.execute("SELECT * FROM completed_tasks")
            completed_tasks = [dict(zip([col[0] for col in cursor.description], row)) 
                             for row in cursor.fetchall()]
            
            # Export plugin progress
            cursor.execute("SELECT * FROM plugin_progress")
            plugin_progress = [dict(zip([col[0] for col in cursor.description], row)) 
                             for row in cursor.fetchall()]
            
            return {
                "export_date": datetime.now().isoformat(),
                "completed_tasks": completed_tasks,
                "plugin_progress": plugin_progress,
                "stats": self.get_overall_stats()
            }

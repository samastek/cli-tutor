# Progress Tracking System

CLI Tutor now includes a robust progress tracking system that remembers your learning progress across sessions. You'll only be asked questions you haven't answered correctly yet, even if you exit and restart the CLI.

## How It Works

The progress tracker uses a SQLite database stored in your home directory (`~/.cli_tutor/progress.db`) to persistently track:

- ✅ Which tasks you've completed for each command
- 📊 Your overall progress statistics
- 🔄 Your current position in each learning module
- 📈 Completion percentages and learning streaks

## Key Features

### Smart Resume
- **Skip Completed Tasks**: Only shows tasks you haven't completed yet
- **Resume Where You Left Off**: Continues from your last incomplete task
- **Cross-Session Persistence**: Progress is saved even if you quit the CLI

### Progress Visualization
- **Real-time Progress Bars**: See your completion status in the CLI
- **Detailed Statistics**: View overall learning statistics
- **Per-Command Tracking**: Monitor progress for individual commands

### Progress Management
- **Reset Individual Commands**: Start over with specific commands
- **Reset All Progress**: Nuclear option to clear everything
- **Export/Import**: Backup your progress data

## Usage Examples

### Starting a Learning Session
```bash
# Start the interactive CLI (automatically resumes from last position)
poetry run cli-tutor start

# View your overall progress
poetry run cli-tutor progress

# List available commands with progress indicators
poetry run cli-tutor list-plugins
```

### Managing Progress
```bash
# Reset progress for a specific command
poetry run cli-tutor reset-progress ls

# Reset all progress (with confirmation)
poetry run cli-tutor reset-progress all

# Force reset without confirmation
poetry run cli-tutor reset-progress all --force

# Export progress for backup
poetry run cli-tutor export-progress --output my_backup.json
```

### Interactive Commands
When in a learning session, you can use these commands:
- `hint` - Get a hint for the current task
- `skip` - Skip the current task (marks as incomplete)
- `reset` - Reset progress for the current command
- `quit` - Return to main menu

## Database Schema

The progress tracker uses three main tables:

### `completed_tasks`
Tracks individual task completions:
- `plugin_name` - Command name (e.g., 'ls', 'grep')
- `task_id` - Task identifier within the plugin
- `task_title` - Human-readable task name
- `completed_at` - Timestamp of completion
- `attempts` - Number of times completed (for repeated practice)

### `plugin_progress`
Tracks overall plugin progress:
- `plugin_name` - Command name
- `total_tasks` - Total number of tasks in plugin
- `completed_tasks` - Number of completed tasks
- `current_task_index` - Current position in task sequence
- `is_completed` - Whether all tasks are done
- `last_accessed` - Last time this plugin was used

### `user_stats`
Stores overall user statistics and preferences.

## Implementation Details

### Progress Tracker Class (`progress_tracker.py`)
- Manages SQLite database operations
- Provides methods for marking tasks complete
- Calculates progress statistics
- Handles data export/import

### Plugin Integration
- Plugins automatically load progress on initialization
- Tasks are skipped if already completed
- Progress is updated after each successful completion
- Smart navigation to next incomplete task

### Data Persistence
- Database stored in `~/.cli_tutor/progress.db`
- Automatic database creation on first run
- Thread-safe operations with proper SQLite handling
- Graceful fallback when progress tracking is unavailable

## Benefits

1. **Efficient Learning**: Focus only on what you haven't mastered
2. **Motivation**: Visual progress tracking encourages completion
3. **Flexibility**: Easy to reset or manage progress as needed
4. **Backup**: Export/import functionality protects your progress
5. **Resumability**: Never lose your place in the learning sequence

## File Locations

- **Database**: `~/.cli_tutor/progress.db`
- **Backups**: Wherever you specify with `--output` flag
- **Logs**: Integrated with Rich console output

## Migration from Non-Tracked Sessions

If you've been using CLI Tutor before this feature:
1. Your existing session state will not be tracked
2. Start fresh with `cli-tutor start` to begin tracking
3. Previously completed tasks will need to be done again (one-time reset)

The progress tracking system is designed to be invisible when working properly - you'll simply notice that you're not asked questions you've already answered correctly!

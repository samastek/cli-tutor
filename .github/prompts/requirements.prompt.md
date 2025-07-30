---
mode: agent
---

I want to create a cli tool that is a Python-based and interactive designed for educational purposes. It helps users learn command-line utilities through repetitive interaction and hands-on practice with immediate feedback.

The tool must be modular, allowing for easy addition of new command plugins. Each plugin should provide a set of tasks that guide users through the command's usage, from basic to advanced levels. 

Each plugin should be added as a new Python module, for example, `find.py`, `grep.py`, `ls.py`, etc. Each module has a corresponding json file that defines the tasks and their metadata. The tool should be able to load these modules dynamically and present the tasks to the user in a structured manner.

The user succeeds in a task by providing the correct command or output, and the tool should provide immediate feedback. If the user fails, it should offer hints or explanations to help them understand the command better. If the user succeeds the next task should be presented, until all tasks in the module are completed. 
It is very important that the tool is designed modularly, so that new command plugins can be added easily without modifying the core logic of the tool.
use poetry for dependency management and packaging.
use rich for the CLI interface.

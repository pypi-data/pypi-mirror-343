# FocusCLI - Developer Productivity Tool
> *Your Personal Productivity Companion - By PyGen Labs*

![PyGen Labs FocusCLI](https://img.shields.io/badge/PyGen%20Labs-FocusCLI-blue)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.1-green)

## 🚀 Overview

FocusCLI is a powerful, offline-first developer productivity tool that helps you manage tasks, sprints, goals, and notes directly from your terminal. Built by PyGen Labs, it's designed to keep developers in their flow state without leaving the command line.

## 📋 Complete Command Reference

### Sprint Management
```bash
# Start a sprint (default 25 minutes)
focus sprint start
focus sprint start --time 30    # Custom duration

# Stop current sprint
focus sprint stop

# View sprint history
focus sprint list
focus sprint history

# Delete sprint record
focus sprint delete <sprint-id>
```

### Task Management
```bash
# Tasks
focus tasks add "Implement API endpoint"
focus tasks list
focus tasks done <task-id>
focus tasks delete <task-id>
focus tasks update <task-id> "New task description"
focus tasks priority <task-id> high|medium|low
focus tasks clear-completed    # Remove completed tasks
```

### Notes Management
```bash
# Notes
focus notes add "Important implementation detail"
focus notes list
focus notes delete <note-id>
focus notes search "keyword"
focus notes edit <note-id> "Updated content"
focus notes export --format md|txt
```

### Goals Management
```bash
# Goals
focus goals add "Complete project" --type daily|weekly|monthly
focus goals list
focus goals complete <goal-id>
focus goals delete <goal-id>
focus goals progress <goal-id>
focus goals stats    # View achievement statistics
```

### Other Features
```bash
# Developer Quotes
focus quote dev    # Get motivational developer quote
focus quote add "Your custom quote"

# Statistics
focus stats daily    # View today's productivity
focus stats weekly   # Weekly summary
```

## 🏢 About PyGen Labs

PyGen Labs is a pioneering software development initiative under PyGen & Co., led by Ameer Hamza Khan. We focus on building open, accessible tools and web applications that empower developers and individuals worldwide.

### Our Mission
- Build simple yet powerful tools that empower individuals and developers
- Use technology for the benefit of all humanity
- Create innovative, open-source solutions for real-world problems

### Notable Projects
- **ProjXs**: Open-source project management platform with AI-powered insights
- **FocusCLI**: Developer productivity command-line tool

## 🤝 Contributing

### Reporting Issues
For bugs, feature requests, or general feedback:

```bash
# In your terminal
focus feedback "Your feedback message"
```

Or add comments in source code:
```python
# TODO: Feature request - Add task categories
# BUG: Sprint timer occasionally shows incorrect duration
# ENHANCE: Add color coding for different priority levels
```

### Local Development Setup
```bash
git clone https://github.com/pygen-labs/focus-cli
cd focus-cli
pip install -e .
```

## 🔒 Privacy & Security

- 100% offline operation
- No data collection
- Local file storage only
- Data stored in: 
  - Windows: `%APPDATA%/focus-cli/`
  - Linux/MacOS: `~/.focus-cli/`

## 🌟 PyGen Labs Community

Join our community of developers:
- Leave inline comments in your code with `# FEEDBACK:`
- Use `focus feedback` command
- Add feature requests with `# FEATURE:`

For detailed documentation and updates, visit our [GitHub Wiki](https://github.com/pygen-labs/focus-cli/wiki)

---

<div align="center">

**Made with ❤️ by [PyGen Labs](https://pygen.in)**

_Empowering Developers, One Tool at a Time_

</div>
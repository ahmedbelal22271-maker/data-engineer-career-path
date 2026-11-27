# Automated Directory Backup & Archive Engine — Linux Shell Scripting

A production-grade Linux shell automation project implementing automated timestamped directory backups, incremental file modification tracking via Unix epoch comparisons, `tar.gz` archive compression, and scheduled execution via `cron`.

---

## 📌 Executive Summary

System administrators and data engineers must maintain reliable, automated directory archives to prevent data loss. This project delivers an automated shell scripting backup engine:
1. **Command-Line Argument Validation**: Enforces strict positional parameter counts (`$# == 2`) and verifies directory validity (`[[ -d ... ]]`).
2. **Epoch Delta Calculation**: Calculates Unix timestamps in seconds (`date +%s`), calculates a 24-hour lookback threshold ($86,400\text{ seconds}$), and filters only files updated within the target window using `date -r "$file" +%s`.
3. **Archiving & Compression**: Bundles modified files into a timestamped compressed archive `backup-[TIMESTAMP].tar.gz` using `tar -czf`.
4. **Automated Scheduling (`cron`)**: Schedules automatic periodic backup executions via the Linux `crontab` daemon (`crontab-schedule.txt`).

---

## 📁 Project Structure

```text
c6_linux_shell_scripting_final_project/
├── README.md                  # Project overview & usage guide
├── backup.sh                  # Core Bash backup automation script
├── crontab-schedule.txt       # Crontab schedule configuration
├── backup-permissions.txt     # Linux permission audit (chmod +x)
├── backup-file-check.txt      # Execution and output verification log
├── backup-script-copy.txt     # Deployment copy verification log
├── final project.pdf          # Official project specification
└── Task 1.png                 # Execution verification screenshot
```

---

## 🛠️ Technology Stack

- **Operating System**: Linux / Ubuntu (WSL)
- **Shell**: GNU Bash
- **Core Utilities**: `date`, `tar`, `gzip`, `cron`, `crontab`, `find`, `test`

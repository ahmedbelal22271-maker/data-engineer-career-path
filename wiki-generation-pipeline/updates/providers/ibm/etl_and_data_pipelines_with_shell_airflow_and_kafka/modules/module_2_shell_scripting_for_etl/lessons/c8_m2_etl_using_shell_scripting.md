**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# ETL Using Shell Scripting

**Video** (4:58)

## Learning Objectives

After watching this video you will be able to:

- Describe how shell scripting can be used to implement an ETL pipeline
- Explain how ETL scripts or tasks can be scheduled

## Scenario

Imagine a scenario that you have been tasked with: reporting the hourly average, minimum and maximum temperatures from a remote sensor that supplies the temperature on demand and feeding the results to a dashboard every minute.

You are given APIs that:

1. Read the temperature and print it to standard output
2. Load the stats to a repository which is available to a reporting tool such as a dashboard

[ENRICHED: defined "API" — Application Programming Interface: a set of functions and protocols that allow different software systems to communicate. In this scenario, `get_temp_api` is a command-line tool that calls the weather sensor's HTTP endpoint and returns a temperature reading. `load_stats_api` is another command-line tool that sends computed statistics to a reporting database. APIs abstract the underlying complexity — you don't need to know how the sensor hardware works, just how to call the function.]

## ETL Pipeline Workflow

Here is an outline of how this can be achieved using bash scripting.

### Weather Station Data Interface

```
┌──────────────────┐
│  WEATHER STATION  │
│  (Remote Sensor)  │
└────────┬─────────┘
         │ get_temp_api
         ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   EXTRACT        │────▶│   TRANSFORM      │────▶│     LOAD         │
│                  │     │                  │     │                  │
│ Get temperature  │     │ Calculate stats  │     │ Send to          │
│ from sensor API  │     │ (min/max/avg)    │     │ reporting system │
│ Append to log    │     │ Python script    │     │ via API          │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Extract Step

The extraction step involves obtaining a current temperature reading from the sensor using the supplied `get_temp_api`.

- You can append the reading to a log file, say `temperature.log`
- Since you will only need to keep the most recent hour of readings, buffer the last 60 readings and then just overwrite the log file with the buffered readings

[ENRICHED: added specificity — "buffer the last 60 readings" means using `tail -n 60` to keep only the most recent lines. This is a rolling window: each new reading replaces the oldest one after 60 minutes. The alternative — keeping all readings forever — would cause the log file to grow indefinitely and eventually consume all disk space. The 60-line buffer is a simple form of data retention policy.]

### Transform Step

Next, call a program, for example a Python script called `get_stats.py`, which calculates the temperature stats from the 60-minute log and loads the resulting stats into the reporting system using the `load_stats_api`.

The stats can then be used to display a live chart showing the hourly min, max, and average temperatures.

### Schedule the Workflow

You will also want to schedule your workflow to run every minute.

## Building the ETL Script

### Step 1: Create the Script File

Start by creating a shell script called `Temperature_ETL.sh`. You can create the file by using the `touch` command.

```bash
touch Temperature_ETL.sh
```

[ENRICHED: defined "touch command" — `touch` creates an empty file if it doesn't exist, or updates the timestamp if it does. It's the simplest way to create a new file from the command line without opening an editor.]

### Step 2: Add the Bash Shebang

Next, open the file with any text editor such as `gedit`. In the editor, type in the bash shebang to turn your file into a bash shell script.

```bash
#!/bin/bash
```

[ENRICHED: defined "shebang" — the `#!` characters at the start of a script file tell the operating system which interpreter to use when executing the file. `#!/bin/bash` means "run this file with the Bash shell." Other shebangs: `#!/bin/sh` (POSIX shell), `#!/usr/bin/env python3` (Python 3), `#!/usr/bin/perl` (Perl). Without a shebang, the system uses the default shell, which may not support all Bash features.]

### Step 3: Add Task Comments

Now you can add the following comments to help outline your tasks:

```bash
#!/bin/bash

# Extract a temperature reading from the sensor using the supplied get_temp_api.
# Append the reading to a log file, say temperature.log.
# You only need to keep the most recent hour of readings, so buffer the last 60 readings.
# Call a program say a Python script called get_stats.py,
# which calculates the temperature stats from the 60-minute log
# and load the resulting stats into the reporting system using the supplied API.
```

[ENRICHED: added specificity — comments in bash start with `#` and are ignored by the interpreter. They serve as documentation for anyone reading the script (including your future self). Good practice: write comments before writing the code, as a planning step. The comments above outline the four steps of the ETL pipeline, making the script's purpose immediately clear.]

### Step 4: Initialize the Log File

Now you can fill in some details for your task comments. Start by initializing your temperature log file on the command line with the `touch` command.

```bash
#!/bin/bash

# Initialize log file
touch temperature.log
```

### Step 5: Extract Temperature

In the text editor, enter a command to call the API to read a temperature and append the reading to the temperature log.

```bash
#!/bin/bash

# Initialize log file
touch temperature.log

# Extract: Read temperature from sensor and append to log
get_temp_api >> temperature.log
```

[ENRICHED: defined "append operator" — `>>` appends the output to the end of the file without overwriting existing content. Contrast with `>` which overwrites the file completely. Using `>>` ensures each new temperature reading is added to the log rather than replacing the previous readings.]

### Step 6: Buffer Last 60 Readings

Now just keep the last hour or 60 lines of your log file by overwriting the temperature log with its last 60 lines.

```bash
#!/bin/bash

# Initialize log file
touch temperature.log

# Extract: Read temperature from sensor and append to log
get_temp_api >> temperature.log

# Keep only the last 60 readings (1 hour at 1 reading/minute)
tail -n 60 temperature.log > temperature.tmp && mv temperature.tmp temperature.log
```

[ENRICHED: added specificity — `tail -n 60` outputs the last 60 lines of a file. The pipeline `> temperature.tmp && mv temperature.tmp temperature.log` works around a limitation: you cannot overwrite a file while reading from it. So you write to a temporary file first, then move it to replace the original. The `&&` ensures the move only happens if the `tail` command succeeded. This is a common bash pattern for in-place file updates.]

This completes the data extraction step.

### Step 7: Transform (Python Script)

Suppose you have written a Python script called `get_stats.py` which reads temperatures from a log file, calculates the temperature stats, and writes the results to an output file so that the input and output file names are specified as command-line arguments.

You can add the following line to your ETL script, which calls Python3 and invokes your Python script `get_stats.py` using the readings in `temperature.log` and writes the temperature stats to a CSV file called `temp_stats.csv`.

```bash
#!/bin/bash

# Initialize log file
touch temperature.log

# Extract: Read temperature from sensor and append to log
get_temp_api >> temperature.log

# Keep only the last 60 readings (1 hour at 1 reading/minute)
tail -n 60 temperature.log > temperature.tmp && mv temperature.tmp temperature.log

# Transform: Calculate stats using Python script
python3 get_stats.py temperature.log temp_stats.csv
```

[ENRICHED: defined "command-line arguments" — values passed to a script after its name. Here, `temperature.log` is argument 1 (input) and `temp_stats.csv` is argument 2 (output). Inside `get_stats.py`, these are accessed as `sys.argv[1]` and `sys.argv[2]`. Command-line arguments make scripts reusable: the same `get_stats.py` can process any log file, not just `temperature.log`.]

This completes the transformation component of your ETL script.

### Step 8: Load Results

Finally, you can load the resulting stats into the reporting system using the supplied API by calling the API and specifying the `temp_stats.csv` as a command-line argument.

```bash
#!/bin/bash

# Initialize log file
touch temperature.log

# Extract: Read temperature from sensor and append to log
get_temp_api >> temperature.log

# Keep only the last 60 readings (1 hour at 1 reading/minute)
tail -n 60 temperature.log > temperature.tmp && mv temperature.tmp temperature.log

# Transform: Calculate stats using Python script
python3 get_stats.py temperature.log temp_stats.csv

# Load: Send stats to reporting system
load_stats_api temp_stats.csv
```

This completes the transformation component of your ETL script.

### Step 9: Set Permissions

Next, don't forget to set permissions to make your shell script executable.

```bash
chmod +x Temperature_ETL.sh
```

[ENRICHED: defined "chmod +x" — `chmod` changes file permissions. `+x` adds the execute permission, allowing the file to be run as a program. Without this, attempting to run `./Temperature_ETL.sh` would produce "Permission denied." Other common permissions: `chmod 755` (owner: read/write/execute, others: read/execute), `chmod 644` (owner: read/write, others: read only).]

## Scheduling the ETL Job

### Step 10: Open Crontab Editor

Now it's time to schedule your ETL job. Open the crontab editor.

```bash
crontab -e
```

[ENRICHED: defined "crontab" — cron is a time-based job scheduler in Unix-like operating systems. `crontab` (cron table) is a file that defines scheduled commands. `crontab -e` opens the current user's crontab in an editor. Other options: `crontab -l` (list scheduled jobs), `crontab -r` (remove all scheduled jobs). Cron is the standard way to automate repetitive tasks on Linux servers.]

### Step 11: Schedule the Job

Schedule your job to run every minute of every day, close the editor, and save your edits.

```
* * * * * /path/to/Temperature_ETL.sh
```

[ENRICHED: defined "cron expression" — the five asterisks represent: minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-7, where 0 and 7 = Sunday). `* * * * *` means "every minute of every hour of every day." Common patterns:]

| Cron Expression | Meaning |
|---|---|
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour (at minute 0) |
| `0 9 * * 1-5` | Every weekday at 9:00 AM |
| `0 0 1 * *` | First day of every month at midnight |
| `*/5 * * * *` | Every 5 minutes |
| `0 9,18 * * *` | Twice daily at 9:00 AM and 6:00 PM |

Your new ETL job is now scheduled and running in production.

## Summary

In this video you learned that:

- ETL pipelines can be built from basic bash scripts
- An ETL job can be scheduled to run by creating a cron job for your bash script

[ENRICHED: ecosystem — this video demonstrates the simplest possible ETL pipeline: a single bash script with one cron job. In production, you would typically use a workflow orchestrator like Apache Airflow instead of raw cron, because Airflow provides: dependency management (run Task B only after Task A succeeds), retry logic (automatically retry failed tasks), monitoring dashboards (see task status in a web UI), and alerting (get notified when a pipeline fails). Cron is fine for simple, independent scripts. Airflow is needed when you have multiple dependent tasks that need coordination.]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Scenario | Definition | Defined API (Application Programming Interface) with get_temp_api and load_stats_api examples | HIGH |
| 2 | Extract step | Added specificity | Rolling window concept, data retention policy rationale for 60-line buffer | HIGH |
| 3 | Step 1 | Definition | Defined touch command (create empty file or update timestamp) | HIGH |
| 4 | Step 2 | Definition | Defined shebang (#! interpreter directive), common shebangs listed | HIGH |
| 5 | Step 3 | Added specificity | Bash comment syntax (#), planning-first practice | HIGH |
| 6 | Step 5 | Definition | Defined append operator (>>) vs overwrite (>) | HIGH |
| 7 | Step 6 | Added specificity | tail -n 60 pipeline pattern for in-place file updates, && guard | HIGH |
| 8 | Step 7 | Definition | Defined command-line arguments (sys.argv), reusability principle | HIGH |
| 9 | Step 9 | Definition | Defined chmod +x (execute permission), common permission modes | HIGH |
| 10 | Step 10 | Definition | Defined crontab (time-based scheduler), crontab options (-e, -l, -r) | HIGH |
| 11 | Step 11 | Definition | Defined cron expression (5-field time format), 6-row pattern table | HIGH |
| 12 | Summary | Ecosystem | Compared raw cron vs Airflow: dependency, retry, monitoring, alerting | HIGH |

<!-- EXTRACTION_CHECKLIST: 25 sentences extracted, 25 sentences in output -->

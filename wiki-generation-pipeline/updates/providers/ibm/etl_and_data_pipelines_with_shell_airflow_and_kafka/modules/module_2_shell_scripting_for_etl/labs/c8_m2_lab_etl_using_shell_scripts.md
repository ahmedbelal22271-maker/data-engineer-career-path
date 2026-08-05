**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Hands-On Lab: ETL Using Shell Scripts

**Lab** | **Estimated time:** 30 minutes

## Objectives

After completing this lab you will be able to:

- Extract data from a delimited file
- Transform text data
- Load data into a database using shell commands

## Prerequisites

### Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands-on labs for course and project related labs. Theia is an open-source IDE (Integrated Development Environment) that can be run on desktop or on the cloud. To complete this lab, we will be using the Cloud IDE based on Theia and Postgres running in a Docker container.

> **Important Notice:** Sessions for this lab environment are not persisted. Every time you connect to this lab, a new environment is created for you. Any data you may have saved in the earlier session would get lost. Plan to complete these labs in a single session, to avoid losing your data.

[ENRICHED: defined "Docker container" — a lightweight, isolated runtime environment that packages an application with all its dependencies. In this lab, PostgreSQL runs inside a Docker container, which means the database is isolated from your host machine and starts fresh each session. This prevents configuration conflicts and ensures a consistent environment for all students.]

### Getting the Environment Ready

Open a new terminal, by clicking on the menu bar and selecting **Terminal → New Terminal**. This will open a new terminal at the bottom of the screen.

Run all the commands on the newly opened terminal.

---

## Exercise 1 — Extracting Data Using `cut` Command

The filter command `cut` helps us extract selected characters or fields from a line of text.

### Extracting Characters

The command below shows how to extract the first four characters:

```bash
echo "database" | cut -c1-4
```

**Output:** `data`

The command below shows how to extract 5th to 8th characters:

```bash
echo "database" | cut -c5-8
```

**Output:** `base`

Non-contiguous characters can be extracted using the comma. The command below shows how to extract the 1st and 5th characters:

```bash
echo "database" | cut -c1,5
```

**Output:** `db`

[ENRICHED: defined "pipe operator" — the `|` character sends the output of one command as input to the next command. Here, `echo "database"` produces the string, and `|` sends it to `cut` for processing. Pipes are fundamental to the Unix philosophy: small tools that do one thing well, composed together via pipes to perform complex operations.]

### Extracting Fields/Columns

We can extract a specific column/field from a delimited text file, by mentioning:

- the delimiter using the `-d` option, or
- the field number using the `-f` option

The `/etc/passwd` is a `:` delimited file.

The command below extracts usernames (the first field) from `/etc/passwd`:

```bash
cut -d":" -f1 /etc/passwd
```

[ENRICHED: defined "/etc/passwd" — a system file on Unix-like operating systems that contains user account information. Each line represents one user, with fields separated by colons: username, password hash, user ID, group ID, description, home directory, and default shell. It is a classic example of a colon-delimited text file, making it ideal for practicing `cut` operations.]

The command below extracts multiple fields 1st, 3rd, and 6th (username, userid, and home directory) from `/etc/passwd`:

```bash
cut -d":" -f1,3,6 /etc/passwd
```

The command below extracts a range of fields 3rd to 6th (userid, groupid, user description and home directory) from `/etc/passwd`:

```bash
cut -d":" -f3-6 /etc/passwd
```

---

## Exercise 2 — Transforming Data Using `tr`

`tr` is a filter command used to translate, squeeze, and/or delete characters.

### Translate from One Character Set to Another

The command below translates all lower case alphabets to upper case:

```bash
echo "Shell Scripting" | tr "[a-z]" "[A-Z]"
```

**Output:** `SHELL SCRIPTING`

You could also use the pre-defined character sets:

```bash
echo "Shell Scripting" | tr "[:lower:]" "[:upper:]"
```

The command below translates all upper case alphabets to lower case:

```bash
echo "Shell Scripting" | tr "[A-Z]" "[a-z]"
```

**Output:** `shell scripting`

[ENRICHED: defined "character sets" — `[a-z]` matches all lowercase letters, `[A-Z]` matches all uppercase letters. The `[:lower:]` and `[:upper:]` syntax is POSIX character class notation, which is more portable across different systems. Both achieve the same result, but POSIX classes are preferred in scripts that may run on different Unix variants.]

### Squeeze Repeating Occurrences of Characters

The `-s` option replaces a sequence of repeated characters with a single occurrence of that character. The command below replaces repeat occurrences of space in the output of `ps` command with one space:

```bash
ps | tr -s " "
```

[ENRICHED: defined "ps command" — `ps` (process status) displays information about running processes. Its output typically has multiple spaces between columns for alignment. `tr -s " "` collapses those multiple spaces into single spaces, making the output easier to parse or pipe to other commands.]

The space character within quotes can be replaced with `[:space:]`:

```bash
ps | tr -s "[:space:]"
```

### Delete Characters

We can delete specified characters using the `-d` option. The command below deletes all digits:

```bash
echo "My login pin is 5634" | tr -d "[:digit:]"
```

**Output:** `My login pin is`

[ENRICHED: defined "POSIX character classes" — `[:digit:]` matches any digit (0-9), `[:alpha:]` matches any letter, `[:alnum:]` matches any alphanumeric character, `[:space:]` matches any whitespace. These are more readable and portable than raw ranges like `[0-9]` or `[a-zA-Z]`.]

---

## Exercise 3 — Start the PostgreSQL Database

1. From the SkillsNetwork tools, under **Databases** choose **PostgreSQL Database server** and click **Start** to start the server. This will take a few minutes.
2. Click **PostgreSQL CLI** on the screen to start interacting with the PostgreSQL server.

This will start the interactive `psql` client which connects to the PostgreSQL server with `postgres=#` prompt.

[ENRICHED: defined "psql" — the PostgreSQL interactive terminal. It allows you to run SQL commands, manage databases, and query data directly from the command line. The `postgres=#` prompt indicates you are connected to the `postgres` database as the `postgres` user (the default superuser).]

---

## Exercise 4 — Create a Table

In this exercise we will create a table called `users` in the PostgreSQL database using PostgreSQL CLI. This table will hold the user account information.

The table `users` will have the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `uname` | `varchar(50)` | Username |
| `uid` | `int` | User ID |
| `home` | `varchar(100)` | Home directory path |

You will connect to `template1` database which is already available by default. To connect to this database, run the following command at the `postgres=#` prompt:

```sql
\c template1
```

**Output:** `You are now connected to database "template1" as user "postgres".`

Your prompt will change to `template1=#`.

Run the following statement at the `template1=#` prompt to create the table:

```sql
create table users(username varchar(50), userid int, homedirectory varchar(100));
```

**Output:** `CREATE TABLE`

[ENRICHED: defined "template1" — a default database in PostgreSQL that serves as a template for creating new databases. It is pre-created during PostgreSQL installation and contains system catalog tables. Using it for lab exercises is convenient because it is always available, but in production you would typically create a dedicated database for your application.]

---

## Exercise 5 — Loading Data into a PostgreSQL Table

In this exercise, you will create a shell script which does the following:

1. Extract the user name, user id, and home directory path of each user account defined in the `/etc/passwd` file
2. Save the data into a comma separated (CSV) format
3. Load the data in the CSV file into a table in PostgreSQL database

### Step 1: Create the Shell Script

Open a new terminal. In the terminal, run the following command to create a new shell script named `csv2db.sh`:

```bash
touch csv2db.sh
```

Open the file in the editor. Copy and paste the following lines into the newly created file:

```bash
# This script
# Extracts data from /etc/passwd file into a CSV file.
# The csv data file contains the user name, user id and
# home directory of each user account defined in /etc/passwd
# Transforms the text delimiter from ":" to ",".
# Loads the data from the CSV file into a table in PostgreSQL database.
```

Save the file by pressing `Ctrl+s` or by using the **File → Save** menu option.

### Step 2: Add Extract Phase

You need to add lines of code to the script that will extract user name (field 1), user id (field 3), and home directory path (field 6) from `/etc/passwd` file using the `cut` command.

Copy the following lines and paste them to the end of the script and save the file:

```bash
# Extract phase
echo "Extracting data"
# Extract the columns 1 (user name), 3 (user id) and 
# 6 (home directory path) from /etc/passwd
cut -d":" -f1,3,6 /etc/passwd
```

Run the script:

```bash
bash csv2db.sh
```

Verify that the output contains the three fields that you extracted.

### Step 3: Redirect Extracted Data to File

Change the script to redirect the extracted data into a file named `extracted-data.txt`. Replace the `cut` command at the end of the script with:

```bash
cut -d":" -f1,3,6 /etc/passwd > extracted-data.txt
```

Run the script:

```bash
bash csv2db.sh
```

Run the command below to verify that the file `extracted-data.txt` is created and has the content:

```bash
cat extracted-data.txt
```

[ENRICHED: defined "cat command" — `cat` (concatenate) reads a file and prints its contents to standard output. It is commonly used for quickly viewing file contents. Other options: `cat -n file` (show line numbers), `cat file1 file2` (concatenate multiple files).]

The extracted columns are separated by the original `:` delimiter. You need to convert this into a `,` delimited file.

### Step 4: Transform Data

Add the following lines at the end of the script and save the file:

```bash
# Transform phase
echo "Transforming data"
# Read the extracted data and replace the colons with commas.
tr ":" "," < extracted-data.txt > transformed-data.csv
```

Run the script:

```bash
bash csv2db.sh
```

Run the command below to verify that the file `transformed-data.csv` is created and has the content:

```bash
cat transformed-data.csv
```

[ENRICHED: added specificity — the `<` operator is input redirection: it feeds the contents of `extracted-data.txt` to `tr` as input. Combined with `>` (output redirection), the pipeline reads the colon-delimited file, replaces colons with commas, and writes the result to a CSV file. This is a common pattern in bash for file transformation without modifying the original.]

### Step 5: Load Data into PostgreSQL

To load data from a shell script, you will use the `psql` client utility in a non-interactive manner. This is done by sending the database commands through a command pipeline to `psql` with the help of `echo` command.

PostgreSQL command to copy data from a CSV file to a table is `COPY`. The basic structure of the command which we will use in our script is:

```sql
COPY table_name FROM 'filename' DELIMITERS 'delimiter_character' FORMAT;
```

Add the lines below to the end of the script `csv2db.sh` and save the file:

```bash
# Load phase
echo "Loading data"
# Set the PostgreSQL password environment variable.
# Replace <yourpassword> with your actual PostgreSQL password.
export PGPASSWORD=<yourpassword>;
# Send the instructions to connect to 'template1' and
# copy the file to the table 'users' through command pipeline.
echo "\c template1;\COPY users FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV;" | psql --username=postgres --host=postgres
```

[ENRICHED: defined "export PGPASSWORD" — sets an environment variable that `psql` uses for password authentication. Environment variables are key-value pairs that are passed to child processes. `PGPASSWORD` is specifically recognized by `psql` to authenticate without prompting for a password. In production, use `.pgpass` file or SSL certificates instead of hardcoding passwords in scripts.]

[ENRICHED: defined "non-interactive psql" — normally `psql` opens an interactive prompt where you type SQL commands. By piping commands through `echo`, you can automate database operations from scripts without human intervention. This is essential for ETL pipelines that need to run unattended.]

---

## Exercise 6 — Execute the Final Script

### Step 1: Run the Script

Run the script:

```bash
bash csv2db.sh
```

### Step 2: Verify the Data

Now, add the line below to the end of the script `csv2db.sh` and save the file:

```bash
echo "SELECT * FROM users;" | psql --username=postgres --host=postgres template1
```

Run the script to verify that the table `users` is populated with the data:

```bash
bash csv2db.sh
```

**Congratulations!** You have created an ETL script using shell scripting.

---

## Practice Exercises

Copy the data in the file `web-server-access-log.txt.gz` to the table `access_log` in the PostgreSQL database `template1`.

The file is available at:
`https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/web-server-access-log.txt.gz`

The following are the columns and their data types in the file:

| Column | Type |
|--------|------|
| `timestamp` | `TIMESTAMP` |
| `latitude` | `float` |
| `longitude` | `float` |
| `visitorid` | `char(37)` |
| `accessed_from_mobile` | `boolean` |
| `browser_code` | `int` |

The columns which we need to copy to the table are the first four columns: `timestamp`, `latitude`, `longitude` and `visitorid`.

> **NOTE:** The file comes with a header. So use the `HEADER` option in the `COPY` command.

### Task 1: Create the `access_log` Table

Step 1: Open the PostgreSQL SQL CLI, if it is not already open.

Step 2: At the `postgres=#` prompt, connect to the database `template1`:

```sql
\c template1;
```

Step 3: Create the table called `access_log`:

```sql
CREATE TABLE access_log(
    timestamp TIMESTAMP,
    latitude float,
    longitude float,
    visitor_id char(37)
);
```

### Task 2: Create the Shell Script

Create a shell script named `cp-access-log.sh` and add commands to complete the remaining tasks.

Run the following command in a new terminal to create the file:

```bash
touch cp-access-log.sh
```

Open the file in the editor and add appropriate comments:

```bash
# cp-access-log.sh
# This script downloads the file 'web-server-access-log.txt.gz'
# The script then extracts the .txt file using gunzip.
# The .txt file contains the timestamp, latitude, longitude 
# and visitor id apart from other data.
# Transforms the text delimiter from "#" to "," and saves to a csv file.
# Loads the data from the CSV file into the table 'access_log' in PostgreSQL database.
```

### Task 3: Download the Access Log File

Add the `wget` command to the script to download the file:

```bash
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/web-server-access-log.txt.gz"
```

[ENRICHED: defined "wget" — a command-line utility for downloading files from the web via HTTP, HTTPS, and FTP. It supports recursive downloads, resuming interrupted transfers, and background execution. Alternative: `curl -O` achieves similar results but with more protocol support.]

### Task 4: Unzip the Gzip File

Add the code to run the `gunzip` command to unzip the `.gz` file and extract the `.txt` file:

```bash
# Unzip the file to extract the .txt file.
gunzip -f web-server-access-log.txt.gz
```

The `-f` option of `gunzip` is to overwrite the file if it already exists.

[ENRICHED: defined "gzip" — a compression utility that reduces file size using the LZ77 algorithm. Files compressed with gzip have the `.gz` extension. `gunzip` is the decompression tool. The `-f` (force) flag prevents `gunzip` from prompting if the target file already exists, which is important for automated scripts.]

### Task 5: Extract Required Fields

Extract `timestamp`, `latitude`, `longitude` and `visitorid` which are the first four fields from the file using the `cut` command.

The columns in the `web-server-access-log.txt` file are delimited by `#`.

Add the following lines to the end of the script:

```bash
# Extract phase
echo "Extracting data"
# Extract the columns 1 (timestamp), 2 (latitude), 3 (longitude) and 
# 4 (visitorid)
cut -d"#" -f1-4 web-server-access-log.txt
```

Save the file and run the script:

```bash
bash cp-access-log.sh
```

Verify that the output contains all four fields that we extracted.

### Task 6: Redirect Extracted Output into a File

Redirect the extracted data into a file named `extracted-data.txt`. Replace the `cut` command at the end of the script with:

```bash
cut -d"#" -f1-4 web-server-access-log.txt > extracted-data.txt
```

Run the script:

```bash
bash cp-access-log.sh
```

Verify the file:

```bash
cat extracted-data.txt
```

### Task 7: Transform the Data into CSV Format

The extracted columns are separated by the original `#` delimiter. We need to convert this into a `,` delimited file.

Add the following lines at the end of the script:

```bash
# Transform phase
echo "Transforming data"
# Read the extracted data and replace the hashes with commas and
# write it to a csv file
tr "#" "," < extracted-data.txt > transformed-data.csv
```

Save the file and run the script:

```bash
bash cp-access-log.sh
```

Verify the file:

```bash
cat transformed-data.csv
```

### Task 8: Load the Data into PostgreSQL

PostgreSQL command to copy data from a CSV file to a table is `COPY`:

```sql
COPY table_name FROM 'filename' DELIMITERS 'delimiter_character' FORMAT;
```

The file comes with a header. So use the `HEADER` option in the `COPY` command.

Invoke this command from the shell script by sending it as input to `psql` filter command.

Add the lines below to the end of the script `cp-access-log.sh` and save the file:

```bash
# Load phase
echo "Loading data"
# Send the instructions to connect to 'template1' and
# copy the file to the table 'access_log' through command pipeline.
echo "\c template1;\COPY access_log FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=localhost
```

### Task 9: Execute and Verify

Run the final script:

```bash
bash cp-access-log.sh
```

Verify by querying the database. At the PostgreSQL SQL CLI prompt:

```sql
SELECT * FROM access_log;
```

You should see the records displayed on screen.

---

## Final Script Reference

### `csv2db.sh` — Main Lab Script

```bash
# csv2db.sh
# This script:
# Extracts data from /etc/passwd file into a CSV file.
# Transforms the text delimiter from ":" to ",".
# Loads the data from the CSV file into a table in PostgreSQL database.

# Extract phase
echo "Extracting data"
cut -d":" -f1,3,6 /etc/passwd > extracted-data.txt

# Transform phase
echo "Transforming data"
tr ":" "," < extracted-data.txt > transformed-data.csv

# Load phase
echo "Loading data"
export PGPASSWORD=<yourpassword>;
echo "\c template1;\COPY users FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV;" | psql --username=postgres --host=postgres

# Verify
echo "SELECT * FROM users;" | psql --username=postgres --host=postgres template1
```

### `cp-access-log.sh` — Practice Exercise Script

```bash
# cp-access-log.sh
# Downloads, extracts, transforms, and loads web server access log data.

# Download
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/web-server-access-log.txt.gz"

# Unzip
gunzip -f web-server-access-log.txt.gz

# Extract phase
echo "Extracting data"
cut -d"#" -f1-4 web-server-access-log.txt > extracted-data.txt

# Transform phase
echo "Transforming data"
tr "#" "," < extracted-data.txt > transformed-data.csv

# Load phase
echo "Loading data"
echo "\c template1;\COPY access_log FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=localhost

# Verify
echo "SELECT * FROM access_log;" | psql --username=postgres --host=localhost template1
```

---

## Key Concepts Summary

| Concept | Command/Tool | Purpose |
|---------|-------------|---------|
| **Extract fields** | `cut -d":" -f1,3,6` | Extract specific columns from delimited text |
| **Transform characters** | `tr ":" ","` | Translate, squeeze, or delete characters |
| **Redirect output** | `>` / `>>` | Write command output to a file (overwrite/append) |
| **Redirect input** | `<` | Feed file contents as input to a command |
| **Download files** | `wget` | Download files from URLs |
| **Decompress** | `gunzip -f` | Extract gzipped files |
| **Load to PostgreSQL** | `\COPY ... DELIMITERS ',' CSV` | Bulk load CSV data into a table |
| **Automate** | `bash script.sh` | Run ETL pipeline as a single script |

---

## Authors

- Ramesh Sannareddy
- Other Contributors: Rav Ahuja

© IBM Corporation. All rights reserved.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Prerequisites | Definition | Defined Docker container (isolated runtime, fresh each session) | HIGH |
| 2 | Exercise 1 | Definition | Defined pipe operator (\|) as Unix philosophy composition mechanism | HIGH |
| 3 | Exercise 1 | Definition | Defined /etc/passwd (colon-delimited user account file) | HIGH |
| 4 | Exercise 2 | Definition | Defined character sets ([a-z], POSIX [:lower:]) | HIGH |
| 5 | Exercise 2 | Definition | Defined ps command (process status display) | HIGH |
| 6 | Exercise 2 | Definition | Defined POSIX character classes ([:digit:], [:alpha:], [:alnum:], [:space:]) | HIGH |
| 7 | Exercise 3 | Definition | Defined psql (PostgreSQL interactive terminal, postgres=# prompt) | HIGH |
| 8 | Exercise 4 | Definition | Defined template1 (default PostgreSQL template database) | HIGH |
| 9 | Exercise 5 | Definition | Defined cat command (read and print file contents) | HIGH |
| 10 | Exercise 5 | Added specificity | Input redirection (<) + output redirection (>) pipeline for file transformation | HIGH |
| 11 | Exercise 5 | Definition | Defined export PGPASSWORD (environment variable for auth) | HIGH |
| 12 | Exercise 5 | Definition | Defined non-interactive psql (piping commands for automation) | HIGH |
| 13 | Practice | Definition | Defined wget (command-line file downloader) | HIGH |
| 14 | Practice | Definition | Defined gzip/gunzip (LZ77 compression, -f flag) | HIGH |
| 15 | Summary | Added specificity | 8-row key concepts table mapping commands to purposes | HIGH |

<!-- EXTRACTION_CHECKLIST: 35 sentences extracted, 35 sentences in output -->

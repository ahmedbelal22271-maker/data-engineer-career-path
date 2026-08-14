# WSL Commands Guide — Apache Kafka 3.7.0 Setup & Management

This reference guide provides step-by-step commands to download, extract, configure, start, and manage Apache Kafka (v3.7.0 in KRaft mode) inside your Windows Subsystem for Linux (WSL2) environment.

---

## Phase 1: Download & Extract Kafka 3.7.0

### Step 1: Navigate to your Linux Home Directory
* **When to run:** Run when you open your WSL terminal to ensure Kafka is installed inside your Linux home directory.
```bash
cd ~
```

### Step 2: Download the Official Kafka 3.7.0 Archive
* **When to run:** Run once to fetch the official Scala 2.12 binary distribution of Kafka 3.7.0 (~115 MB).
```bash
wget https://archive.apache.org/dist/kafka/3.7.0/kafka_2.12-3.7.0.tgz
```
* **Explanation:** `wget` is a command-line tool for downloading files directly from web servers.

### Step 3: Extract the Tarball Archive
* **When to run:** Run after the download finishes to unpack the compressed `.tgz` file.
```bash
tar -xzf kafka_2.12-3.7.0.tgz
```
* **Explanation:** 
  * `-x`: Extract files from archive.
  * `-z`: Uncompress `.gzip` format.
  * `-f`: Read from the specified file path.

### Step 4: Enter the Extracted Kafka Directory
* **When to run:** Run to enter the root directory of your Kafka installation.
```bash
cd kafka_2.12-3.7.0
```

---

## Phase 2: Configure Storage Directories (KRaft Mode)

> **Note on Kafka Architecture:** Modern Kafka (v3.0+) uses **KRaft** (Kafka Raft Metadata mode) instead of ZooKeeper. KRaft mode is faster and requires formatting a cluster storage ID before the first server boot.

### Step 1: Generate a Random Cluster ID
* **When to run:** Run before formatting your log directories for the first time.
```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```
* **Explanation:** Generates a unique 22-character base64 string that identifies your Kafka cluster.

### Step 2: Format the Log Storage Directory
* **When to run:** Run once after generating your Cluster ID to prepare the storage metadata.
```bash
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
```
* **Explanation:** 
  * `-t`: Specifies the Cluster ID generated in Step 1.
  * `-c`: Specifies the configuration file (`server.properties`).

---

## Phase 3: Starting & Running the Kafka Server

### Option A: Start Kafka in the Foreground (Logs Visible)
* **When to run:** Use when you want to watch the real-time startup logs in your active terminal.
```bash
bin/kafka-server-start.sh config/kraft/server.properties
```
* **To stop Kafka in foreground mode:** Press `Ctrl + C`.

### Option B: Start Kafka in the Background (Frees Terminal)
* **When to run:** Use when you want Kafka running quietly in the background so you can use the same terminal window for other commands.
```bash
bin/kafka-server-start.sh config/kraft/server.properties &
```
* **Explanation:** The trailing `&` sends the process to run in the background.

---

## Phase 4: Key Management & Lab Commands

### 1. Create the `toll` Topic
* **When to run:** Run after starting Kafka to create the topic for streaming vehicle events.
```bash
bin/kafka-topics.sh --create --topic toll --bootstrap-server localhost:9092
```

### 2. Verify Topic Creation
* **When to run:** Run to list all active topics on your Kafka broker.
```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 3. Check if Kafka Process is Running
* **When to run:** Run to verify whether the Kafka broker process is active.
```bash
ps aux | grep -i kafka
```

### 4. Gracefully Stop Kafka
* **When to run:** Run when you finish your lab work and want to shut down the Kafka broker cleanly.
```bash
bin/kafka-server-stop.sh
```

---

## Phase 5: MySQL Database Server Setup & Configuration

### Step 1: Install MySQL Server in WSL
```bash
sudo apt update && sudo apt install -y mysql-server
```

### Step 2: MySQL Service Management
```bash
sudo service mysql start
sudo service mysql status
sudo service mysql stop
```

### Step 3: Configure Root Password & Authentication
```bash
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'Ah22059038!@#'; FLUSH PRIVILEGES;"
```

### Step 4: Accessing the Interactive MySQL Shell
```bash
mysql -u root -p'Ah22059038!@#'
```

---

## Phase 6: Lab Database (`tolldata`) & Schema (`livetolldata`) Setup

```sql
CREATE DATABASE IF NOT EXISTS tolldata;
USE tolldata;

CREATE TABLE IF NOT EXISTS livetolldata (
    timestamp DATETIME,
    vehicle_id INT,
    vehicle_type VARCHAR(15),
    toll_plaza_id INT
);
```

---

## Phase 7: Real-Time Streaming Data Verification & Maintenance Queries

```sql
-- 1. Check Streamed Row Count
SELECT COUNT(*) AS total_records FROM livetolldata;

-- 2. View Latest Streamed Vehicles
SELECT * FROM livetolldata ORDER BY timestamp DESC LIMIT 10;

-- 3. Aggregate Vehicles by Type
SELECT vehicle_type, COUNT(*) AS count FROM livetolldata GROUP BY vehicle_type;

-- 4. Aggregate Records by Toll Plaza ID
SELECT toll_plaza_id, COUNT(*) AS total_vehicles FROM livetolldata GROUP BY toll_plaza_id;
```

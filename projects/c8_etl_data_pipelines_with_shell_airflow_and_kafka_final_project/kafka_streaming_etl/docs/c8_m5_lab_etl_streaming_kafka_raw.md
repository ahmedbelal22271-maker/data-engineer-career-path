



# Hands-on Lab: Build a Streaming ETL Pipeline using Kafka

![Skills Network logo](assets/c8_m5_skills_network_logo.jpg)

The logo for Skills Network, featuring a stylized network diagram with nodes and connecting lines, enclosed within a circular border.

Skills Network logo

**Skills**  
Network

Estimated time needed: **45** minutes.

## Project scenario

You are a data engineer at a data analytics consulting company. You have been assigned to a project that aims to de-congest the national highways by analyzing the road traffic data from different toll plazas. As a vehicle passes a toll plaza, the vehicle's data like `vehicle_id`, `vehicle_type`, `toll_plaza_id`, and timestamp are streamed to Kafka. Your job is to create a data pipe line that collects the streaming data and loads it into a database.

## Objectives

In this assignment, you will create a streaming data pipe by performing these steps:

- Start a MySQL database server
- Create a table to hold the toll data

- Install the Kafka Python driver
- Install the MySQL Python driver
- Create a topic named toll in Kafka
- Download streaming data generator program
- Customize the generator program to stream to toll topic
- Download and customize streaming data consumer
- Customize the consumer program to write into a MySQL database table
- Verify that streamed data is being collected in the database table

## Note about screenshots

Throughout this lab, you will be prompted to take screenshots and save them on your device. You will need to upload the screenshots for peer review. You can use various free screen grabbing tools or your operating system's shortcut keys (Alt + PrintScreen in Windows, for example) to capture the required screenshots. You can save the screenshots with the `.jpg` or `.png` extension.

## About Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands-on labs for course and project-related labs. Theia is an open-source IDE (Integrated Development Environment) that can be run on a desktop or on the cloud. To complete this lab, you will be using the Cloud IDE based on Theia, running in a Docker container.

## Important notice about this lab environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

## Exercise 1: Download and extract Kafka

1. Download Kafka by running the command below.

![code icon](assets/c8_m5_streaming_kafka_code_icon_3.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_1.jpg)

```
wget https://archive.apache.org/dist/kafka/3.7.0/kafka_2.12-3.7.0.tgz
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_3.jpg) Run

2. Extract Kafka from the zip file by running the command below.

![code icon](assets/c8_m5_streaming_kafka_code_icon_2.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_2.jpg)

```
tar -xzf kafka_2.12-3.7.0.tgz
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_4.jpg) Run

**Note:** This command creates a directory named `kafka_2.12-3.7.0` in the current directory.

## Exercise 2: Configure KRaft and start server

1. Change to the `kafka_2.12-3.7.0` directory.

![code icon](assets/c8_m5_streaming_kafka_code_icon_3.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_3.jpg)

```
cd kafka_2.12-3.7.0
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_3.jpg) Run

2. Generate a cluster UUID that will uniquely identify the Kafka cluster.

![code icon](assets/c8_m5_streaming_kafka_code_icon_4.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_4.jpg)

```
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_4.jpg) Run

**Note:** The new cluster id generated will be used by the KRaft controller.

3. KRaft requires the log directories to be configured. Run the following command to configure the log directories passing the cluster id.

![code icon](assets/c8_m5_streaming_kafka_code_icon_5.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_5.jpg)

```
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_5.jpg) Run

4. Now that KRaft is configured, you can start the Kafka server by running the following command.

![code icon](assets/c8_m5_streaming_kafka_code_icon_6.jpg) plaintext ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_6.jpg)

```
bin/kafka-server-start.sh config/kraft/server.properties
```

*Note: You can be sure that the Kafka server started there is information generated that the server started successfully along with some additional messages, such as log loaded.*

```
[2024-06-12 02:19:51,129] INFO [BrokerServer id=1] Transition from STARTING to STARTED (kafka.server.BrokerServer)
[2024-06-12 02:19:51,130] INFO Kafka version: 3.7.0 (org.apache.kafka.common.utils.AppInfoParser)
[2024-06-12 02:19:51,135] INFO Kafka commitId: 2ae524ed625438c5 (org.apache.kafka.common.utils.AppInfoParser)
[2024-06-12 02:19:51,135] INFO Kafka startTimeMs: 1718173191129 (org.apache.kafka.common.utils.AppInfoParser)
[2024-06-12 02:19:51,137] INFO [KafkaRaftServer nodeId=1] Kafka Server started (kafka.server.KafkaRaftServer)
[2024-06-12 02:20:25,678] INFO [ReplicaFetcherManager on broker 1] Removed fetcher for partitions Set(bankbranch-1, bankbranch-0) (kafka.server.ReplicaFetcherManager)
[2024-06-12 02:20:25,718] INFO [LogLoader partition=bankbranch-1, dir=/tmp/kraft-combined-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.UnifiedLog$)
[2024-06-12 02:20:25,722] INFO Created log for partition bankbranch-1 in /tmp/kraft-combined-logs/bankbranch-1 with properties {} (kafka.log.LogManager)
[2024-06-12 02:20:25,725] INFO [Partition bankbranch-1 broker=1] No checkpointed highwatermark is found for partition bankbranch-1 (kafka.cluster.Partition)
[2024-06-12 02:20:25,727] INFO [Partition bankbranch-1 broker=1] Log loaded for partition bankbranch-1 with initial high watermark 0 (kafka.cluster.Partition)
[2024-06-12 02:20:25,745] INFO [LogLoader partition=bankbranch-0, dir=/tmp/kraft-combined-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.UnifiedLog$)
[2024-06-12 02:20:25,746] INFO Created log for partition bankbranch-0 in /tmp/kraft-combined-logs/bankbranch-0 with properties {} (kafka.log.LogManager)
```

## Exercise 3: Start MySQL server and setup the database

Open MySQL Page in IDE

1. On the launching page, click the **Create** button.

![Screenshot of the MySQL IDE interface showing the 'Create' button highlighted with a red box.](assets/c8_m5_streaming_kafka_mysql_create_button.jpg)

A screenshot of the MySQL IDE interface. The top menu bar includes File, Edit, Selection, View, Go, Run, Terminal, and Help. Below the menu bar is a toolbar with icons for file operations. The main panel displays the MySQL status, showing 'MySQL' with an 'INACTIVE' button. Below this, it lists versions: 8.0.22, 5.0.4, and 2.0.2. A message states: 'Connect to MySQL and phpMyAdmin directly in your Skills Network Labs environment.' Below this message are two buttons: 'Create' (highlighted with a red box) and 'Delete'. At the bottom, there are tabs for 'Summary', 'Connection Information', and 'Details'.

Screenshot of the MySQL IDE interface showing the 'Create' button highlighted with a red box.

2. Once the MySQL server started, select the **Connection Information** tab. From that, copy the password.

![Screenshot of the MySQL IDE interface showing the 'Connection Information' tab highlighted with a red box.](assets/c8_m5_streaming_kafka_mysql_connection_info.jpg)

A screenshot of the MySQL IDE interface, showing the 'Connection Information' tab selected and highlighted with a red box. The status of the MySQL server is now 'ACTIVE'. The 'Create' button is disabled, and the 'Delete' button is active. The 'Summary' tab is also visible. The main panel displays the following text: 'Your database and phpMyAdmin server are now ready to use and available with the following login credentials. For more details on how to navigate MySQL, please check out the Details section.' Below this, it says 'You can manage MySQL via:' followed by a 'phpMyAdmin' button and a link icon. At the bottom, it says 'Or to interact with the database in the terminal, select one of these options:'.

Screenshot of the MySQL IDE interface showing the 'Connection Information' tab highlighted with a red box.

![Screenshot of a MySQL configuration interface showing fields for URL, CLI Command, Command, Password, Title, and ID.](assets/c8_m5_streaming_kafka_mysql_config_interface.jpg)

A screenshot of a MySQL configuration interface. It features several input fields with labels: 'MYSQL\_URL:' with a value 'https://labs-mysql-melted-huge-solstice.mysql.databases.labs.skills.network'; 'MySQL CLI Command:' with a value 'mysql --host=172.21.26.207 --port=3306 --user=root --password=vd6sFvnG62MCpW4grvhC3Cav'; 'MYSQL\_COMMAND:' with the same command; 'MYSQL\_PASSWORD:' with the same password (highlighted with a red box); 'MYSQL\_TITLE:' with a value 'MySQL Database'; and 'MYSQL\_ID:' with a value 'labs-mysql-melted-huge-solstice'. The interface has a dark theme and a sidebar with icons on the left.

Screenshot of a MySQL configuration interface showing fields for URL, CLI Command, Command, Password, Title, and ID.

3. Connect to the MySQL server using the command below in the terminal. Make sure you use the password given to you when the MySQL server starts. Please make a note of the password because you will need it later.

![code icon](assets/c8_m5_streaming_kafka_code_icon_7.jpg) plaintext ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_7.jpg)

```
mysql --host=mysql --port=3306 --user=root --password=Replace you
```

4. Create a database named `tolldata`.

At the **mysql>** prompt, run the command below to create the database.

![code icon](assets/c8_m5_streaming_kafka_code_icon_8.jpg) plaintext ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_8.jpg)

```
create database tolldata;
```

5. Create a table named `livetolldata` with the schema to store the data generated by the traffic simulator.

Run the following command to create the table:

![Code icon](assets/c8_m5_streaming_kafka_code_icon_9.jpg)

Code icon

sql

![Copy icon](assets/c8_m5_streaming_kafka_copy_icon_9.jpg)

Copy icon

```
use tolldata;
```

```
create table livetolldata(timestamp datetime,vehicle_id int,vehi
```

**Note:** This is the table where you will store all streamed data that comes from Kafka. Each row is a record of when a vehicle has passed through a certain toll plaza along with its type and anonymized id.

6. Disconnect from the MySQL server.

![Code icon](assets/c8_m5_streaming_kafka_code_icon_10.jpg)

Code icon

plaintext

![Copy icon](assets/c8_m5_streaming_kafka_copy_icon_10.jpg)

Copy icon

```
exit
```

## Exercise 4: Install the Python packages

1. Install the Python module `kafka-python`. This Python module will help you to communicate with kafka server. It can used to send and receive messages from Kafka.

![Code icon](assets/c8_m5_streaming_kafka_code_icon_11.jpg)

Code icon

plaintext

![Copy icon](assets/c8_m5_streaming_kafka_copy_icon_11.jpg)

Copy icon

```
pip3 install kafka-python
```

2. Install the Python module `mysql-connector-python` using the `pip` command.

![Code icon](assets/c8_m5_streaming_kafka_code_icon_12.jpg)

Code icon

plaintext

![Copy icon](assets/c8_m5_streaming_kafka_copy_icon_12.jpg)

Copy icon

```
pip3 install mysql-connector-python==8.0.31
```

This Python module will help you to interact with MySQL server.

## Exercise 5: Create data pipeline for toll data

1. Create a Kafka topic named `toll`.
2. Download the `toll_traffic_generator.py` from the url given below using `wget`.

![code icon](assets/c8_m5_streaming_kafka_code_icon_13.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_13.jpg)

```
wget https://cf-courses-data.s3.us.cloud-object-storage.ap
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_6.jpg) Run

3. Open the code using the editor using the "Menu --> File --> Open" option.
4. Open the `toll_traffic_generator.py` and set the topic to `toll`.
5. Run the `toll_traffic_generator.py`.

![code icon](assets/c8_m5_streaming_kafka_code_icon_14.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_14.jpg)

```
python3 toll_traffic_generator.py
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_7.jpg) Run

6. Download the `streaming-data-reader.py` from the URL below using `wget`.

![code icon](assets/c8_m5_streaming_kafka_code_icon_15.jpg) bash ![copy icon](assets/c8_m5_streaming_kafka_copy_icon_15.jpg)

```
wget https://cf-courses-data.s3.us.cloud-object-storage.ap
```

![run icon](assets/c8_m5_streaming_kafka_run_icon_8.jpg) Run

7. Open the `streaming-data-reader.py` and modify the following details so that the program can connect to your MySQL server.

DATABASE

USERNAME

PASSWORD

8. Run the `streaming-data-reader.py`.

![Terminal window showing the command to run the streaming-data-reader.py script.](assets/c8_m5_streaming_kafka_terminal_streaming_reader.jpg)

A terminal window with a light gray background. The top bar is white and contains a code icon on the left, a 'bash' label in the center, and a copy icon on the right. The main area is white and contains the command `python3 streaming-data-reader.py`. A green 'Run' button with a play icon is located at the bottom right of the terminal area.

9. If you completed all the steps correctly, the streaming toll data will get stored in the table `livetolldata`. As a last step in this lab, open mysql CLI and list the top 10 rows in the table `livetolldata`.

## Authors

Ramesh Sannareddy [Lavanya T S](#)

## Other Contributors

Rav Ahuja

© IBM Corporation. All rights reserved.

# Hands-on Lab: Build a Streaming ETL Pipeline using Kafka

Estimated time needed: **45** minutes.

## Project scenario

You are a data engineer at a data analytics consulting company. You have been assigned to a project that aims to de-congest the national highways by analyzing the road traffic data from different toll plazas. As a vehicle passes a toll plaza, the vehicle's data like `vehicle_id`, `vehicle_type`, `toll_plaza_id`, and timestamp are streamed to Kafka. Your job is to create a data pipe line that collects the streaming data and loads it into a database.

## Objectives

In this assignment, you will create a streaming data pipe by performing these steps:

- Start a MySQL database server
- Create a table to hold the toll data
- Start the Kafka server
- Install the Kafka Python driver
- Install the MySQL Python driver
- Create a topic named toll in Kafka
- Download streaming data generator program
- Customize the generator program to stream to toll topic
- Download and customize streaming data consumer

table

- Verify that streamed data is being collected in the database table

## Note about screenshots

Throughout this lab, you will be prompted to take screenshots and save them on your device. You will need to upload the screenshots for peer review. You can use various free screen grabbing tools or your operating system's shortcut keys (Alt + PrintScreen in Windows, for example) to capture the required screenshots. You can save the screenshots with the `.jpg` or `.png` extension.

---

About Skills Network Clo... →

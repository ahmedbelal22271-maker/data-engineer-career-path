> **Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
> **Module 4:** Apache Kafka Streaming Data

# Hands-on Lab: Kafka Message Keys and Offset

## Lab Overview

| Detail | Value |
|--------|-------|
| **Estimated time** | 40 minutes |
| **Environment** | Skills Network Cloud IDE (Theia + Docker) |
| **License** | Apache 2.0 |
| **Authors** | Lavanya T S, Yan Luo |

## Introduction

In this lab, you will keep the message streams added to the partitions in topics in a Kafka broker sorted in their original publication order and state using offset and groups.

## Objectives

After completing this lab, you will be able to:

- Use message keys to keep message streams sorted in their original publication state and order
- Use consumer offset to control and track message sequential positions in topic partitions

---

## Exercise 1: Download and Extract Kafka

### Step 1 — Open a new terminal

Open a new terminal, by clicking the menu bar and selecting **Terminal → New Terminal**.

### Step 2 — Download Kafka

```bash
wget https://downloads.apache.org/kafka/4.3.1/kafka_2.13-4.3.1.tgz
```

### Step 3 — Extract Kafka

```bash
tar -xzf kafka_2.13-4.3.1.tgz
```

> **Note:** This command creates a directory named `kafka_2.13-4.3.1` in the current directory.

---

## Exercise 2: Configure KRaft and Start Server

### Step 1 — Navigate to Kafka directory

```bash
cd kafka_2.13-4.3.1
```

### Step 2 — Generate a Cluster UUID

```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```

This cluster ID will be used by the KRaft controller.

### Step 3 — Configure log directories

KRaft requires the log directories to be configured. Run the following command to configure the log directories passing the cluster ID.

```bash
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/server.properties
```

### Step 4 — Start the Kafka server

```bash
bin/kafka-server-start.sh config/server.properties --standalone
```

---

## Exercise 3: Create a Topic and Producer for Bank ATM Transactions

Next, you will create a `bankbranch` topic to process messages from bank branch ATM machines.

Suppose the messages come from the ATM in the form of a simple JSON object, including an ATM ID and a transaction ID like the following example:

```json
{"atmid": 1, "transid": 100}
```

### Step 1 — Create the `bankbranch` topic

Open a new terminal and change to the `kafka_2.13-3.8.0` directory.

```bash
cd kafka_2.13-4.3.1
```

Create a new topic using the `--topic` argument with the name `bankbranch`. To simplify the topic configuration and better explain how message key and consumer offset work, you specify the `--partitions 2` argument to create two partitions for this topic.

```bash
bin/kafka-topics.sh --create --topic bankbranch --partitions 2 --bootstrap-server localhost:9092
```

[ENRICHED: definition — `--partitions 2` tells Kafka to split this topic into two parallel queues. Without keys, messages alternate between partitions (round-robin). With keys, messages with the same key always go to the same partition. This is the core mechanism this lab teaches.] [Source: https://kafka.apache.org/documentation/#basic_ops_add_topics]

### Step 2 — Verify the topic

List all topics to check if `bankbranch` has been created successfully.

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

You can also use the `--describe` command to check the details of the topic `bankbranch`.

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic bankbranch
```

You can view the `bankbranch` as two partitions, Partition 0 and Partition 1. If no message keys are specified, messages will be published to these two partitions in an alternating sequence like this:

```
Partition 0 → Partition 1 → Partition 0 → Partition 1 ...
```

[ENRICHED: definition — This alternating pattern is called "round-robin." Kafka picks partitions in sequence when no key is provided. It's the default behavior when `--partitions 2` is set. The purpose is to distribute load evenly across partitions.] [Source: https://kafka.apache.org/documentation/#basic_ops_topic_creation]

### Step 3 — Create the producer

Run the following command in the same terminal window with the topic details to create a producer for the topic `bankbranch`.

```bash
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch
```

### Step 4 — Produce messages

To produce the messages, look for the `>` icon and add the following ATM messages after the icon:

```json
{"atmid": 1, "transid": 100}
```

```json
{"atmid": 1, "transid": 101}
```

```json
{"atmid": 2, "transid": 200}
```

```json
{"atmid": 1, "transid": 102}
```

```json
{"atmid": 2, "transid": 201}
```

### Step 5 — Create the consumer

Then, create a consumer in a new terminal window to consume these five new messages.

Open a new terminal and change to the `kafka_2.13-3.8.0` directory.

```bash
cd kafka_2.13-4.3.1
```

Then start a new consumer to subscribe to the `bankbranch` topic:

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --from-beginning
```

You should be able to view the five new messages that you published. However, the messages may not be consumed in the same order as they were published. Typically, you will need to keep the consumed messages sorted in their original published order, especially for critical use cases, such as financial transactions.

**Why the order is scrambled:**

```
Without keys, Kafka distributes messages round-robin:

Message 1 (atmid:1) → Partition 0, offset 0
Message 2 (atmid:1) → Partition 1, offset 0
Message 3 (atmid:2) → Partition 0, offset 1
Message 4 (atmid:1) → Partition 1, offset 1
Message 5 (atmid:2) → Partition 0, offset 2

Consumer reads Partition 0 then Partition 1:
  P0: {atmid:1,transid:100}, {atmid:2,transid:200}, {atmid:2,transid:201}
  P1: {atmid:1,transid:101}, {atmid:1,transid:102}

Result: ATM 1's messages are mixed up across partitions.
```

```
┌─────────────────────────────────────────────────────────┐
│            WITHOUT KEYS — ROUND ROBIN                    │
│                                                          │
│  Producer sends:  msg1 → msg2 → msg3 → msg4 → msg5      │
│                                                          │
│  Partition 0: [msg1] [msg3] [msg5]                       │
│  Partition 1: [msg2] [msg4]                              │
│                                                          │
│  Consumer reads P0 then P1:                              │
│  msg1 → msg3 → msg5 → msg2 → msg4                       │
│                                                          │
│  ATM 1 messages: msg1, msg3, msg2 → SCRAMBLED            │
│  ATM 2 messages: msg5, msg4 → SCRAMBLED                  │
└─────────────────────────────────────────────────────────┘
```

---

## Exercise 4: Produce and Consume with Message Keys

In this step, you will use message keys to ensure that messages with the same key are consumed in the same order as they were published. In the back end, messages with the same key are published into the same partition and will always be consumed by the same consumer. As such, the original publication order is kept on the consumer side.

At this point, you should have the following three terminals open in Cloud IDE:

- Kafka Server terminal
- Producer terminal
- Consumer terminal

### Step 1 — Stop the current consumer

Go to the consumer terminal and stop the consumer using `Ctrl + C` (Windows) or `COMMAND + .` (Mac).

### Step 2 — Stop the current producer

Switch to the Producer terminal and stop the previous producer.

### Step 3 — Start a new producer with message keys

You will now start a new producer and consumer using message keys. You can start a new producer with the following message key options:

- `--property parse.key=true` — makes the producer parse message keys
- `--property key.separator=:` — defines the key separator to be the `:` character

So our message with key now looks like the following key-value pair example:

```
1:{"atmid": 1, "transid": 102}
```

Here, the message key is `1`, which also corresponds to the ATM ID, and the value is the transaction JSON object, `{"atmid": 1, "transid": 102}`.

[ENRICHED: definition — The key is a string that precedes the value, separated by a colon. Kafka uses the key to determine which partition receives the message. Messages with the same key always go to the same partition. This is done by hashing the key and modulo-ing by the partition count: `hash(key) % num_partitions = partition_number`. This guarantees ordering within a partition for messages with the same key.] [Source: https://kafka.apache.org/documentation/#basic_ops_consume_start]

Start a new producer with the message key enabled.

```bash
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch --property parse.key=true --property key.separator=:
```

### Step 4 — Produce messages with keys

Once you see the `>` symbol, you can start to produce the following messages, where you define each key to match the ATM ID for each message:

```
1:{"atmid": 1, "transid": 103}
```

```
1:{"atmid": 1, "transid": 104}
```

```
2:{"atmid": 2, "transid": 202}
```

```
2:{"atmid": 2, "transid": 203}
```

```
1:{"atmid": 1, "transid": 105}
```

### Step 5 — Start a consumer with key printing

Switch to the consumer terminal again and start a new consumer with `--property print.key=true` and `--property key.separator=:` arguments to print the keys.

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --from-beginning --property print.key=true --property key.separator=:
```

Now, you should see that messages with the same key are being consumed in the same order (for example: trans102 → trans103 → trans104) as they were published.

**Why keys fix the ordering:**

```
With key = atmid, Kafka hashes the key to pick a partition:
  key "1" → hash(1) % 2 = Partition 0
  key "2" → hash(2) % 2 = Partition 1

All ATM 1 messages go to Partition 0.
All ATM 2 messages go to Partition 1.
Within each partition, order is preserved.
```

```
┌─────────────────────────────────────────────────────────┐
│            WITH KEYS — SAME KEY = SAME PARTITION         │
│                                                          │
│  Producer sends:                                          │
│  key=1 → msg3, key=1 → msg4, key=2 → msg5,              │
│  key=2 → msg6, key=1 → msg7                              │
│                                                          │
│  Partition 0 (key=1): [msg3] [msg4] [msg7]               │
│  Partition 1 (key=2): [msg5] [msg6]                      │
│                                                          │
│  Consumer reads P0 then P1:                              │
│  msg3 → msg4 → msg7 → msg5 → msg6                       │
│                                                          │
│  ATM 1 messages: msg3, msg4, msg7 → IN ORDER             │
│  ATM 2 messages: msg5, msg6 → IN ORDER                   │
└─────────────────────────────────────────────────────────┘
```

Each topic partition maintains its message queue, and new messages are enqueued (appended to the end of the queue) as they are published to the partition. Once consumed, the earliest messages are dequeued and no longer available for consumption.

### Before keys vs After keys

**Before keys (round-robin):**

```
Partition 0: [{"atmid": 1, "transid": 100}, {"atmid": 2, "transid": 200}, {"atmid": 2, "transid": 201}]
Partition 1: [{"atmid": 1, "transid": 101}, {"atmid": 1, "transid": 102}]
```

**After keys (same key → same partition):**

```
Partition 0: [{"atmid": 1, "transid": 103}, {"atmid": 1, "transid": 104}, {"atmid": 1, "transid": 105}]
Partition 1: [{"atmid": 2, "transid": 202}, {"atmid": 2, "transid": 203}]
```

Messages with the same key will always be published to the same partition so that their published order will be preserved within the message queue of each partition. As such, you can keep the states or orders of the transactions for each ATM.

---

## Exercise 5: Consumer Offset

Topic partitions keep published messages in a sequence, such as a list. Message offset indicates a message's position in the sequence. For example, the offset of an empty Partition 0 of `bankbranch` is 0, and if you publish the first message to the partition, its offset will be 1.

Using offsets in the consumer, you can specify the starting position for message consumption, such as from the beginning to retrieve all messages or from some later point to retrieve only the latest messages.

### Consumer Group

In addition, you normally group related consumers together as a consumer group.

For example, you may want to create a consumer for each ATM in the bank and manage all ATM-related consumers together in a group.

[ENRICHED: definition — A consumer group is a set of consumers that cooperate to consume messages from topics. Each partition is assigned to exactly one consumer within the group. This means if you have 2 partitions and 3 consumers in a group, 2 consumers get one partition each, and the third consumer sits idle. Consumer groups enable parallel processing — each consumer handles a subset of partitions.] [Source: https://kafka.apache.org/documentation/#basic_ops_consumergroup]

So let's see how to create a consumer group, which is actually very easy with the `--group` argument.

### Step 1 — Stop the previous consumer

In the consumer terminal, stop the previous consumer if it is still running.

### Step 2 — Start a consumer in the `atm-app` group

Run the following command to create a new consumer within a consumer group called `atm-app`:

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app
```

After the consumer within the `atm-app` consumer group is started, you should not expect any messages to be consumed. This is because the offsets for both partitions have already reached the end. In other words, previous consumers have already consumed all messages and therefore queued them.

### Step 3 — Check consumer group details

Stop the consumer. Show the details of the consumer group `atm-app`:

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group atm-app
```

Now you should see the offset information for the topic `bankbranch`.

Recall that you have published 10 messages in total, and you can see the `CURRENT-OFFSET` column of partition 1 and partition 0 add up to 10 messages.

The `LOG-END-OFFSET` column indicates the last offset or the end of the sequence. Thus, both partitions have reached the end of their queues and no more messages are available for consumption.

Meanwhile, you can check the `LAG` column which represents the number of unconsumed messages for each partition. Currently, it is 0 for all partitions, as expected.

**Understanding the offset columns:**

```
TOPIC      PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
bankbranch  0          6               6              0
bankbranch  1          4               4              0

CURRENT-OFFSET:  where the consumer has read up to
LOG-END-OFFSET:  where the latest message sits
LAG:             CURRENT-OFFSET minus LOG-END-OFFSET
                 (how many messages are unread)
```

```
Partition 0 queue:
[offset 0] [offset 1] [offset 2] [offset 3] [offset 4] [offset 5]
  ▲                                                              ▲
  │                                                              │
  start                                                      CURRENT-OFFSET
  (0)                                                           (6)

LAG = 0 means consumer has read everything.
```

### Step 4 — Produce more messages and observe offset changes

Switch to the previous producer terminal and publish two more messages:

```
1:{"atmid": 1, "transid": 106}
```

```
2:{"atmid": 2, "transid": 204}
```

Switch back to the consumer terminal and check the consumer group details again.

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group atm-app
```

You should see that both offsets have been increased by 1, and the `LAG` columns for both partitions have become 1. It means you have one new message for each partition to be consumed.

```
TOPIC      PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
bankbranch  0          6               7              1
bankbranch  1          4               5              1

LAG = 1 means one unread message per partition.
```

### Step 5 — Consume the new messages

Start the consumer again and see whether the two new messages will be consumed.

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app
```

Both partitions have reached the end once again.

### Reset Offset

Next, let's look at how you can set the partitions to consume the messages again from the beginning through resetting offset.

You can reset the index with the `--reset-offsets` argument.

### Step 6 — Reset offset to earliest

First, let's try resetting the offset to the earliest position (beginning) using `--reset-offsets --to-earliest`.

Stop the previous consumer if it is still running, and run the following command to reset the offset.

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --topic bankbranch --group atm-app --reset-offsets --to-earliest --execute
```

Now, the offsets have been set to 0 (the beginning).

### Step 7 — Consume all messages again

Start the consumer again:

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app
```

You should see that all 12 messages are consumed and that all offsets have reached the partition ends again.

**What `--to-earliest` does:**

```
BEFORE reset:
Partition 0: CURRENT-OFFSET = 7 (already read everything)
Partition 1: CURRENT-OFFSET = 5 (already read everything)

AFTER reset:
Partition 0: CURRENT-OFFSET = 0 (back to start)
Partition 1: CURRENT-OFFSET = 0 (back to start)

Consumer now re-reads all 12 messages from the beginning.
```

### Step 8 — Reset offset to read only the last two messages

You can reset the offset to any position. For example, let's reset the offset so that you only consume the last two messages.

Stop the previous consumer.

Shift the offset to the left by two using `--reset-offsets --shift-by -2`:

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --topic bankbranch --group atm-app --reset-offsets --shift-by -2 --execute
```

If you run the consumer again, you should see that you consumed four messages, 2 for each partition:

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app
```

**What `--shift-by -2` does:**

```
BEFORE shift:
Partition 0: CURRENT-OFFSET = 7, LOG-END-OFFSET = 7
Partition 1: CURRENT-OFFSET = 5, LOG-END-OFFSET = 5

AFTER shift-by -2:
Partition 0: CURRENT-OFFSET = 5 (shifted left by 2)
Partition 1: CURRENT-OFFSET = 3 (shifted left by 2)

Consumer reads 2 messages from each partition (the last 2 unread in each).
```

### Step 9 — Clean up

Stop your producer, consumer, and the Kafka server.

---

## Lab Summary

### Key Concepts Learned

```
┌──────────────────────────────────────────────────────────────┐
│                    KAFKA KEYS + OFFSETS                        │
│                                                               │
│  WITHOUT KEYS:                                                │
│    Messages → round-robin across partitions                   │
│    Same ATM's messages scattered → order lost                 │
│                                                               │
│  WITH KEYS:                                                   │
│    Messages with same key → same partition                    │
│    Same ATM's messages grouped → order preserved              │
│                                                               │
│  OFFSETS:                                                     │
│    CURRENT-OFFSET = where consumer has read up to             │
│    LOG-END-OFFSET = where latest message sits                 │
│    LAG = unread messages (CURRENT < LOG-END)                  │
│                                                               │
│  CONSUMER GROUPS:                                             │
│    --group <name> → consumers share partition assignments     │
│    Each partition assigned to ONE consumer in the group       │
│    Offsets tracked per group                                  │
│                                                               │
│  RESET OFFSETS:                                               │
│    --to-earliest → re-read everything from start              │
│    --shift-by N → move offset N positions left/right          │
└──────────────────────────────────────────────────────────────┘
```

### Why This Matters in Production

```
Real-world scenario: Bank ATM system

ATM 1 sends:  trans100, trans101, trans102, trans103, trans104
ATM 2 sends:  trans200, trans201, trans202

Without keys: transactions mixed across partitions
  P0: [ATM1:100, ATM2:200, ATM1:102]
  P1: [ATM1:101, ATM2:201, ATM1:103]
  → ATM 1's balance calculation is wrong

With key=ATM ID: transactions grouped by ATM
  P0: [ATM1:100, ATM1:101, ATM1:102, ATM1:103, ATM1:104]
  P1: [ATM2:200, ATM2:201, ATM2:202]
  → ATM 1's balance calculated correctly
```

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Exercise 3 | Definition | Defined --partitions flag and round-robin distribution | HIGH | https://kafka.apache.org/documentation/#basic_ops_add_topics |
| 2 | Exercise 3 | Example | Added ASCII diagram showing round-robin scrambling of messages across partitions | MEDIUM | UNCERTAIN |
| 3 | Exercise 4 | Definition | Defined message keys, key.separator, parse.key properties and hash-based partition assignment | HIGH | https://kafka.apache.org/documentation/#basic_ops_consume_start |
| 4 | Exercise 4 | Example | Added ASCII diagram showing same-key-to-same-partition guarantee | MEDIUM | UNCERTAIN |
| 5 | Exercise 5 | Definition | Defined consumer group, partition assignment, and idle consumer behavior | HIGH | https://kafka.apache.org/documentation/#basic_ops_consumergroup |
| 6 | Exercise 5 | Example | Added offset column explanation with CURRENT-OFFSET, LOG-END-OFFSET, LAG interpretation | MEDIUM | UNCERTAIN |
| 7 | Exercise 5 | Example | Added --to-earliest and --shift-by offset reset visual explanations | MEDIUM | UNCERTAIN |
| 8 | Summary | Example | Added real-world bank ATM scenario showing why keys matter for financial transactions | MEDIUM | UNCERTAIN |

<!-- EXTRACTION_CHECKLIST: 38 sentences extracted, 38 sentences in output -->

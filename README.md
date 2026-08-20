# Distributed Key-Value Store

A fault-tolerant, TCP-based distributed key-value store built from scratch in Python.

The project explores how distributed databases work internally, including TCP networking, concurrent clients, persistence, replication, heartbeats, failure detection, automatic leader failover, and client reconnection.

## Features

- TCP-based client-server architecture
- Custom command protocol
- Concurrent client handling using Python threads
- In-memory key-value storage
- `SET`, `GET`, `DEL`, and `EXISTS` commands
- Write-Ahead Logging (WAL)
- Snapshot-based persistence
- Crash recovery from WAL and snapshots
- Primary-replica replication
- Multiple replicas
- Heartbeat-based failure detection
- Automatic primary failover
- Client automatic reconnection after primary failure
- Docker-based multi-node deployment

## Architecture

```text
                       ┌──────────────┐
                       │    Client    │
                       └──────┬───────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │     Primary      │
                    │      :5000       │
                    └───────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        ┌─────────────────┐   ┌─────────────────┐
        │    Replica 1    │   │    Replica 2    │
        │      :5001      │   │      :5002      │
        └─────────────────┘   └─────────────────┘
```

When the primary fails, a replica can take over as the new primary.

```text
Primary
   │
   X  Failure
   │
   ▼
Replica 1
   │
   │ becomes primary
   ▼
Replica 2
```

## Project Structure

```text
.
├── src/
│   ├── server.py
│   ├── client.py
│   ├── database.py
│   ├── executor.py
│   │
│   ├── protocol/
│   │   ├── codec.py
│   │   └── parser.py
│   │
│   ├── storage/
│   │   ├── wal.py
│   │   └── snapshot.py
│   │
│   ├── replication/
│   │   └── client.py
│   │
│   ├── election/
│   │   ├── heartbeat.py
│   │   ├── watchdog.py
│   │   ├── leader.py
│   │   └── sender.py
│   │
│   └── cluster/
│       └── state.py
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Supported Commands

### SET

Stores a key-value pair.

```text
SET name sudhit
```

Response:

```text
OK
```

### GET

Retrieves a value.

```text
GET name
```

Response:

```text
sudhit
```

### EXISTS

Checks whether a key exists.

```text
EXISTS name
```

Response:

```text
1
```

### DEL

Deletes a key.

```text
DEL name
```

Response:

```text
OK
```

## Persistence

The store uses two persistence mechanisms.

### Write-Ahead Log

Every write is recorded in the WAL before modifying the in-memory database.

Example:

```text
SET name sudhit
SET bike duke
DEL name
```

The WAL allows the database to recover operations after a restart.

### Snapshots

After a configured number of writes, the current database state is written to a snapshot.

On startup:

```text
Snapshot
   ↓
Load database
   ↓
Replay WAL
   ↓
Recovered state
```

This reduces the amount of WAL that needs to be replayed during recovery.

## Replication

The primary replicates write operations to its replicas.

```text
Client
  │
  ▼
Primary
  │
  ├──────► Replica 1
  │
  └──────► Replica 2
```

Replicas maintain their own database and persistence files.

The project uses separate Docker volumes for each node's persistent data.

## Failure Detection

Replicas monitor the primary using periodic heartbeats.

```text
Primary ───── HEARTBEAT ─────► Replica
Primary ───── HEARTBEAT ─────► Replica
Primary ───── HEARTBEAT ─────► Replica
```

If heartbeats stop for longer than the configured timeout:

```text
No heartbeat
      ↓
Timeout detected
      ↓
Primary considered failed
      ↓
Replica starts failover
```

A replica does not immediately elect itself when starting. It first waits until it has observed a primary heartbeat, preventing a startup race where a slow-starting primary could incorrectly result in multiple primaries.

## Client Failover

The client knows about multiple nodes and attempts to connect to them in order.

If the current primary fails:

```text
Client
  │
  ├──► Primary :5000 ❌
  │
  ├──► Replica 1 :5001 ✅
  │
  └──► Continue requests
```

The goal is to allow the client to reconnect without manually restarting the application.

## Running with Docker

### Requirements

- Docker
- Docker Compose

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

Build the containers:

```bash
docker compose build
```

Start the cluster:

```bash
docker compose up
```

The cluster consists of:

```text
Primary    :5000
Replica 1  :5001
Replica 2  :5002
```

### Running the Client

Open another terminal:

```bash
docker exec -it primary bash
```

Then:

```bash
cd /app/src
python client.py
```

You can also run the client from another container depending on the Docker network configuration.

### Testing Failover

Start the cluster:

```bash
docker compose up
```

Connect a client and write some data:

```text
SET name sudhit
SET language python
GET name
```

Then stop the primary:

```bash
docker stop primary
```

The replica should detect the missing heartbeat and take over as primary.

The client can then reconnect to an available node.

### Example

Before failure:

```text
Primary
  │
  ├── SET name sudhit
  │
  ├── Replica 1
  └── Replica 2
```

After primary failure:

```text
Primary ❌

Replica 1
    │
    └── becomes PRIMARY

Replica 2
    │
    └── remains replica
```

## Technologies

- Python
- TCP/IP sockets
- Multithreading
- Docker
- Docker Compose
- Linux
- Write-Ahead Logging
- Snapshot persistence
- Replication
- Heartbeat-based failure detection

## Learning Goals

This project is primarily a systems and distributed-systems learning project.

It is designed to explore:

- How TCP connections work internally
- How servers handle multiple clients
- How databases persist data
- How replication works
- How failures are detected
- How leader failover works
- How clients recover from node failures
- How distributed systems handle consistency and availability

## Roadmap

Planned improvements:

- [ ] Proper TCP message framing
- [ ] Robust replica reconnection
- [ ] Replica catch-up after downtime
- [ ] Pub/Sub-based replication
- [ ] More robust leader election
- [ ] Multiple concurrent replicas
- [ ] Replication acknowledgements
- [ ] Improved consistency guarantees
- [ ] Performance benchmarking
- [ ] Graceful shutdown and recovery
- [ ] Automated tests

## Disclaimer

This project is an educational implementation designed to explore distributed systems concepts. It is not intended to be used as a production database.

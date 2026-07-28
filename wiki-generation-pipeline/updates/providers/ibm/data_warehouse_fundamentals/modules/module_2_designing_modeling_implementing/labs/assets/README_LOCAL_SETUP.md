# Local Docker Setup for Data Quality Lab

## Quick Start

### 1. Start PostgreSQL Container

```bash
docker run -d \
  --name postgres-dw-lab \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16
```

### 2. Verify Container is Running

```bash
docker ps | grep postgres-dw-lab
```

### 3. Create the Database

```bash
export PGPASSWORD=postgres
createdb -h localhost -U postgres -p 5432 billingDW
```

### 4. Apply the Schema

```bash
psql -h localhost -U postgres -p 5432 billingDW < star-schema.sql
```

### 5. Install Python Dependencies

```bash
pip install psycopg2 pandas tabulate
```

### 6. Update Python Scripts for Local Docker

The downloaded scripts expect the host to be `postgres` (Docker container name). For local usage, you need to change the host to `localhost` in:
- `dbconnect.py` (line 9): Change `host = "postgres"` to `host = "localhost"`
- `generate-data-quality-report.py` (line 19): Change `host = "postgres"` to `host = "localhost"`

Also update the password in both files (line 3 in dbconnect.py, line 15 in generate-data-quality-report.py).

### 7. Test Connectivity

```bash
python3 dbconnect.py
```

### 8. Run the Data Quality Report

```bash
python3 generate-data-quality-report.py
```

## Troubleshooting

### Container won't start
- Check if port 5432 is already in use: `netstat -ano | findstr :5432`
- Stop any existing PostgreSQL services

### Connection refused
- Ensure container is running: `docker ps`
- Check logs: `docker logs postgres-dw-lab`

### Authentication failed
- Verify password in Python scripts matches the POSTGRES_PASSWORD you set
- Default password in this lab: `postgres`

## Useful Commands

```bash
# Stop the container
docker stop postgres-dw-lab

# Start an existing container
docker start postgres-dw-lab

# Remove the container
docker rm postgres-dw-lab

# Connect to database interactively
docker exec -it postgres-dw-lab psql -U postgres -d billingDW
```

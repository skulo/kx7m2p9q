# Weather Sensor API

This is a FastAPI-based REST API designed to handle weather sensor data ingestion and provide aggregated query results.

## Technical Stack

- **Framework:** FastAPI (Asynchronous support, Pydantic v2 validation)
- **Database:** PostgreSQL 16
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Package Manager:** [uv](https://github.com/astral-sh/uv) (Ultra-fast Python bundler)
- **Testing:** pytest with TestClient

---

## Technical Architecture & Components

### 1. Data Models (`app/models/`)

The application uses a relational schema to ensure data integrity:

- **Sensor:** Stores metadata (`sensor_id`, `country`, `city`). The `sensor_id` is a unique string used as a natural key for external references.
- **Measurement:** Stores time-series data. Each record links to a `sensor_id` via a Foreign Key. It stores the `metric` type (e.g., temperature), the `value` (float), and a `recorded_at` timestamp.

### 2. Schemas (`app/schemas/`)

Powered by **Pydantic v2**, these classes handle:

- **Data Validation:** Ensures metrics are non-empty and dates follow ISO formats.
- **Serialization:** Converts SQLAlchemy models to JSON responses, stripping internal database IDs where necessary.

### 3. Service Layer (`app/services/`)

- **SensorService:** Manages registration and duplicate checks.
- **MeasurementService:** Handles the query logic.
  - **Date Logic:** Automatically defaults to the last 24 hours if no range is provided.
  - **Validation:** Enforces a 31-day limit on queries to prevent database performance degradation.
  - **Aggregation:** Uses SQL `AVG` and `GROUP BY` to ensure the calculation happens at the database level rather than in Python memory.

### 4. API Routes (`app/api/`)

The routes are thin wrappers that inject the database session and call the appropriate service.

---

## Testing Strategy

The project includes automated integration tests using `pytest`.

### Key Test Scenarios:

- **Registration Flow:** Verifies successful sensor creation and prevents duplicate IDs (Conflict 409).
- **Data Ingestion:** Ensures measurements can only be added to existing sensors (Not Found 404 check).
- **Aggregation Logic:** Validates that the average calculation is mathematically correct.
- **Edge Cases:** - Prevents invalid date ranges (start date > end date).
  - Returns 404 if a query yields no results instead of an empty list, providing better API feedback.

---

## Running the Project

### First time setup:

1. `git clone https://github.com/skulo/kx7m2p9q`
2. `cd kx7m2p9q`
3. `docker compose up --build`
4. The API will be available at: `http://localhost:8000/docs`

### Subsequent starts:

`docker compose up`

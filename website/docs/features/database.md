---
sidebar_position: 2
---

# Database

Equipment wraps SQLAlchemy setup in `SQLAlchemyFactory`. The generated project defaults to SQLite so the scaffold can run locally without an external database.

## Configuration

`config/database.yaml` selects the active connection:

```yaml
database:
  connection: ${DB_CONNECTION:sqlite}

  connections:
    sqlite:
      schema: sqlite
      database: "${DB_DATABASE:database/database.sqlite}"
```

The generated file also includes MySQL and PostgreSQL examples. Those require optional drivers in the generated `pyproject.toml`, such as `mysql-connector-python` or `psycopg2-binary`.

## Raw SQL

Use `app.database().text()` for SQLAlchemy text queries:

```python
from app import app

application = app()

with application.database().engine.connect() as connection:
    result = connection.execute(
        application.database().text("SELECT * FROM todos ORDER BY id DESC LIMIT 1")
    )
    latest = result.mappings().first()
```

## ORM Sessions

```python
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

from app import app


Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)


application = app()
session = application.database().session()

try:
    session.add(Todo(title="Learn Equipment", completed=False))
    session.commit()
except Exception:
    session.rollback()
    raise
finally:
    session.close()
```

## Migrations

The generated project includes an Alembic environment under `database/migrations`.

Create a migration:

```bash
cd database/migrations
alembic revision --autogenerate -m "create todos table"
```

Apply migrations:

```bash
cd database/migrations
alembic upgrade head
```

## Testing And Maintenance

- Use SQLite `:memory:` for fast unit tests when possible.
- Keep MySQL and PostgreSQL tests optional unless CI provides those services.
- Run database URL and session tests before upgrading SQLAlchemy.
- Do not commit local SQLite database files.

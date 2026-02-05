---
sidebar_position: 2
---

# Database Management

Equipment leverages [SQLAlchemy](https://www.sqlalchemy.org) to provide a powerful and flexible database management system. It supports multiple database engines and provides both low-level raw SQL execution and high-level ORM capabilities.

## Configuration

Configure your database connections in `config/database.yaml`.

```yaml
database:
  connection: ${DB_CONNECTION:sqlite}

  connections:
    sqlite:
      schema: sqlite
      database: "${DB_DATABASE:database/database.sqlite}"
    mysql:
      schema: mysql+pymysql
      host: ${DB_HOST:localhost}
      port: ${DB_PORT:3306}
      database: ${DB_DATABASE:my_app}
      username: ${DB_USERNAME:root}
      password: ${DB_PASSWORD:secret}
      charset: ${DB_CHARSET:utf8mb4}
```

## Usage

### Raw SQL Execution

For simple queries or when you need maximum performance, you can use raw SQL.

```python
from app import app

app = app()

with app.database().engine.connect() as connection:
    # Use app.database().text() for safe query building
    result = connection.execute(
        app.database().text("SELECT * FROM users WHERE active = :active"),
        {"active": True}
    )

    for row in result:
        print(row.name)
```

### SQLAlchemy ORM

For complex business logic, the ORM approach is recommended.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from app import app

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

app = app()
session = app.database().session()

try:
    # Querying
    users = session.query(User).filter(User.name == "John").all()

    # Inserting
    new_user = User(name="Jane")
    session.add(new_user)
    session.commit()
except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()
```

## Database Migrations

Equipment uses [Alembic](https://alembic.sqlalchemy.org/) for managing database schema changes.

1.  **Initialize Migrations** (already done in the scaffold):
    The `database/migrations` directory contains the Alembic environment.

2.  **Create a new migration**:
    ```bash
    cd database/migrations
    alembic revision --autogenerate -m "create users table"
    ```

3.  **Apply migrations**:
    ```bash
    cd database/migrations
    alembic upgrade head
    ```

## Best Practices

1.  **Use Migrations**: Never manually change your database schema. Always use Alembic.
2.  **Session Context**: Always ensure your sessions are properly closed using a `try...finally` block or a context manager.
3.  **Environment Variables**: Use `${DB_...}` interpolation in `database.yaml` to manage connection strings for different environments.
4.  **Validation**: Validate your model data before attempting to commit to the database.

---
sidebar_position: 1
---

# Database

## Overview
Equipment uses [SQLAlchemy](https://www.sqlalchemy.org) as its Object-Relational Mapping (ORM) framework to manage database interactions efficiently and provide a robust, flexible database layer.

## Configuration
Database connections are defined in the `config/database.yaml` configuration file. This file allows you to specify:
- Database connection strings
- Connection pool settings
- Dialect and driver configurations

## Migrations
The `database/` folder contains [Alembic](https://alembic.sqlalchemy.org) migration scripts, which provide a structured way to:
- Version control database schema changes
- Incrementally update database structure
- Roll forward or roll back schema modifications

### Run migrations

```bash
cd database/migrations
alembic upgrade head
```

## Getting Started
1. Configure your database connection in `config/database.yaml`
2. Use Alembic to manage database migrations
3. Leverage SQLAlchemy models for database interactions

## Usage Example

Here's an example of database interactions using Equipment:

```python
def database_example():
    """
    Demonstrates database interactions using Equipment's SQLAlchemy integration.

    This example shows:
    - Raw SQL query execution
    - ORM-based database operations
    """
    # Raw SQL query
    result = app.database().execute("SELECT * FROM your_table")

    # ORM-based query
    # Assuming you have defined a model class, e.g., User
    users = app.database().query(User).filter_by(active=True).all()

    # Inserting a new record
    new_user = User(name="John Doe", email="john@example.com")
    app.database().add(new_user)
    app.database().commit()
```

## Best Practices
- Always run migrations before working with the database
- Use `app.database()` for database interactions
- Use either raw SQL or ORM query methods
- Use transactions for database operations to ensure data consistency

#!/usr/bin/env python

from equipment.framework import equipment


app = equipment()

app.log().info(
    f'''

    Welcome to {app.config().get('APP', 'name')}

    Do you to access a SQL Database, a MongoDB instance, or a Redis cluster?

    Go to the root folder and run:

    $ rm main.py && mv examples/example_connection.py main.py
    $ py main.py
    '''
)

# SQL (SQLAlchemy connection)
with app.sql().factory().begin() as connection:
    result = connection.execute('SELECT 1')
    app.log().info(result)

# MongoDB connection
result = app.mongo().factory().products.insert_one(
    {'product': 'PS5', 'stock': 0}
)

app.log().info(result)

# Redis connection
app.redis().factory().set('foo', 'bar')
app.log().info(
    app.redis().factory().get('foo')
)


# Neo4J connection

# You might have a logging issue with the following message:
# "NameError: name 'open' is not defined"
# Change your logging level from DEBUG to INFO as a workaround.
# Check https://bugs.python.org/issue39513 for more details

with app.neo4j().factory().session() as session:
    app.log().info(
        session.run('MATCH (n) RETURN n LIMIT 5')
    )

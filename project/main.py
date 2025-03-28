#!/usr/bin/env python

from app import app

app = app()

app.log().info(
    f'''
    Welcome to {app.config.app.name()}

    First, install the project dependencies
    $ pipenv install

    Do you need to run scheduled tasks?
    $ py scheduler.py

    Do you need to enqueue tasks?
    $ py queues.py

    Do you need to run a web server?
    $ py web.py

    Check main.py for more examples
    '''
)


def storage_example():
    """
    Equipment Storage offers a simple Filesystem API.
    By default, it uses a Local driver based on the ./storage/app/ directory.

    Check the config/storage.yml file for more details
    """

    app.storage().write('foo.txt', 'bar')  # True if successfully written
    app.storage().exists('foo.txt')  # True
    app.storage().path('foo.txt')  # ./storage/app/foo.txt when using the Local storage driver
    app.storage().read('foo.txt')  # 'bar'
    app.storage().list('')  # ['foo.txt', '.gitignore'] when using the Local storage driver

    app.storage().move('foo.txt', 'bar.txt')  # True if successfully moved
    app.storage().exists('foo.txt')  # False
    app.storage().exists('bar.txt')  # True

    app.storage().remove('bar.txt')  # True if successfully removed
    app.storage().exists('bar.txt')  # False


def queue_example():
    """
    Equipment Storage offers an easy way to handle asynchronous tasks by using queues.

    When using the Sync driver, an inspiring quote will be logged in the current process.
    When using Redis, the quote will be logged in a queue worker. To start the worker, run the following command:
    $ py queues.py

    Check the config/queue.yml file for more details
    """

    # Results in `app.log().debug(app.inspiring().quote())`
    app.queue().push(
        app.log().debug,
        app.inspiring().quote()
    )

def database_example():
    """
    Equipment offers different database drivers to be used via SQLAlchemy.
    This example uses both raw sql and orm approaches.

    IMPORTANT: to run this example you first need to run the database migrations placed in database/migrations directory.

    $ cd database/migrations && alembic upgrade head

    Check the config/database.yml file for more details
    """

    with app.database().engine.connect() as connection:
        result = connection.execute(app.database().text(
            'SELECT * FROM todos ORDER BY id DESC LIMIT 1;'
        ))

        todo = result.mappings().first()

        if todo is not None:
            app.log().debug(f'Latest todo: {str(todo)}')
        else:
            app.log().debug('There are no todos yet')

    from sqlalchemy import BigInteger, Column, String, Boolean
    from sqlalchemy.orm import declarative_base

    class Todo(declarative_base()):
        __tablename__ = "todos"

        id = Column(BigInteger, primary_key=True, autoincrement=True)
        title = Column(String(255), nullable=False)
        completed = Column(Boolean, nullable=False)

    if todo is None:
        app.log().debug('Creating Todo...')
        session = app.database().session()

        try:
            session.add(Todo(title='Learn Equipment', completed=False))
            session.flush()
            session.commit()
            app.log().debug('Todo created')
        except Exception as e:
            session.rollback()
            app.log().warning('Could not create Todo')
            app.log().error(e)


def log_example():
    """
    Equipment offers a simple approach to handle logs by defining a log channel and a logger formatter.

    Check the config/log.yml file for more details
    """

    app.log().debug('debug')
    app.log().info('info')
    app.log().warning('warning')
    app.log().error('error')
    app.log().critical('critical')

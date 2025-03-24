from logging import Handler, LogRecord
from sqlite3 import connect, Cursor
from datetime import datetime
from json import dumps
from typing import Optional


class SQLiteLogHandler(Handler):
    baseFilename: str
    table: str = 'logs'
    pragmas: Optional[list[str]] = None
    default_pragmas: list[str] = [
        "PRAGMA journal_mode = WAL",
        "PRAGMA max_page_count = 26214400",
        "PRAGMA page_size = 4096",
        "PRAGMA cache_size = -1000000",
        "PRAGMA mmap_size = 30000000000",
        "PRAGMA temp_store = MEMORY",
        "PRAGMA threads = 4",
        "PRAGMA busy_timeout = 5000",
        "PRAGMA synchronous = NORMAL",
        "PRAGMA journal_size_limit = 67108864",
        "PRAGMA wal_autocheckpoint = 1000",
        "PRAGMA auto_vacuum = INCREMENTAL",
        "PRAGMA auto_vacuum_increment = 200",
        "PRAGMA optimization_level = 3",
        "PRAGMA analysis_limit = 1000",
        "PRAGMA cache_spill = 1600",
        "PRAGMA locking_mode = NORMAL",
        "PRAGMA recursive_triggers = 0",
        "PRAGMA foreign_keys = ON",
        "PRAGMA defer_foreign_keys = ON"
    ]

    def __init__(self, filename: str, table: str = 'logs', pragmas: Optional[list[str]] = None) -> None:
        super().__init__()

        self.baseFilename = filename
        self.table = table
        self.pragmas = pragmas

        self._create_table()

    def emit(self, record: LogRecord) -> None:
        conn = connect(self.baseFilename)
        cursor = conn.cursor()

        self._apply_configurations(cursor)

        # Format datetime for better readability
        current_time = datetime.now().isoformat()

        # Convert args to string if they exist
        args_str = dumps(record.args) if hasattr(
            record, 'args') and record.args else None

        # Handle exception text if present
        exc_info = str(record.exc_info).replace(
            "'", '"') if hasattr(record, 'exc_info') else None

        cursor.execute(
            f"""INSERT INTO {self.table}
            (timestamp, name, levelno, levelname, msg, args, module, funcName,
            lineno, exc_info, process, thread, threadName)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                current_time, record.name, record.levelno, record.levelname,
                record.msg, args_str, record.module, record.funcName,
                record.lineno, exc_info, record.process,
                str(record.thread), record.threadName
            )
        )

        conn.commit()
        conn.close()

    def _apply_configurations(self, cursor: Cursor) -> None:
        if self.pragmas is None:
            self.pragmas = self.default_pragmas

        for pragma in self.pragmas:
            cursor.execute(pragma)

    def _create_table(self) -> None:
        conn = connect(self.baseFilename)
        cursor = conn.cursor()

        self._apply_configurations(cursor)

        cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            name TEXT,
            levelno INT,
            levelname TEXT,
            msg TEXT,
            args TEXT,
            module TEXT,
            funcName TEXT,
            lineno INT,
            exc_info TEXT,
            process INT,
            thread TEXT,
            threadName TEXT
            )
            '''
        )

        conn.commit()
        conn.close()

    def close(self) -> None:
        # Clean up resources and ensure connections are closed
        try:
            conn = connect(self.baseFilename)
            conn.execute("PRAGMA optimize")
            conn.close()
        except Exception:
            # Silently handle any errors during cleanup
            pass

        # Call parent's close
        super().close()

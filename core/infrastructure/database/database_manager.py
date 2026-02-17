from .database_connector import DatabaseConnector

class DatabaseManager:
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector

    async def initialize(self):
        if self.connector.dialect == "sqlite":
            await self.connector.executescript("""
                PRAGMA foreign_keys = ON;
                PRAGMA journal_mode = WAL;
                PRAGMA synchronous = NORMAL;
                PRAGMA busy_timeout = 5000;

                CREATE TABLE IF NOT EXISTS users (
                    id              INTEGER PRIMARY KEY,
                    is_bot          INTEGER NOT NULL DEFAULT 0,
                    first_name      TEXT    NOT NULL,
                    last_name       TEXT,
                    username        TEXT    UNIQUE COLLATE NOCASE,
                    language_code   TEXT,
                    is_premium      INTEGER NOT NULL DEFAULT 0,

                    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen       DATETIME DEFAULT CURRENT_TIMESTAMP,

                    full_name       TEXT GENERATED ALWAYS AS (
                        TRIM(first_name || ' ' || COALESCE(last_name, ''))
                    ) STORED
                );

                CREATE INDEX IF NOT EXISTS idx_users_username   ON users(username);
                CREATE INDEX IF NOT EXISTS idx_users_last_seen  ON users(last_seen);
            """)
        
        elif self.connector.dialect == "postgresql":
            await self.connector.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id              BIGINT PRIMARY KEY,
                    is_bot          BOOLEAN NOT NULL DEFAULT FALSE,
                    first_name      TEXT NOT NULL,
                    last_name       TEXT,
                    username        TEXT UNIQUE,
                    language_code   TEXT,
                    is_premium      BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    last_seen       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    full_name       TEXT GENERATED ALWAYS AS (
                        TRIM(first_name || ' ' || COALESCE(last_name, ''))
                    ) STORED
                );
            """)
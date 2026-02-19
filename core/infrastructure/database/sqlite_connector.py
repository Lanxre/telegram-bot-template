from typing import Any, Mapping

import aiosqlite


class SQLiteConnector:
    def __init__(self, db_path: str = "bot.db"):
        self.db_path = db_path
        self._conn: aiosqlite.Connection | None = None

    @property
    def dialect(self) -> str:
        return "sqlite"

    async def _ensure_conn(self) -> aiosqlite.Connection:
        if self._conn is None:
            self._conn = await aiosqlite.connect(self.db_path)
            self._conn.row_factory = aiosqlite.Row
        return self._conn

    async def execute(
        self, query: str, params: Mapping[str, Any] | None = None
    ) -> None:
        conn = await self._ensure_conn()
        await conn.execute(query, params or {})
        await conn.commit()

    async def executescript(self, script: str) -> None:
        conn = await self._ensure_conn()
        await conn.executescript(script)
        await conn.commit()

    async def fetch_one(
        self, query: str, params: Mapping[str, Any] | None = None
    ) -> Mapping[str, Any] | None:
        conn = await self._ensure_conn()
        async with conn.execute(query, params or {}) as cursor:
            return await cursor.fetchone()

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()

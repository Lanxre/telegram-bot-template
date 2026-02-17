import asyncpg
import re
from typing import Any, Mapping, Sequence

class PostgresConnector:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.dsn)
        return self._pool

    def _convert_query(self, query: str, params: Mapping[str, Any] | None) -> tuple[str, list[Any]]:
        if not params:
            return query, []
            
        keys = list(params.keys())
        for i, key in enumerate(keys, 1):
            query = query.replace(f":{key}", f"${i}")
        return query, [params[k] for k in keys]

    async def execute(self, query: str, params: Mapping[str, Any] | None = None) -> None:
        pool = await self._get_pool()
        q, p = self._convert_query(query, params)
        await pool.execute(q, *p)

    async def fetch_one(self, query: str, params: Mapping[str, Any] | None = None) -> Mapping[str, Any] | None:
        pool = await self._get_pool()
        q, p = self._convert_query(query, params)
        return await pool.fetchrow(q, *p)

    async def fetch_all(self, query: str, params: Mapping[str, Any] | None = None) -> Sequence[Mapping[str, Any]]:
        pool = await self._get_pool()
        q, p = self._convert_query(query, params)
        return await pool.fetch(q, *p)

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
from multiprocessing import Pool
from aiogram import Dispatcher

from config import DatabaseSettings
from handlers import __routers__
from core.infrastructure.database import DatabaseManager, SQLiteConnector, PostgresConnector
from middleware import ServiceMiddleware

async def setup_connector(database_settings: DatabaseSettings):
    match database_settings.driver:
        case "aiosqlite":
            sqlite_connector = SQLiteConnector(database_settings.name)
            db_manager = DatabaseManager(sqlite_connector)
            await db_manager.initialize()
            return sqlite_connector, db_manager
        case "postgresql":
            postgres_connector = PostgresConnector(database_settings.postgresql_url)
            db_manager = DatabaseManager(postgres_connector)
            await db_manager.initialize()
            return postgres_connector, db_manager
        case _:
            raise ValueError(f"Unsupported database driver: {database_settings.driver}")
        

async def create_dispatcher(database_settings: DatabaseSettings) -> Dispatcher:
    dispatcher = Dispatcher()
    
    connector, db_manager = await setup_connector(database_settings)
    dispatcher.update.middleware(ServiceMiddleware(connector))
    
    dispatcher["db_manager"] = db_manager
    __routers__.register_routes(dispatcher)
    return dispatcher
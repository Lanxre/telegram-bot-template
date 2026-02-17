from aiogram import Dispatcher

from handlers import __routers__
from core.infrastructure.database import DatabaseManager, SQLiteConnector
from middleware import ServiceMiddleware

async def create_dispatcher(database_name: str) -> Dispatcher:
    dispatcher = Dispatcher()
    
    connector = SQLiteConnector(database_name)
    
    db_manager = DatabaseManager(connector)
    await db_manager.initialize()
    
    dispatcher.update.middleware(ServiceMiddleware(connector))

    __routers__.register_routes(dispatcher)
    return dispatcher
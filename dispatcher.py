from aiogram import Dispatcher

from handlers import __routers__
# from core.infrastructure import admin_config, db_manager
# from middleware import AdminMiddleware, ServiceMiddleware


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    
    # dispatcher.update.middleware(ServiceMiddleware(db_manager, admin_config))
    # dispatcher.update.middleware(AdminMiddleware(admin_config))

    # dispatcher["is_admin"] = get_is_admin

    __routers__.register_routes(dispatcher)
    return dispatcher
from .handle_router import HandleRouters

from .start import base_router

__routers__ = HandleRouters(
    routers=(
        base_router,
    )
)
__all__ = ("routers",)

from .start import router as start_router
from .sell_asic import router as sell_asic_router
from .ecosystem_poolproof import router as ecosystem_poolproof_router
from .faq import router as faq_router

routers = [
    start_router,
    sell_asic_router,
    ecosystem_poolproof_router,
    faq_router,
]

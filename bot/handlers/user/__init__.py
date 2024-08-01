__all__ = ("routers",)

from .ecosystem_poolproof import router as ecosystem_poolproof_router
from .dont_publish_post import router as dont_publish_post_router
from .publish_post import router as publish_post_router
from .sell_asic import router as sell_asic_router
from .correct import router as correct_router
from .start import router as start_router
from .next import router as next_router
from .faq import router as faq_router

routers = [
    ecosystem_poolproof_router,
    dont_publish_post_router,
    publish_post_router,
    sell_asic_router,
    correct_router,
    start_router,
    next_router,
    faq_router,
]

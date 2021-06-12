from fastapi import APIRouter

from app.api.routes import couriers, orders, reports, web


router = APIRouter()
router.include_router(couriers.router, tags=["couriers"], prefix="/couriers")
router.include_router(orders.router, tags=["orders"], prefix="/orders")
router.include_router(reports.router)
router.include_router(web.router, tags=["web"], prefix="/web")

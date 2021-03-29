from fastapi import APIRouter

from app.api.routes import couriers, orders


router = APIRouter()
router.include_router(couriers.router, tags=["couriers"], prefix="/couriers")
router.include_router(orders.router, tags=["orders"], prefix="/orders")

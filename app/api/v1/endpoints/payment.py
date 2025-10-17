from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.api.v1 import deps
from app.services import paypal_service
from pydantic import BaseModel

router = APIRouter()

class CreateOrderRequest(BaseModel):
    amount: str = "9.99"
    currency: str = "USD"
    description: str = "SNEH AI Pro Subscription"

class CreateOrderResponse(BaseModel):
    order_id: str
    approval_link: str

class CaptureOrderResponse(BaseModel):
    status: str
    payment_id: str
    state: str

@router.post("/paypal/create-order", response_model=CreateOrderResponse)
def create_paypal_order(
    request: CreateOrderRequest,
    current_user = Depends(deps.get_current_user)
):
    """
    Create a PayPal order and get an approval link.
    """
    try:
        order_details = paypal_service.create_payment_order(
            amount=request.amount,
            currency=request.currency,
            description=request.description
        )
        return order_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paypal/capture-order", response_model=CaptureOrderResponse)
def capture_paypal_order(
    paymentId: str = Query(...),
    PayerID: str = Query(...),
    current_user = Depends(deps.get_current_user)
):
    """
    Capture the payment after the user approves it on PayPal.
    NOTE: PayPal redirects to this endpoint with 'paymentId' and 'PayerID' as query parameters.
    """
    try:
        capture_details = paypal_service.capture_payment(
            payment_id=paymentId,
            payer_id=PayerID
        )
        return capture_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
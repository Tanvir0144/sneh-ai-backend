import paypalrestsdk
from app.core.config import settings

# Configure the PayPal SDK
try:
    if settings.PAYPAL_CLIENT_ID and settings.PAYPAL_CLIENT_SECRET:
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # "sandbox" or "live"
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
except Exception as e:
    print(f"Error configuring PayPal SDK: {e}")

def create_payment_order(amount: str, currency: str, description: str) -> dict:
    """
    Creates a PayPal payment order and returns the approval link.
    """
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": description,
                    "sku": "SNEH-PRO-01",
                    "price": amount,
                    "currency": currency,
                    "quantity": 1
                }]
            },
            "amount": {
                "total": amount,
                "currency": currency
            },
            "description": f"Payment for {description}"
        }],
        # --- THIS IS THE UPDATED SECTION ---
        "redirect_urls": {
            # This URL is called by PayPal after the user approves the payment.
            # It now uses the dynamic BASE_URL from your .env file.
            "return_url": f"{settings.BASE_URL}/api/v1/payment/paypal/capture-order",
            
            # This URL is called if the user cancels the payment.
            # Ideally, this should be a page on your Flutter frontend.
            "cancel_url": f"{settings.BASE_URL}/payment-cancelled"
        }
        # --- END OF UPDATE ---
    })

    if payment.create():
        # Find the approval link
        for link in payment.links:
            if link.rel == "approval_url":
                return {"order_id": payment.id, "approval_link": str(link.href)}
        raise Exception("Approval URL not found in PayPal response.")
    else:
        raise Exception(f"PayPal payment creation failed: {payment.error}")

def capture_payment(payment_id: str, payer_id: str) -> dict:
    """
    Executes (captures) the payment after user approval.
    """
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # In a real application, you would now update the user's subscription
        # plan in your database from 'Free' to 'Pro'
        print(f"Payment {payment.id} executed successfully.")
        return {"status": "success", "payment_id": payment.id, "state": payment.state}
    else:
        raise Exception(f"PayPal payment capture failed: {payment.error}")
import datetime
from sqlalchemy.orm import Session
from app.db import models
from app.db.models.user import SubscriptionPlan

# Daily image generation limits based on subscription plan
IMAGE_LIMITS = {
    SubscriptionPlan.FREE: 3,
    SubscriptionPlan.PRO: 7,
    SubscriptionPlan.PLUS: 1_000_000  # Essentially unlimited
}

def get_or_create_usage(db: Session, user: models.User) -> models.Usage:
    """
    Get the user's usage record for today.
    If the last record is from a previous day, it resets the counters.
    If no record exists, it creates a new one.
    """
    today = datetime.date.today()
    usage = db.query(models.Usage).filter(models.Usage.user_id == user.id).first()

    if not usage:
        # Create new usage record if it doesn't exist
        usage = models.Usage(user_id=user.id, last_reset_date=today)
        db.add(usage)
        db.commit()
        db.refresh(usage)
    elif usage.last_reset_date < today:
        # Reset counters if the last usage was from a previous day
        usage.chat_count = 0
        usage.image_count = 0
        usage.last_reset_date = today
        db.commit()
        db.refresh(usage)
        
    return usage

def check_image_limit(user: models.User, usage: models.Usage) -> bool:
    """Checks if the user is within their daily image generation limit."""
    limit = IMAGE_LIMITS.get(user.subscription_plan, 0)
    return usage.image_count < limit

def reset_all_daily_usage(db: Session):
    """
    Resets the daily chat and image counts for ALL users to zero.
    This function is designed to be run by a daily scheduler.
    """
    try:
        # Update all rows in the usage table
        num_rows_updated = db.query(models.Usage).update({
            models.Usage.chat_count: 0,
            models.Usage.image_count: 0
        })
        db.commit()
        print(f"SCHEDULER: Successfully reset daily usage for {num_rows_updated} users.")
    except Exception as e:
        db.rollback()
        print(f"SCHEDULER ERROR: Failed to reset daily usage. Error: {e}")
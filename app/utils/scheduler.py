from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.services.usage_service import reset_all_daily_usage
import pytz

# It's good practice to use a specific timezone, e.g., UTC for servers
utc_tz = pytz.utc

# Create a scheduler instance
scheduler = BackgroundScheduler(timezone=utc_tz)

def scheduled_reset_job():
    """
    The job function that the scheduler will execute.
    It creates its own database session.
    """
    print("SCHEDULER: Running scheduled daily usage reset job...")
    db = SessionLocal()
    try:
        reset_all_daily_usage(db)
    finally:
        db.close()
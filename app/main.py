import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.base import Base
from app.db.session import engine
from app.api.v1.router import api_router
from app.utils.scheduler import scheduler, scheduled_reset_job

# This function will create all database tables on startup
def create_tables():
    Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(title="SNEH AI Backend")


# --- THIS IS THE UPDATED SECTION FOR DEPLOYMENT ---

# 1. Create a directory for static files if it doesn't exist
# This will store our generated images and audio files.
if not os.path.exists("static"):
    os.makedirs("static")

# 2. Mount the static directory to serve images and audio
# This makes files inside the 'static' folder accessible via URLs like /static/filename.png
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. CORS (Cross-Origin Resource Sharing) Middleware
# In production, you MUST restrict this to your actual frontend domain for security.
# For example: origins = ["https://my-sneh-ai-app.com", "https://www.my-sneh-ai-app.com"]
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use the origins variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- END OF UPDATE ---


# Event handler for application startup
@app.on_event("startup")
def on_startup():
    print("Application starting up...")
    create_tables()
    print("Database tables created (if they did not exist).")
    
    # Add the daily reset job to the scheduler to run every day at 00:01 UTC
    scheduler.add_job(scheduled_reset_job, 'cron', hour=0, minute=1)
    
    # Start the scheduler
    scheduler.start()
    print("Scheduler started. Daily usage reset job is scheduled.")

# Event handler for application shutdown
@app.on_event("shutdown")
def on_shutdown():
    print("Application shutting down...")
    scheduler.shutdown()
    print("Scheduler shut down.")

# Include the main API router
app.include_router(api_router, prefix="/api")

# Root endpoint for health check
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to SNEH AI Backend!"}
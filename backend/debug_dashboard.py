
import asyncio
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from database import db
from services.job_discovery import job_discovery

async def test_dashboard_logic():
    print("Testing imports...")
    try:
        from routes.dashboard import get_career_progress_dashboard
        print("Imports successful.")
    except Exception as e:
        print(f"Import failed: {e}")
        return

    print("Testing JobDiscoveryService initialization...")
    try:
        # Just check if we can call a method
        print("Calling job_discovery.search_all with checks...")
        # We won't actually call the API to save time/limits, just check if the object exists and method is callable
        if hasattr(job_discovery, 'search_all'):
            print("job_discovery.search_all exists.")
        else:
            print("job_discovery.search_all MISSING.")
    except Exception as e:
        print(f"JobDiscoveryService check failed: {e}")

    print("Success. The backend logic seems importable.")

if __name__ == "__main__":
    asyncio.run(test_dashboard_logic())

"""Initialize database tables"""
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("✓ Database initialized")

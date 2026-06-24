"""Seed development data

This script will populate the database with sample data for development.
Run this after migrations are applied.

Usage:
    python scripts/seed_data.py
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))


def main():
    """Main seed function"""
    print("🌱 Seeding database with sample data...")
    print("This is a placeholder. Implementation coming in Sprint 1.")


if __name__ == "__main__":
    main()

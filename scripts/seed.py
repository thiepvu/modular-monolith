#!/usr/bin/env python3
"""
Database seeding script.
Populates database with initial/test data.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.connection import db
from src.infrastructure.seeds.seed_runner import SeedRunner, seed_users


async def seed_all():
    """Run all seed functions"""
    print("🌱 Starting database seeding...")
    
    # Initialize database
    db.initialize()
    
    # Create seed runner
    runner = SeedRunner()
    
    # Register all seeders
    runner.register_seeder(seed_users)
    # Add more seeders here as you create them:
    # runner.register_seeder(seed_files)
    # runner.register_seeder(seed_projects)
    
    # Run all seeders
    await runner.run_all()
    
    # Close database
    await db.close()
    
    print("✅ Database seeding completed!")


async def seed_module(module_name: str):
    """Seed specific module"""
    print(f"🌱 Seeding {module_name} module...")
    
    db.initialize()
    
    seeder_map = {
        "users": seed_users,
        # Add more module seeders here
    }
    
    if module_name not in seeder_map:
        print(f"❌ Unknown module: {module_name}")
        print(f"Available modules: {', '.join(seeder_map.keys())}")
        sys.exit(1)
    
    runner = SeedRunner()
    runner.register_seeder(seeder_map[module_name])
    
    await runner.run_all()
    await db.close()
    
    print(f"✅ {module_name} module seeded!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Database seeding utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Seed all modules
  python scripts/seed.py
  
  # Seed specific module
  python scripts/seed.py --module users
  
  # Force reseed (clear existing data)
  python scripts/seed.py --force
        """
    )
    
    parser.add_argument(
        "--module",
        type=str,
        help="Seed specific module only"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reseed (clear existing data)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.module:
            asyncio.run(seed_module(args.module))
        else:
            asyncio.run(seed_all())
    except KeyboardInterrupt:
        print("\n⚠️  Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
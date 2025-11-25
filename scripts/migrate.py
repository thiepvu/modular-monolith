#!/usr/bin/env python3
"""
Database migration management script.
Wrapper around Alembic for easier usage.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from alembic import command
from alembic.config import Config


def get_alembic_config() -> Config:
    """Get Alembic configuration"""
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    return alembic_cfg


def create_migration(message: str) -> None:
    """Create a new migration"""
    print(f"Creating migration: {message}")
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, message=message, autogenerate=True)
    print(f"✅ Migration created: {message}")


def upgrade_migrations(revision: str = "head") -> None:
    """Apply migrations"""
    print(f"Upgrading database to: {revision}")
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, revision)
    print(f"✅ Database upgraded to: {revision}")


def downgrade_migrations(revision: str = "-1") -> None:
    """Rollback migrations"""
    print(f"Downgrading database to: {revision}")
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)
    print(f"✅ Database downgraded to: {revision}")


def show_current_revision() -> None:
    """Show current database revision"""
    alembic_cfg = get_alembic_config()
    command.current(alembic_cfg)


def show_migration_history() -> None:
    """Show migration history"""
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Database migration management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new migration
  python scripts/migrate.py --create "Add users table"
  
  # Apply all pending migrations
  python scripts/migrate.py --upgrade
  
  # Rollback last migration
  python scripts/migrate.py --downgrade -1
  
  # Show current revision
  python scripts/migrate.py --current
  
  # Show migration history
  python scripts/migrate.py --history
        """
    )
    
    parser.add_argument(
        "--create",
        type=str,
        metavar="MESSAGE",
        help="Create a new migration with the given message"
    )
    parser.add_argument(
        "--upgrade",
        nargs="?",
        const="head",
        metavar="REVISION",
        help="Apply migrations (default: head)"
    )
    parser.add_argument(
        "--downgrade",
        type=str,
        metavar="REVISION",
        help="Rollback migrations (e.g., -1, base, or specific revision)"
    )
    parser.add_argument(
        "--current",
        action="store_true",
        help="Show current database revision"
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show migration history"
    )
    
    args = parser.parse_args()
    
    try:
        if args.create:
            create_migration(args.create)
        elif args.upgrade is not None:
            upgrade_migrations(args.upgrade)
        elif args.downgrade:
            downgrade_migrations(args.downgrade)
        elif args.current:
            show_current_revision()
        elif args.history:
            show_migration_history()
        else:
            parser.print_help()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

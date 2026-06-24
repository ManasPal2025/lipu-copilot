# Database Migrations Guide

Guide to managing database migrations with Alembic.

## Overview

We use Alembic for database schema versioning and migrations.

## Creating a Migration

### Auto-generate Migration

```bash
cd apps/api

# Auto-generate based on model changes
alembic revision --autogenerate -m "Add user table"
```

This will:
1. Compare current models with database schema
2. Generate a new migration file in `migrations/versions/`
3. Show the detected changes

### Manual Migration

```bash
# Create empty migration
alembic revision -m "Custom operation"
```

Then edit the generated file in `migrations/versions/`

## Running Migrations

```bash
cd apps/api

# Upgrade to latest
alembic upgrade head

# Upgrade to specific version
alembic upgrade <revision_id>

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show history
alembic history
```

## Viewing Migration Status

```bash
# Detailed history
alembic history --rev-range <start>:<end>

# Current version and branches
alembic branches
```

## Best Practices

1. **Always test migrations locally before committing**
2. **Write descriptive messages** - Use clear names for migration files
3. **Review generated migrations** - Auto-generated migrations may need manual review
4. **Keep migrations small** - One logical change per migration
5. **Test rollbacks** - Ensure downgrade scripts work correctly
6. **Document complex changes** - Add comments in migration files

## Example: Adding a Column

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(20)))

def downgrade() -> None:
    op.drop_column('users', 'phone')
```

## Troubleshooting

### Migration fails

1. Check database connection
2. Review migration code for syntax errors
3. Verify all dependencies are installed
4. Check database logs for errors

### Can't downgrade

- Ensure downgrade() function is implemented
- Check for data loss issues (e.g., dropping columns)
- Manually inspect database state

### Conflicts with multiple developers

1. Pull latest changes
2. Resolve merge conflicts in version files
3. Test migrations locally
4. Coordinate with team on branch merges

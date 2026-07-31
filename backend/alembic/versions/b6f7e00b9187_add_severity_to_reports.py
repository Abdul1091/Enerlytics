"""add severity to reports

Revision ID: <generated_id>
Revises: 0e430c95a282
Create Date: 2026-07-25
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b6f7e00b9187'
down_revision: Union[str, Sequence[str], None] = '0e430c95a282'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Define enum matching your existing non-native enum pattern
    severity_enum = sa.Enum(
        'LOW',
        'MEDIUM',
        'HIGH',
        'CRITICAL',
        name='severity_level',
        native_enum=False,
    )

    # 2. Add column with server_default to safely handle existing rows
    op.add_column(
        'reports',
        sa.Column(
            'severity',
            severity_enum,
            nullable=False,
            server_default='LOW',
        ),
    )

    # 3. Add index on severity for fast GROUP BY aggregation queries
    op.create_index(
        'ix_reports_severity',
        'reports',
        ['severity'],
    )


def downgrade() -> None:
    op.drop_index('ix_reports_severity', table_name='reports')
    op.drop_column('reports', 'severity')
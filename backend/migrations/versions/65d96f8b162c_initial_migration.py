from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.enums import RequestStatus, Role

# revision identifiers, used by Alembic.
revision = '65d96f8b162c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the "users" table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('user', 'admin', name='role'), nullable=False, server_default='user'),
    )

    # Create the "tags" table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
    )

    # Create the "confirmations" table
    op.create_table(
        'confirmations',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('issue_type', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    )

    # Create the "confirmation_tag" table (association table)
    op.create_table(
        'confirmation_tag',
        sa.Column('confirmation_id', sa.Integer(), sa.ForeignKey('confirmations.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )

    # Create the "steps" table
    op.create_table(
        'steps',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('confirmation_id', sa.Integer(), sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False),
    )


def downgrade():
    # Drop the "steps" table
    op.drop_table('steps')

    # Drop the "confirmation_tag" table
    op.drop_table('confirmation_tag')

    # Drop the "confirmations" table
    op.drop_table('confirmations')

    # Drop the "tags" table
    op.drop_table('tags')

    # Drop the "users" table
    op.drop_table('users')
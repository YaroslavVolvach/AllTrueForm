from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.enums import RequestStatus, Role

# revision identifiers, used by Alembic.
revision = '65d96f8b162c'  # Use the current revision ID
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create the "users" table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum(Role), nullable=False, default=Role.user),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the "tags" table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the "support_requests" table
    op.create_table(
        'support_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('issue_type', sa.String(), nullable=False),
        sa.Column('status', sa.Enum(RequestStatus), nullable=False, default=RequestStatus.pending),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the "support_request_tags" association table
    op.create_table(
        'support_request_tags',
        sa.Column('support_request_id', sa.Integer(), sa.ForeignKey('support_requests.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    )

def downgrade():
    # Drop the "support_request_tags" table
    op.drop_table('support_request_tags')

    # Drop the "support_requests" table
    op.drop_table('support_requests')

    # Drop the "tags" table
    op.drop_table('tags')

    # Drop the "users" table
    op.drop_table('users')
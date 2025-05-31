<%!
import re
from alembic import util
%>
"""${message}

Revision ID: ${up_revision}
Revises: ${', '.join(down_revision) or None}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}


def upgrade():
${upgrades if upgrades else "    pass"}


def downgrade():
${downgrades if downgrades else "    pass"}

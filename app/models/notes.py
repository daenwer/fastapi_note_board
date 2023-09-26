from app.models.database import metadata
from sqlalchemy import Table, Column, Integer, Text, DateTime, func


notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", Text, nullable=False),
    Column(
        "created_at", DateTime, server_default=func.current_timestamp(),
        nullable=False
    ),
    Column(
        "updated_at", DateTime, server_default=func.current_timestamp(),
        nullable=False
    ),
    Column("view_count", Integer, server_default="0", nullable=False),
)

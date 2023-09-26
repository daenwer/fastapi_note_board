from app.models.database import metadata
from sqlalchemy import Table, Column, ForeignKey


note_boards = Table(
    "note_boards",
    metadata,
    Column("note_id", ForeignKey("notes.id")),
    Column("board_id", ForeignKey("boards.id")),
)

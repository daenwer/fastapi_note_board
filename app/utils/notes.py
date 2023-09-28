from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.sql import update

from app.models.database import database
from app.models.note_boards import note_boards
from app.models.notes import notes
from app.schemas import notes as note_schemas


async def get_notes(
    skip: int = 0, limit: int = 100, note_ids: Optional[List[int]] = None
):
    if note_ids is None:
        query = notes.select().offset(skip).limit(limit)
    else:
        query = (
            notes.select()
            .offset(skip)
            .limit(limit)
            .where(notes.c.id.in_(note_ids))
        )
    result = await database.fetch_all(query)
    return result


async def get_note(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


async def update_note(notes_id: int, new_data: dict, updated=False):
    if updated:
        new_data["updated_at"] = func.current_timestamp()
    query = update(notes).where(notes.c.id == notes_id).values(**new_data)
    await database.execute(query)


async def create_note(note: note_schemas.BaseNote):
    db_note = notes.insert().values(content=note.content)
    note_id = await database.execute(db_note)
    return {"id": note_id}


async def delete_note(note_id: int):
    query_note_boards = note_boards.delete().where(
        note_boards.c.note_id == note_id
    )
    query_note = notes.delete().where(notes.c.id == note_id)
    async with database.transaction():
        await database.execute(query_note_boards)
        await database.execute(query_note)

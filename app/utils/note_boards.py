from app.models.database import database
from app.models.note_boards import note_boards
from app.utils import boards as board_utils


async def get_note_board(board_id: int, note_id: int):
    query = note_boards.select().where(
        note_boards.c.board_id == board_id
    ).where(note_boards.c.note_id == note_id)
    result = await database.fetch_one(query)
    return result


async def add_note(board_id: int, note_id: int):
    query = note_boards.insert().values(board_id=board_id, note_id=note_id)
    await database.execute(query)
    await board_utils.update_updated_at(board_id)


async def remove_note(board_id: int, note_id: int):
    query = note_boards.delete().where(
        note_boards.c.board_id == board_id
    ).where(note_boards.c.note_id == note_id)
    await database.execute(query)
    await board_utils.update_updated_at(board_id)

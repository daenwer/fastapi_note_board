from typing import List

from app.utils import boards as board_utils
from app.utils import notes as note_utils
from app.utils import note_boards as note_board_utils
from app.schemas import boards as board_schemas
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post(
    "/boards/", response_model=board_schemas.CreatedBoard, status_code=201
)
async def create_note(board: board_schemas.BaseBoard):
    return await board_utils.create_board(board)


@router.get("/boards/", response_model=List[board_schemas.Board])
async def get_boards(skip: int = 0, limit: int = 100):
    return await board_utils.get_boards(skip=skip, limit=limit)


@router.get("/boards/{board_id}", response_model=board_schemas.BoardNotes)
async def get_board(board_id: int):
    db_board = await board_utils.get_board(board_id, True)
    if not db_board:
        raise HTTPException(status_code=400, detail="Board not created")
    return db_board


@router.delete("/boards/{board_id}", status_code=204)
async def delete_board(board_id: int):
    if not await board_utils.get_board(board_id):
        raise HTTPException(status_code=400, detail="Note not created")
    await board_utils.delete_board(board_id)


@router.put(
    "/boards/{board_id}/{new_name}", status_code=204
)
async def update_note_name(board_id: int, new_name: str):
    if not await board_utils.get_board(board_id):
        raise HTTPException(status_code=400, detail="Note not created")
    await board_utils.update_name(board_id, {"name": new_name})


@router.put(
    "/boards_add_note/{board_id}/{note_id}", status_code=204
)
async def add_note(board_id: int, note_id: int):
    if not await board_utils.get_board(board_id):
        raise HTTPException(status_code=400, detail="Board not created")
    if not await note_utils.get_note(note_id):
        raise HTTPException(status_code=400, detail="Note not created")
    if await note_board_utils.get_note_board(board_id, note_id):
        raise HTTPException(status_code=400, detail="Note already added")
    await note_board_utils.add_note(board_id, note_id)


@router.put(
    "/boards_remove_note/{board_id}/{note_id}", status_code=204
)
async def remove_note(board_id: int, note_id: int):
    if not await note_board_utils.get_note_board(board_id, note_id):
        raise HTTPException(
            status_code=400, detail="There is no such note on the board"
        )
    await note_board_utils.remove_note(board_id, note_id)

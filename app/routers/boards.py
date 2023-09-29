from typing import List

from fastapi import APIRouter

from app.schemas.boards import CreatedBoard, BaseBoard, Board, BoardNotes
from app.utils import boards as board_utils
from app.utils import note_boards as note_board_utils

router = APIRouter()


@router.post("/boards/", response_model=CreatedBoard, status_code=201)
async def create_board(board: BaseBoard):
    return await board_utils.create_board(board)


@router.get("/boards/", response_model=List[Board])
async def get_boards(skip: int = 0, limit: int = 100):
    return await board_utils.get_boards(skip=skip, limit=limit)


@router.get("/boards/{board_id}", response_model=BoardNotes)
async def get_board(board_id: int):
    return await board_utils.get_board(board_id, True)


@router.delete("/boards/{board_id}", status_code=204)
async def delete_board(board_id: int):
    await board_utils.delete_board(board_id)


@router.put("/boards/{board_id}/{new_name}", status_code=204)
async def update_note_name(board_id: int, new_name: str):
    await board_utils.update_name(board_id, {"name": new_name})


@router.put("/boards_add_note/{board_id}/{note_id}", status_code=204)
async def add_note(board_id: int, note_id: int):
    await note_board_utils.add_note(board_id, note_id)


@router.put("/boards_remove_note/{board_id}/{note_id}", status_code=204)
async def remove_note(board_id: int, note_id: int):
    await note_board_utils.remove_note(board_id, note_id)

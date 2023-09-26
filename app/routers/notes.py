from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas import notes as note_schemas
from app.utils import boards as board_utils
from app.utils import notes as note_utils

router = APIRouter()


@router.post(
    "/notes/", response_model=note_schemas.CreatedNote, status_code=201
)
async def create_note(note: note_schemas.BaseNote):
    return await note_utils.create_note(note)


@router.get("/notes/", response_model=List[note_schemas.Note])
async def get_notes(skip: int = 0, limit: int = 100):
    return await note_utils.get_notes(skip=skip, limit=limit)


@router.get("/notes/{note_id}", response_model=note_schemas.Note)
async def get_note(note_id: int):
    db_note = await note_utils.get_note(note_id)
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not created")
    view_count = db_note._mapping["view_count"] + 1
    await note_utils.update_note(note_id, {"view_count": view_count})
    return db_note


@router.get(
    "/notes_form_board/{board_id}", response_model=List[note_schemas.Note]
)
async def get_note_from_board(board_id: int, skip: int = 0, limit: int = 100):
    db_board = await board_utils.get_board(board_id, True)
    if not db_board:
        raise HTTPException(status_code=400, detail="Board not created")
    return await note_utils.get_notes(
        note_ids=db_board.get("notes_id"), skip=skip, limit=limit
    )


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int):
    if not await note_utils.get_note(note_id):
        raise HTTPException(status_code=400, detail="Note not created")
    await note_utils.delete_note(note_id)


@router.put("/notes/{note_id}/{content}", response_model=note_schemas.Note)
async def update_note(note_id: int, content: str):
    if not await note_utils.get_note(note_id):
        raise HTTPException(status_code=400, detail="Note not created")
    await note_utils.update_note(note_id, {"content": content}, True)
    return await note_utils.get_note(note_id)

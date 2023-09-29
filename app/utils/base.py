from fastapi import HTTPException


def check_skip_limit(skip, limit):
    if skip < 0 or limit < 1 or skip >= limit:
        raise HTTPException(status_code=400, detail="Incorrect skip or limit")

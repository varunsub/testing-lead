from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from app.core.security import authenticate_user, create_access_token
from app.schemas import users as schema_users
from fastapi import Form

from app.db.database import get_db

router = APIRouter()


@router.post("/token", response_model=schema_users.Token)
async def login_for_access_token(
    username: str = Form(...), password: str = Form(...), db=Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    response = JSONResponse(content={"auth_success": True})
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )
    return response

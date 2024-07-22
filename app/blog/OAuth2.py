from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from blog import token_1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(tokenData: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_1.verify_token(tokenData, credentials_exception)

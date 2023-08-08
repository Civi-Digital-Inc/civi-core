"""
## Description
Routes dependencies
## Usage
```python3
from civi_core import deps

@app.get('/example/')
def example(
    db: Session = Depends(deps.get_db),
    current_identity: deps.TokenData = Depends(deps.get_current_identity),
    ...
```
"""
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from google.cloud.sql.connector import Connector
import os

from .config import settings

connector = Connector()

def getconn():
    conn = connector.connect(
        "charming-shield-389823:us-central1:civi",
        "pg8000",
        user="postgres",
        password=os.getenv("PW"),
        db=os.getenv("DB_NAME"),
    )
    return conn

__engine = create_engine("postgresql+pg8000://", creator=getconn)
__SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=__engine)


def get_db() -> Generator:
    """
    Returns a sqlachemy database session.
    """
    db = __SessionLocal()
    try:
        yield db
    finally:
        db.close()


__oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)


class TokenData(BaseModel):
    """
    Identity data
    """

    id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[List[str]] = None
    token: Optional[str] = None


__credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"Authorizaiton": ""},
)


async def get_current_identity(
    db: Session = Depends(get_db), token: str = Depends(__oauth2_scheme)
) -> TokenData:
    """
    Returns the current logged in identity.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        identity_id: int = payload.get('id', '')
        email: str = payload.get('email', '')
        role: List[str] = literal_eval(payload.get('role', '[]'))
        if identity_id is None or email is None:
            raise __credentials_exception
        token_data = TokenData(id=identity_id, email=email, token=token, role=role)
    except JWTError:
        raise __credentials_exception
    return token_data

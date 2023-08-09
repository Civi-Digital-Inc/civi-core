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
import os
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.cloud.sql.connector import Connector
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from .choices import EnvType, IdentityRole
from .config import settings

connector = Connector()


def __env_based_engine():
    if settings.ENV == EnvType.LOCAL:
        return create_engine(settings.SQLALCHEMY_DATABASE_URI)

    return create_engine(
        'postgresql+pg8000://',
        creator=lambda: connector.connect(
            'charming-shield-389823:us-central1:civi',
            'pg8000',
            user='postgres',
            password=os.getenv('PW'),
            db=os.getenv('DB_NAME'),
        ),
    )


__engine = __env_based_engine()
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
    tokenUrl=f'{settings.API_V1_STR}/login'
)


class TokenData(BaseModel):
    """
    Identity data
    """

    id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[IdentityRole] = None
    token: Optional[str] = None


__credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'Authorizaiton': ''},
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
            options={'verify_aud': False},
        )
        identity_id: int = payload.get('id', '')
        email: str = payload.get('email', '')
        role: IdentityRole = IdentityRole(
            payload.get('role', IdentityRole.DEFAULT.value)
        )
        if identity_id is None or email is None:
            raise __credentials_exception
        token_data = TokenData(
            id=identity_id, email=email, token=token, role=role
        )
    except JWTError:
        raise __credentials_exception
    except ValueError:
        raise __credentials_exception
    return token_data

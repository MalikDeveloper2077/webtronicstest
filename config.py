import os

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer


access_security = JwtAccessBearer(secret_key="SECRET", auto_error=True)
refresh_security = JwtRefreshBearer(secret_key="SECRET", auto_error=True)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/kali')

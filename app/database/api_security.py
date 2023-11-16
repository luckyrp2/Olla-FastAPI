from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="Olla-API-Key")
api_keys = ["my_api_key"]

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
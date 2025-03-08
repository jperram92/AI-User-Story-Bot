from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import hashlib
import os

api_key_header = APIKeyHeader(name="X-API-Key")

class AuthService:
    def __init__(self):
        # Generate a random API key at startup
        self.api_key = hashlib.sha256(os.urandom(32)).hexdigest()[:32]
    
    async def verify_api_key(self, api_key: str = Security(api_key_header)):
        if api_key != self.api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        return api_key
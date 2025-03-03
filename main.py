from fastapi import FastAPI, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict
import logging
import os
from pydantic import BaseModel

from database import get_session, init_models
from models import TokenModel
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI(title="Authorization Service")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class AuthResponse(BaseModel):
    authorized: bool
    user_id: Optional[str] = None
    message: Optional[str] = None

@app.post("/auth", response_model=AuthResponse)
async def validate_token(
    authorization: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session)
):
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Invalid authorization header format")
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    # Extract token from header
    token = authorization.replace("Bearer ", "")
    
    try:
        # Query the database for the token
        result = await session.get(TokenModel, token)
        
        if result:
            logger.info(f"Token validated successfully for user: {result.user_id}")
            return AuthResponse(
                authorized=True,
                user_id=result.user_id,
                message="Token is valid"
            )
        else:
            logger.warning(f"Invalid token: {token[:10]}...")
            raise HTTPException(
                status_code=403, 
                detail="Token is invalid"
            )
    
    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
        raise HTTPException(status_code=403, detail=f"Error validating token: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database models")
    await init_models()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
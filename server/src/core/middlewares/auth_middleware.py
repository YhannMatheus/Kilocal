from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.core.auth.token import AccessToken
from src.types.models.user import User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):

    PUBLIC_PATHS = [
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/user/login",
        "/api/v1/user/register",
        "/health"
    ]

    async def dispatch(self, request:Request, call_next):
        if any(request.url.path.startswith(path) for path in self.PUBLIC_PATHS):
            response = await call_next(request)
            return response
        
        try:
            token = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]

            if not token:
                token = request.cookies.get("access_token")

            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required. Provide token via Authorization header or Cookie.",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            user_data = AccessToken.decode(token)
            user = await User.get(id=user_data.user_id)

            request.state.user = user
            request.state.user_id = user.id

            logger.info(f"Authenticated request from user_id: {user.id} at {datetime.utcnow().isoformat()} for path: {request.url.path}")

            response = await call_next(request)
            return response
        
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail,
                    "timestamp": datetime.utcnow().isoformat()
                    },
                headers=e.headers if hasattr(e, 'headers') else {}
            )
        
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error during authentication.",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
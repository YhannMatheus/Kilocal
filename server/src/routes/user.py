from fastapi import APIRouter, Depends, HTTPException, status, Header
from src.services.user_services import UserService
from src.types.schemas.auth import *
from src.types.schemas.user import *
from src.services.session_services import SessionService
from src.core.auth.token import AccessToken
from src.types.models.user import User

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login", response_model=Token)
async def login(data: LoginRequest) -> Token:
    try:
        access_token = await UserService.get_user(data)
                
        token_data = AccessToken.decode(access_token)
        
        session = await SessionService.create_session(user_id=str(token_data.user_id), remember=data.remember)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user session",
            )
        
        return Token(access_token=access_token)

    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"\n{'='*80}\nLOGIN ERROR:\n{error_detail}\n{'='*80}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. Error: {str(e)}",
        )

@router.post("/register", response_model=Token)
async def register(data: RegisterRequest) -> Token:
    try:
        access_token = await UserService.create_user(data)
        token_data = AccessToken.decode(access_token)
        session = await SessionService.create_session(user_id=str(token_data.user_id), remember=True)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user session",
            )
        
        return Token(access_token=access_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"\n{'='*80}\nREGISTRATION ERROR:\n{error_detail}\n{'='*80}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. Error: {str(e)}",
        )

@router.get("/profile", response_model=UserProfile)
async def profile(authorization:str = Header(...)) -> UserProfile:
    token = AccessToken.decode(authorization)
    try:
        user_id = token.user_id
        profile = await UserService.get_user_profile(str(user_id))
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"\n{'='*80}\nPROFILE ERROR:\n{error_detail}\n{'='*80}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. Error: {str(e)}",
        )
    
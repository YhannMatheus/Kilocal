from src.services.body_assessment_service import BodyAssessmentService
from src.types.schemas.auth import LoginRequest, RegisterRequest
from src.types.schemas.workout import WorkoutRead
from src.types.schemas.user import *
from src.types.models.workout import Workout
from src.core.auth.security import Authenticate
from src.core.auth.token import AccessToken
from fastapi import HTTPException, status
from src.types.models.user import User
from src.core.validator.validator import Validator
import asyncio

class UserService:
    @staticmethod
    async def create_user(data: RegisterRequest):
        if await User.exists(email=data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )
        if not Validator.is_valid_email(data.email) or not Validator.is_strong_password(data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or weak password"
            )

        hashed_password = Authenticate.hash_password(data.password)

        user = await User.create(
            name=data.name,
            email=(data.email).lower(),
            hashed_password=hashed_password,
            gender=data.gender,
            birth_date=data.birth_date,
            height_cm=data.height_cm,
        )

        return AccessToken.generate(str(user.id), user.role.value, remember=True)
    
    @staticmethod
    async def login(data: LoginRequest) -> str:
        user = await User.get_or_none(email=(data.email).lower())
        
        invalid_auth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not user or not Authenticate.verify_password(data.password, user.hashed_password):
            raise invalid_auth_exception

        return AccessToken.generate(str(user.id), user.role.value, data.remember)

    @staticmethod
    async def get_by_id(user_id: str) -> User:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    async def get_user_profile(user_id: str) -> UserProfile:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        workouts_query = Workout.filter(user_id=user.id).prefetch_related("sets__exercise")
        
        workouts, body_history = await asyncio.gather(
            workouts_query.all(),
            BodyAssessmentService.get_body_assessment_graphs(str(user.id))
        )
        
        workout_list = [WorkoutRead.model_validate(w) for w in workouts]
        
        return UserProfile(
            userData=UserRead.model_validate(user), # Ajuste aqui também se necessário
            workouts=workout_list,
            body_graphs=body_history
        )
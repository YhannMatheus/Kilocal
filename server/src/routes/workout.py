from fastapi import APIRouter, HTTPException, status, Header
from src.services.workout_service import WorkoutService
from src.types.schemas.workout import *
from src.core.auth.token import AccessToken
from uuid import UUID

router = APIRouter(prefix="/workout", tags=["Workout"])

@router.post("/")
async def create_workout(data : WorkoutCreate, authorization:str = Header(...)):
    token = AccessToken.decode(authorization)
    try:
        if str(token.user_id) != str(data.userid):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to create a workout for this user"
            )
        data.userid = UUID(str(data.userid))
        await WorkoutService.create_workout(data)
    except HTTPException  as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating workout: {str(e)}"
        )
    return {"message":"Workout created successfully", "workout_id": str(data.userid)}

@router.get("/{userid}")
async def get_workouts(userid:UUID, authorization:str = Header(...)) -> list[WorkoutRead]:
    token = AccessToken.decode(authorization)
    try:
        if str(token.user_id) != str(userid):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access workouts for this user"
            )
        workouts = await WorkoutService.get_all_user_workouts(str(userid))
    except HTTPException  as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving workouts: {str(e)}"
        )
    return workouts

@router.get("/detail/{workoutid}")
async def get_workout_detail(workoutid:UUID, authorization:str = Header(...)) -> WorkoutDetailed:
    token = AccessToken.decode(authorization)
    try:
        workout = await WorkoutService.get_workout_by_id(str(workoutid))
        if str(token.user_id) != str(workout.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this workout"
            )
    except HTTPException  as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving workout detail: {str(e)}"
        )
    return workout

@router.put("/{workoutid}")
async def update_workout(workoutid:UUID, data:WorkoutUpdate, authorization:str = Header(...)) -> WorkoutDetailed:
    token = AccessToken.decode(authorization)
    try:
        workout = await WorkoutService.get_workout_by_id(str(workoutid))
        if str(token.user_id) != str(workout.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this workout"
            )
        await WorkoutService.update_workout(str(workoutid), data)
    except HTTPException  as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating workout: {str(e)}"
        )
    return workout

@router.get("/days/{userid}")
async def get_workout_days(userid:UUID, authorization:str = Header(...)):
    token = AccessToken.decode(authorization)
    try:
        if str(token.user_id) != str(userid):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access workout days for this user"
            )
        workout_days = await WorkoutService.get_all_workout_day(str(userid))
    except HTTPException  as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving workout days: {str(e)}"
        )
    return workout_days
from tortoise import Model, fields
from src.types.enums.user import GenderEnum, ActivityLevelEnum, RoleEnum

class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    hashed_password = fields.CharField(max_length=255)
    birth_date = fields.DateField()
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)

    height_cm = fields.FloatField(null=True,default=0.0)
    goal = fields.FloatField(null=True)

    gender = fields.CharEnumField(GenderEnum)
    activity_level = fields.CharEnumField(ActivityLevelEnum, null=True, default=ActivityLevelEnum.SEDENTARY)
    
    activates_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"
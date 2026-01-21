from tortoise import fields, Model
from src.types.enums.exercise import MuscleGroupEnum

class Exercise(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100, index=True)
    target_muscle = fields.CharEnumField(MuscleGroupEnum, default=MuscleGroupEnum.CHEST)
    instructions = fields.TextField(null=True)
    
    is_system_default = fields.BooleanField(default=False)
    created_by = fields.ForeignKeyField("models.User", related_name="custom_exercises", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "exercises"
        ordering = ["name"]
        unique_together = (("name", "created_by"),("name", "is_system_default"))

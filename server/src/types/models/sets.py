from tortoise import Model, fields

class Set(Model):
    id = fields.UUIDField(pk=True)
    workout = fields.ForeignKeyField("models.Workout", related_name="sets", on_delete=fields.CASCADE)
    exercise = fields.ForeignKeyField("models.Exercise", related_name="sets", on_delete=fields.CASCADE)
    
    reps = fields.IntField(null=True)
    weight = fields.FloatField(null=True)  # in kg
    duration = fields.IntField(null=True)  # in seconds
    distance = fields.FloatField(null=True)  # in meters
    calories_burned = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "sets"
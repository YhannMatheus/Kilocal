from tortoise import fields, Model


class CaloricIntake(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="caloric_intakes", on_delete=fields.CASCADE)
    
    name = fields.CharField(max_length=100, description="Nome da refeição (ex: Almoço, Whey)")
    date = fields.DateField(auto_now_add=True) # Data do registro (normalmente hoje)
    
    # Macronutrientes
    protein_grams = fields.FloatField(default=0.0)
    carbs_grams = fields.FloatField(default=0.0)
    fats_grams = fields.FloatField(default=0.0)
    
    # Total calórico (pode ser calculado ou inserido manualmente)
    calories_consumed = fields.FloatField(default=0.0)
    
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "caloric_intakes"
        ordering = ["-created_at"]
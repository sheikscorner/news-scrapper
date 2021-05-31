from tortoise import fields
from tortoise import models
from tortoise.contrib.pydantic import pydantic_model_creator

class User(models.Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)


    class PydanticMeta:
        pass

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

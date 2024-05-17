from pydantic import BaseModel, EmailStr, SecretStr


class UpdateUser(BaseModel):
    username: str
    nickname: str


class BaseUser(UpdateUser):
    email: EmailStr


class RegisterUser(BaseUser):
    password: SecretStr


class CreatedUser(BaseUser):
    class Config:
        from_attributes = True

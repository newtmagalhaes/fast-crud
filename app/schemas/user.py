from pydantic import BaseModel, EmailStr, SecretStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str
    nickname: str | None


class RegisterUser(BaseUser):
    password: SecretStr


class CreatedUser(BaseUser):
    class Config:
        from_attributes = True

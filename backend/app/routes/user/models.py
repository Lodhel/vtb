from pydantic import BaseModel, Field
from fastapi import Query


class UserModel(BaseModel):
    password: str = Field(..., description="Пароль пользователя")
    phone_number: str = Field(..., description="Номер телефона пользователя")
    vtb_auth: str = Field(None, description="ВТБ идентификатор для аутентификации")


class UserActivateModel(BaseModel):
    sms_code: str = Field(..., description="Код подтверждения, полученный по СМС")


class UserDataModel(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    lastname: str = Field(..., description="Фамилия пользователя")
    phone_number: str = Field(..., description="Номер телефона пользователя")
    email: str = Field(None, description="Электронная почта пользователя")
    vtb_auth: str = Field(None, description="ВТБ идентификатор для аутентификации")


class UserGETModel(BaseModel):
    password: str = Field(..., description="Пароль пользователя")
    phone_number: str = Field(..., description="Номер телефона пользователя")


class UserQuestionnaireModel(BaseModel):
    info: str = Field(..., description="Информация, указанная пользователем в анкете")


class UserQuestionnaireParams:
    def __init__(
        self,
        user_id: int = Query(..., description="Идентификатор пользователя, к которому привязана анкета")
    ):
        self.user_id = user_id


class UserResponse(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    name: str = Field(..., description="Имя пользователя")
    lastname: str = Field(..., description="Фамилия пользователя")
    phone_number: str = Field(..., description="Номер телефона пользователя")
    email: str = Field(..., description="Электронная почта пользователя")
    vtb_auth: str = Field(..., description="ВТБ идентификатор для аутентификации")
    token_auth: str = Field(..., description="Токен для авторизации пользователя")


class UserCreateResponse(BaseModel):
    code: str = Field(..., description="Код подтверждения создания пользователя")
    token_auth: str = Field(..., description="Токен для авторизации нового пользователя")

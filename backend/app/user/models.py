from pydantic import BaseModel
from fastapi import Query, UploadFile


class UserModel(BaseModel):
    password: str = Query(..., description="пароль")
    phone_number: str = Query(..., description="номер телефона")
    vtb_auth: str = Query(default=None, description="втб идентификатор")


class UserActivateModel(BaseModel):
    sms_code: str = Query(..., description="смс код")


class UserDataModel(BaseModel):
    name: str = Query(..., description="имя пользователя")
    lastname: str = Query(..., description="фамилия пользователя")
    phone_number: str = Query(..., description="номер телефона")
    email: str = Query(default=None, description="эмайл")
    vtb_auth: str = Query(default=None, description="втб идентификатор")


class UserGETModel(BaseModel):
    password: str = Query(..., description="пароль")
    phone_number: str = Query(..., description="номер телефона")


class UserQuestionnaireModel(BaseModel):
    info: str = Query(..., description="информация в анкете")


class UserQuestionnaireParams:
    def __init__(
        self,
        user_id: int = Query(..., description="идентификатор пользователя анкеты")
    ):
        self.user_id = user_id

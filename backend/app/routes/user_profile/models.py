from pydantic import BaseModel


class UserProfileRequest(BaseModel):
    income_last_month: float
    expenses_last_month: float
    savings_last_month: float
    marital_status: bool
    children_count: int
    education: str
    occupation: str


class UserProfileResponse(BaseModel):
    user_id: int
    income_last_month: float
    expenses_last_month: float
    savings_last_month: float
    marital_status: bool
    children_count: int
    education: str
    occupation: str

    class Config:
        orm_mode = True

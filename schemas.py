from pydantic import BaseModel


class X_Schema(BaseModel):
    username: str
    days: int = 120

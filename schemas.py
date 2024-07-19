from pydantic import BaseModel


class UnameDay_Schema(BaseModel):
    username: str
    days: int = 120

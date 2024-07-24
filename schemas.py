from typing import Optional, List

from pydantic import BaseModel, EmailStr, constr


class CrawlerSchema(BaseModel):

    username: str
    days: int = 120


class UserSchema(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    mobile_number: constr(min_length=11, max_length=11)  # Ensures exactly 11 digits
    address: constr(min_length=1, max_length=200)
    fb_username: Optional[str] = None
    insta_username: Optional[str] = None
    x_username: Optional[str] = None
    hashtags: List[str]

    def as_dict(self) -> dict:
        return self.dict()

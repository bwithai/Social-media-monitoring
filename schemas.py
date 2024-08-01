from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr


class CrawlerSchema(BaseModel):
    username: str
    days: int = 120


class UserSchema(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    mobile_number: constr(min_length=11, max_length=12)  # Ensures exactly 11 digits
    address: constr(min_length=1, max_length=200)
    fb_username: Optional[str] = None
    insta_username: Optional[str] = None
    x_username: Optional[str] = None
    num_fb_posts: Optional[int] = 0
    num_insta_posts: Optional[int] = 0
    num_x_days: Optional[int] = 0

    def as_dict(self) -> dict:
        user_dict = self.dict()
        user_dict["crawler"] = {
            "X": [],
            "Instagram": [],
            "facebook": []
        }
        return user_dict


class GraphSchema(BaseModel):
    tweets_id: Optional[str] = None
    fb_posts_id: Optional[str] = None

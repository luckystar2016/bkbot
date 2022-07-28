from typing import Optional

from pydantic import BaseModel

from .user_profile import UserProfile


class Desc(BaseModel):
    type: int
    timestamp: int
    view: int
    orig_dy_id: Optional[int]
    orig_type: int
    user_profile: UserProfile
    dynamic_id: int
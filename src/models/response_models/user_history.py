from datetime import datetime

from pydantic import BaseModel


class UserHistoryResponseModel(BaseModel):
    created_at: datetime
    action: str

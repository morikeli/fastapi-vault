from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class TrackModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    artist: str
    duration: str
    last_play: datetime

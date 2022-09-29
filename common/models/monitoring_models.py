import datetime
from typing import Optional

from pydantic import BaseModel, Field

import config


class JobData(BaseModel):
    old_received_bytes: int = Field(default=0)
    old_upload_bytes: int = Field(default=0)

    current_received_bytes: int = Field(default=0)
    current_upload_bytes: int = Field(default=0)

    update_interval: int = Field(default=config.DEFAULT_UPDATE_INTERVAL)

    message_id: Optional[int] = Field()

    start_date: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())
    last_update: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

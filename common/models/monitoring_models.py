from pydantic import BaseModel, Field

import config


class JobData(BaseModel):
    old_received_bytes: int = Field(default=0)
    old_upload_bytes: int = Field(default=0)
    update_interval: int = Field(default=config.DEFAULT_UPDATE_INTERVAL)

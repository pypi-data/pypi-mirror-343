from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class JobOrdersListPayloadWithAccount(BaseModel):
    accountId: UUID
    recent: Optional[bool] = None

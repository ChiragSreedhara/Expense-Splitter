from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    user_id: int
    amount: float
    description: Optional[str] = None

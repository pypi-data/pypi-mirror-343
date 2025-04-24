from pydantic import BaseModel


class APIResponse(BaseModel):
    data: str

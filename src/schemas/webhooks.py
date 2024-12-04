from pydantic import BaseModel


class DestinationDTO(BaseModel):
    id: str
    name: str
    url: str
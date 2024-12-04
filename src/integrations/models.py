from enum import Enum
from pydantic import BaseModel, Field
from typing import Any

from aiohttp import ClientSession


class HTTPMethod(Enum):
    POST = 'POST'
    GET = 'GET'
    DELETE = 'DELETE'
    PATCH = 'PATCH'

    async def call(self, session: ClientSession, url: str, **kwargs):
        method_map = {
            'POST': session.post,
            'GET': session.get,
            'DELETE': session.delete,
            'PATCH': session.patch,
        }
        method = method_map[self.value]
        return await method(url=url, **kwargs)

class Request(BaseModel):
    method: HTTPMethod
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    params: dict[str, str] = Field(default_factory=dict)
    json_payload: dict[str, Any] = Field(default_factory=dict)
    data: str | None = None

class ResponseWithRequest(BaseModel):
    request: Request
    data: dict
    status: int
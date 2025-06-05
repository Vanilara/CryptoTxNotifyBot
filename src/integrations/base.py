import asyncio
from itertools import batched

from aiohttp import ClientSession, ClientResponse

from utils.logger_setter import Loggable
from integrations.models import HTTPMethod, ResponseWithRequest, Request
from core.networks import Network
from core.config import settings


class BaseRequestSender(Loggable):
    def __init__(
            self, base_url: str, base_headers: dict[str, str] | None = None
        ):
        super().__init__('request_sender')
        self.base_url = base_url
        self.base_headers = {'accept': 'application/json'} | (base_headers or {})

    async def _send_request(self, 
        method: HTTPMethod, 
        extra_url: str = '',
        extra_headers: dict[str, str] | None = None, 
        **kwargs
    ) -> ClientResponse:
        if extra_headers is None:
            extra_headers = {}
        headers=self.base_headers | extra_headers
        url = self.base_url + extra_url

        debug_info = {**kwargs, 'headers': headers}
        self.logger.debug(f"Sending {method.value} to {url}. With {debug_info}")
        async with ClientSession() as session:
            response = await method.call(
                session,
                headers = headers,
                url = url,
                **kwargs
            )
        if response.headers['Content-Type'] == 'application/json':
            self.logger.debug(f'Got {response.status} from {url}. {await response.json()}')
        else:
            self.logger.debug(f'Got {response.status} from {url}. {await response.text()}')
        return response
    
    async def _send_batched_group_requests(
        self, request: Request, session: ClientSession
    ) -> ResponseWithRequest:
        self.logger.debug(f"Sending {request}")
        response = await request.method.call(
            session,
            **request.model_dump(exclude={"method", "json_payload"})
        )
        self.logger.debug(f'Got {response.status} from {request.url}. {await response.text()}')
        data = await response.json()
        return ResponseWithRequest(
            data = data, status = response.status, request = request
        )
        
    async def _send_group_requests(
        self, requests: list[Request], limit: int | None = None, delay: int = 1
    ) -> list[ResponseWithRequest]:
        responses = []
        requests_groups = [requests]
        if limit is not None:
            requests_groups = batched(requests, limit)
        async with ClientSession() as session:
            for index, requests_group in enumerate(requests_groups):
                if index != 0:
                    await asyncio.sleep(delay)
                tasks = [
                    self._send_batched_group_requests(
                        request = request, session = session
                    ) for request in requests_group
                ]
                responses += await asyncio.gather(*tasks)
        return responses
    
    def _make_endpoint_url(self, network: Network) -> str:
        endpoint_url = settings.integrations.QUICKNODE_ENDPOINT_URL
        return endpoint_url.replace('.{chain}', network.endpoint_quicknode_path)


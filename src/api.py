import aiohttp
from aiohttp.client_exceptions import ClientError

from src import configs

HEADERS = {'x-token': configs.CRM_API_TOKEN, 'x-token-type': 'telegram'}


async def crm_request(method: str, url: str, data: dict) -> tuple[bool, dict]:
    """
    Make a request to the CRM API
    :method: GET, POST, PUT, DELETE
    :url: API endpoint
    :data: JSON data
    """
    session = aiohttp.ClientSession(base_url=configs.CRM_API_URL, headers=HEADERS)
    if method == 'GET':
        request_data = {'method': method, 'url': url, 'params': data}
    else:
        request_data = {'method': method, 'url': url, 'json': data}

    try:
        async with session.request(**request_data) as response:
            resp_data = await response.json()
            if response.status not in (200, 201):
                return False, resp_data

            return True, resp_data
    except ClientError as e:
        if configs.DEBUG:
            configs.logger.error(f'Error while making a request: {str(e)}')
        return False, {'error': str(e)}
    finally:
        await session.close()


def log_request(is_success: bool, message) -> None:
    """For DEBUG purposes"""
    if is_success:
        configs.logger.success(message)
    else:
        configs.logger.error(message)


class CRMApi:
    CLIENTS_URL = '/api/v1/clients/'
    CONSULTATIONS_URL = '/api/v1/consultations/'
    EVENTS_URL = '/api/v1/events/'

    async def _make_request(self, method: str, url: str, data: dict, entity: str) -> tuple[bool, dict]:
        is_success, resp = await crm_request(method, url, data)

        if configs.DEBUG:
            message = f'{entity}, {url=}, {data=}, {resp=}'
            log_request(is_success, message)

        return is_success, resp

    async def create_client(self, data: dict) -> tuple[bool, dict]:
        """
        Create a new client in the CRM
        Success if a client with phone_number and tg_id does not exist
        :data:
        {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123456789",
            "telegram_data": {
                "tg_id": 123456789,
                "username": "tg-username",
                "language_code": "en"
            }
        """
        return await self._make_request('POST', self.CLIENTS_URL, data, 'Create client')

    async def create_consultation(self, data: dict) -> tuple[bool, dict]:
        """
        Create a new consultation in the CRM
        :data: {"client_note": "Some client text", "client": 1, "room_name": "bedroom", "area": 20}
        ""room_name" and "area" are optional
        """
        return await self._make_request('POST', self.CONSULTATIONS_URL, data, 'Create consultation')

    async def get_client_by_tg_id(self, tg_id: int) -> dict:
        """Get a client by tg_id"""
        query_params = {'tg_id': tg_id}
        is_success, resp = await crm_request('GET', self.CLIENTS_URL, data=query_params)
        if configs.DEBUG:
            message = f'Get user by tg id, url={self.CLIENTS_URL}, {query_params=}, {resp=}'
            log_request(is_success, message)

        count, results = resp.get('count', 0), resp.get('results', [])

        if count >= 1:
            results = results[0]
        else:
            results = {}

        return results


# to use one instance of the class
API = CRMApi()

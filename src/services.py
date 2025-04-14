from src.api import API


async def get_user_by_tg_id(tg_id: int) -> dict:
    return await API.get_client_by_tg_id(tg_id)

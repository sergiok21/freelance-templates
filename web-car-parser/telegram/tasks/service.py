import logging

from shared.utils.request import Sender, Request

logger = logging.getLogger(__name__)


async def update_web_data_task(headers: dict, t_id: str, token: str):
    status = Sender.send_data_to_service(
        method=Request().post, headers=headers,
        t_id=t_id, token=token,
        is_superuser=False
    )
    if status == 400:
        patch_status = Sender.send_data_to_service(
            method=Request().patch, headers=headers, t_id=t_id, token=token
        )
        if patch_status != 204:
            raise Exception(f'Web data was not updated. Status: {status}')
    else:
        raise Exception(f'Web data was not updated. Status: {status}')
    logger.info(f'Update web data task was completed')


async def delete_web_data_task(headers: dict, t_id: int):
    status = Sender.send_data_to_service(method=Request.delete, headers=headers, t_id=t_id)
    if status != 204:
        raise Exception(f'User web data {t_id} was not deleted. Status: {status}')
    logger.info(f'Delete web data task was completed')


async def delete_parser_data_task(url: str, headers: dict, user_status: dict):
    status = Sender.send_data_to_service(method=Request.post, url=url, headers=headers, user_status=user_status)
    if status != 204:
        raise Exception(f'User parser threads was not deleted. Status: {status}')
    logger.info(f'Delete parser data task was completed')

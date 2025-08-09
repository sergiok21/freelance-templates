import logging

from shared.database.models import Admin

logger = logging.getLogger(__name__)


async def delete_token_task(t_id, token):
    admin_model = Admin(t_id=t_id)
    tokens = await admin_model.get_tokens()
    if token in tokens:
        await Admin(t_id=t_id).delete_token(token=token)
        logger.info(f'Token {token} was deleted (creator {t_id})')
        return
    logger.info(f'Token {token} could not delete cause token was activated')

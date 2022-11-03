"""
Helper functions and message filters
"""
from modules.config import ADMIN_IDS
from aiogram.types import Message


def is_admin(message: Message) -> bool:
    """
    Message filter that checks user to be a bot admin
    :param message: Telegram message object
    :return: True if user is bot admin, else False
    """
    return message.from_user.id in ADMIN_IDS

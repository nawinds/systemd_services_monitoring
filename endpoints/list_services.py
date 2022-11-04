import logging

from aiogram import types
from check import check

from modules.bot import dp
from modules.helper import is_admin
from modules.data.db_session import create_session
from modules.data.services import Service
from endpoints.systemd_commands import start_service


@dp.message_handler(is_admin, commands=["help", "start"])
async def help(message: types.Message):
    if len(message.text.split()) > 1:
        await start_service(message)
    else:
        HELP_TEXT = "test"
        await message.answer(HELP_TEXT)


@dp.message_handler(is_admin, commands=["all"])
async def all_service(message: types.Message):
    session = create_session()
    all_services = session.query(Service).all()
    res = "Services list:\n\n"
    for s in all_services:
        is_up = check(s.name)
        res += "🟢 UP" if is_up else "🔴 DOWN"
        res += " <code>" + s.name + "</code>\n"
    logging.info("Service list retrieved")
    await message.reply(res)


@dp.message_handler(is_admin, commands=["add"])
async def add_service(message: types.Message):
    try:
        service = message.text.split()[1]
    except IndexError:
        await message.reply("Service name???")
        return
    session = create_session()
    session.add(Service(name=service))
    session.commit()
    logging.info("Service %s added", service)
    await message.reply("Service added")


@dp.message_handler(is_admin, commands=["delete"])
async def delete_service(message: types.Message):
    try:
        service = message.text.split()[1]
    except IndexError:
        await message.reply("Service name?")
        return
    session = create_session()
    session.query(Service).filter(Service.name == service).first().delete()
    session.commit()
    logging.info("Service %s deleted", service)
    await message.reply("Service deleted")

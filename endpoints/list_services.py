import logging

from aiogram import types
from check import check

from modules.bot import dp
from modules.helper import is_admin
from modules.data.db_session import create_session
from modules.data.services import Service
from modules.config import CONTACT_MAIL
from endpoints.systemd_commands import start_service


@dp.message_handler(is_admin, commands=["help", "start"])
async def help(message: types.Message):
    if len(message.text.split()) > 1:
        await start_service(message)
    else:
        HELP_TEXT = "Hi, sysadmin :)\n" \
                    "I'll help you to monitor and manage your systemd services. " \
                    "Below is a list of commands to help you:\n" \
                    "\n" \
                    "SETTINGS:\n" \
                    "/add service_name — adds service_name.service to the monitoring system\n" \
                    "/delete service_name — removes service_name.service from the monitoring system\n" \
                    "\n" \
                    "MONITORING:\n" \
                    "/all — lists up/down statuses of all services, added to the monitoring system\n" \
                    "/status service_name — gets output of <code>systemctl status service_name.service</code> " \
                    "command\n" \
                    "/start service_name — starts service_name.service\n" \
                    "/stop service_name — stops service_name.service\n" \
                    "/restart service_name — restarts service_name.service\n" \
                    "\n" \
                    "LOGS:\n" \
                    "/logs service_name — sends a log file of service_name.service from journalctl " \
                    "(last 15 min events only)\n" \
                    "\n" \
                    f"<i>Feel free to email me at <a href=\"mailto:{CONTACT_MAIL}\">{CONTACT_MAIL}</a> " \
                    "if you have any questions</i>\n" \
                    "To get this message again send /help"
        await message.answer(HELP_TEXT)


@dp.message_handler(is_admin, commands=["settings"])
async def settings(message: types.Message):
    SETTINGS_HELP_TEXT = "SETTINGS:\n" \
                         "/add service_name — adds service_name.service to the monitoring system\n" \
                         "/delete service_name — removes service_name.service from the monitoring system\n" \
                         "\n" \
                         "To get full commands list, send /help"
    await message.answer(SETTINGS_HELP_TEXT)


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
    to_delete = session.query(Service).filter(Service.name == service).first()
    session.delete(to_delete)
    session.commit()
    logging.info("Service %s deleted", service)
    await message.reply("Service deleted")

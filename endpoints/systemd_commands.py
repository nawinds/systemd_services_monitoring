import logging

from aiogram import types
import subprocess
from check import send_logs

from modules.bot import dp
from modules.helper import is_admin
from os import system


@dp.message_handler(is_admin, commands=["restart"])
async def restart_service(message: types.Message):
    try:
        service = message.text.split()[1]
    except IndexError:
        await message.reply("Service name?")
        return
    result = subprocess.run(["sudo", "systemctl", "restart", service])
    return_code = str(result.returncode)
    if return_code == "0":
        logging.info("Service %s RESTARTED", service)
        await message.reply("Service successfully restarted!")
    else:
        logging.warning("FAILED to restart %s service", service)
        await message.reply("Failed to restart service!")


@dp.message_handler(is_admin, commands=["stop"])
async def stop_service(message: types.Message):
    try:
        service = message.text.split()[1]
    except IndexError:
        await message.reply("Service name?")
        return
    result = subprocess.run(["sudo", "systemctl", "stop", service])
    return_code = str(result.returncode)
    if return_code == "0":
        with open("temp/alerted.txt", encoding="utf-8") as f:
            alerted = f.read().split("\n")
        with open("temp/alerted.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(alerted) + f"\n{service}")

        logging.info("Service %s STOPPED", service)
        await message.reply("Service successfully stopped!")
    else:
        logging.warning("FAILED to stop %s service", service)
        await message.reply("Failed to stop service!")


async def start_service(message: types.Message):
    service = message.text.split()[1]
    result = subprocess.run(["sudo", "systemctl", "start", service])
    return_code = str(result.returncode)
    if return_code == "0":
        logging.info("Service %s STARTED", service)
        await message.reply("Service successfully started!")
    else:
        logging.warning("FAILED to start %s service", service)
        await message.reply("Failed to start service!")


@dp.message_handler(is_admin, commands=["status"])
async def status_service(message: types.Message):
    try:
        service = message.text.split()[1]
    except IndexError:
        await message.reply("Service name?")
        return
    system(f"sudo systemctl status {service} > temp/status.txt")

    logging.info("%s service STATUS requested", service)
    with open("temp/status.txt", encoding="utf-8") as f:
        data = f.read()
    await message.reply(f"{service} status command response:\n<code>{data}</code>")


@dp.message_handler(is_admin, commands=["logs"])
async def logs_service(message: types.Message):
    try:
        service = message.text.split()[1]
    except IndexError:
        await message.reply("Service name?")
        return
    await send_logs(service)

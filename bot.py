import asyncio
import logging

from aiogram import executor

from modules.bot import dp
from modules.config import AIOGRAM_LOGS_PATH, DB_PATH
from modules.data.db_session import global_init, create_session
from modules.data.services import Service
import endpoints

if __name__ == '__main__':
    global_init(DB_PATH)
    logging.basicConfig(level=logging.INFO, filename=AIOGRAM_LOGS_PATH,
                        format='%(levelname)s %(asctime)s - '
                               '%(name)s (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    logging.info("Starting...")
    session = create_session()
    existing_monitoring_service = session.query(Service)\
        .filter(Service.name == "monitoring").first()
    if not existing_monitoring_service:
        session.add(Service(name="monitoring"))
        session.commit()
        logging.info("Service %s added", "monitoring")
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)

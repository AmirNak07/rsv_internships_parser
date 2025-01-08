import asyncio
import time

import httpx
import schedule
from loguru import logger

from config import (
    API_PARAM,
    INTERNSHIPS_API_URL,
    INTERNSHIPS_PAGE_URL,
    LOGS_CONFIG,
    OFFSET_PARAM,
    PAGE_PARAM,
    SHEET_NAME,
    SPREADSHEET_ID,
)
from utils.google_sheets_helper import authorize_google_sheets, write_to_google_sheet
from utils.internship_parser import (
    get_all_internship_links,
    get_internship_count,
    parse_internship_card,
)

logger.remove()
logger.configure(**LOGS_CONFIG)


@logger.catch
async def main():
    logger.info("Start parsing Internships")
    try:
        # Шаг 1: Получение количества стажировок
        internship_count = await get_internship_count(INTERNSHIPS_PAGE_URL, PAGE_PARAM)
        logger.debug(f"Total internships: {internship_count}")

        # Шаг 2: Получение всех карточек на стажировки
        internship_links = await get_all_internship_links(INTERNSHIPS_API_URL, API_PARAM, internship_count, OFFSET_PARAM)
        logger.debug(f"Found {len(internship_links)} internship links")

        # Шаг 3: Асинхронный парсинг каждой карточки стажировки
        async with httpx.AsyncClient() as client:
            tasks = [parse_internship_card(client, link) for link in internship_links]
            internships_data = await asyncio.gather(*tasks)

        internships_data = [item for sublist in internships_data for item in sublist]

        # Шаг 4: Авторизация и отправка данных в Google Таблицу
        service = authorize_google_sheets()
        write_to_google_sheet(service, SPREADSHEET_ID, SHEET_NAME, internships_data)
        logger.debug("Data sent to Google Sheets")
    except httpx.ReadTimeout:
        logger.error("Nothing was found")
    logger.info("End parsing Internships")


def timer():
    asyncio.run(main())


if __name__ == "__main__":
    schedule.every(3).hours.do(timer)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # timer()

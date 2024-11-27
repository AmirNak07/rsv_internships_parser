import asyncio

import httpx

from config import (
    API_PARAM,
    INTERNSHIPS_API_URL,
    INTERNSHIPS_PAGE_URL,
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


async def main():
    # Шаг 1: Получение количества стажировок
    internship_count = await get_internship_count(INTERNSHIPS_PAGE_URL, PAGE_PARAM)
    print(f"Total internships: {internship_count}")

    # Шаг 2: Получение всех карточек на стажировки
    internship_links = await get_all_internship_links(INTERNSHIPS_API_URL, API_PARAM, internship_count, OFFSET_PARAM)
    print(f"Found {len(internship_links)} internship links")

    # Шаг 3: Асинхронный парсинг каждой карточки стажировки
    async with httpx.AsyncClient() as client:
        tasks = [parse_internship_card(client, link) for link in internship_links]
        internships_data = await asyncio.gather(*tasks)

    internships_data = [item for sublist in internships_data for item in sublist]

    # Шаг 4: Авторизация и отправка данных в Google Таблицу
    service = authorize_google_sheets()
    write_to_google_sheet(service, SPREADSHEET_ID, SHEET_NAME, internships_data)

if __name__ == "__main__":
    asyncio.run(main())

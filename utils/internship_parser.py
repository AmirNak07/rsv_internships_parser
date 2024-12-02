import asyncio

from bs4 import BeautifulSoup
from httpx import AsyncClient

from config import REGIONS_API, SKILS_API
from utils.html_helpers import extract_internship_data


async def get_internship_count(url: str, params: dict) -> int:
    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Пример поиска тега с числом стажировок
        internship_count = soup.find('div', class_='list-header__counts-item-number').text

        return int(internship_count)


async def get_all_internship_links(url: str, params: dict, count: int, take: int) -> list:
    links = []
    tasks = [
        create_link(url, params, start)
        for start in range(0, count, take)
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        links.append(result)

    return links


async def create_link(url: str, params: dict, start: int) -> list:
    params["skip"] = start
    params = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{url}/?{params}"
    return url


async def parse_internship_card(client: AsyncClient, url: str) -> list:
    response = await client.get(url)
    if response.status_code != 200:
        response.raise_for_status()
    json_content = response.text

    regions = await get_regions(REGIONS_API)
    skils = await get_skils(SKILS_API)

    return extract_internship_data(json_content, regions, skils)


async def get_regions(url: str) -> list:
    async with AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            response.raise_for_status()
        regions_data = response.json()

    regions = {region["id"]: region["field_value"] for region in regions_data["data"]}
    return regions


async def get_skils(url: str) -> list:
    async with AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            response.raise_for_status()
        skils_data = response.json()

    skils = {skill["id"]: skill["name"] for skill in skils_data["data"]}
    return skils

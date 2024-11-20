import asyncio
from collections import defaultdict
import csv
import re

import aiohttp
from bs4 import BeautifulSoup


CYRILL__UPPER_SET = {chr(i) for i in range(ord("А"), ord("Я") + 1)}
LATIN__UPPER_SET = {chr(i) for i in range(ord("A"), ord("Z") + 1)}


async def get_page(session, url, retries=3, delay=2):
    """
    Асинхронная загрузка страницы с попытками повторения в случае ошибки.
    """
    attempt = 0
    while attempt < retries:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(
                    f"Ошибка загрузки страницы: {response.status}"
                    f"Попытка {attempt + 1} из {retries}."
                )
                attempt += 1
                if attempt < retries:
                    # Пауза перед очередной попыткой
                    await asyncio.sleep(delay)
                else:
                    print(f"Не удалось загрузить страницу после {retries} попыток.")
                    return None
    return None


async def parse_animals_from_page(html, alphabet_counts):
    """
    Парсинг страницы по группам букв, игнорируя латиницу и подкатегории.
    """
    soup = BeautifulSoup(html, "html.parser")

    mw_subcategories_section = soup.find(id="mw-subcategories")
    # Игнорируем подкатегории
    if mw_subcategories_section:
        mw_subcategories_section.decompose()

    # Находим группы букв
    groups = soup.select("div.mw-category-group")
    for group in groups:
        # Извлекаем букву из заголовка
        letter = group.find("h3").text.strip()
        if letter not in CYRILL__UPPER_SET:
            continue

        # Извлекаем ссылки на животных
        animals = group.select("ul li a")
        # Увеличиваем счётчик для буквы
        alphabet_counts[letter] += len(animals)

    # Поиск ссылки на следующую страницу
    next_page = soup.find("a", string="Следующая страница")
    if next_page:
        next_url = next_page["href"]

        # Ищем значение pagefrom
        match = re.search(r"pagefrom=([^#]+)", next_url)
        if match:
            page_from_value = match.group(1)
            # Проверяем если буква в латинском алфавите
            if page_from_value[0] in LATIN__UPPER_SET:
                return None
            # Возвращаем полный URL
            return f"https://ru.wikipedia.org{next_url}"

    return None


def write_to_csv(output_file, alphabet_counts):
    """
    Запись результатов в CSV.
    """
    with open(output_file, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for letter, count in sorted(alphabet_counts.items()):
            writer.writerow([letter, count])


async def count_animals(url, output_file, pause=0.1):
    """
    Асинхронный сбор данных о животных по буквам.
    """
    letters_count = defaultdict(int)
    async with aiohttp.ClientSession() as session:
        while url:
            html = await get_page(session, url)
            if html is None:
                print(f"Не удалось загрузить страницу: {url}. Прекращаем.")
                break
            url = await parse_animals_from_page(html, letters_count)
            await asyncio.sleep(pause)

    write_to_csv(output_file, letters_count)
    print(f"Результаты записаны в {output_file}")


if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    output_file = "beasts.csv"
    asyncio.run(count_animals(url, output_file))

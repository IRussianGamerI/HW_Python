import re
import sys
import argparse
import asyncio
from collections import Counter

import aiohttp
import aiofiles
from bs4 import BeautifulSoup


async def read_url(url, client):
    async with client.get(url) as resp:
        data = await resp.read()
        soup = BeautifulSoup(data, features="html.parser")
        words = re.findall(r"[a-zA-Zа-яёА-ЯЁ_]+", soup.text)
        res_counted = Counter(words).most_common(5)
        res_dict = {url: {item[0]: item[1] for item in res_counted}}
        print(res_dict)


async def parse_urls(client, url_queue, queue_task):
    while True:
        url = await url_queue.get()
        try:
            await read_url(url, client)
        except Exception as message:
            print(f"Ошибка: {message}")
        finally:
            url_queue.task_done()
        if queue_task.done() and url_queue.empty():
            break


async def fill_queue(url_queue, filename):
    """Заполнение очереди из url"""
    async with aiofiles.open(filename, mode="r") as file:
        async for url in file:
            await url_queue.put(url.strip())


async def start_async_parsing(filename: str, num_async_reqs: int, queue_max_size: int):
    """Запуск асинхронного парсинга"""
    url_queue = asyncio.Queue(maxsize=queue_max_size)
    queue_task = asyncio.create_task(fill_queue(url_queue, filename))

    async with aiohttp.ClientSession() as client:
        tasks = [
            asyncio.create_task(parse_urls(client, url_queue, queue_task))
            for _ in range(num_async_reqs)
        ]

        await url_queue.join()
        await queue_task
        await asyncio.wait(tasks)


def create_parser():
    """Функция для настройки запуска скрипта из консоли"""
    arg_conf = argparse.ArgumentParser()
    arg_conf.add_argument("-c", "--async_reqs", default="5")
    arg_conf.add_argument("-f", "--file", default="some_urls.txt")
    return arg_conf


if __name__ == "__main__":
    arg_config = create_parser()
    args = arg_config.parse_args(sys.argv[1:])
    async_reqs = int(args.async_reqs)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        start_async_parsing(
            filename=args.file, num_async_reqs=async_reqs, queue_max_size=2 * async_reqs
        )
    )
    print("Обкачка url'ов завершена")

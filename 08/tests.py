import argparse
import asyncio
import unittest
from unittest.mock import patch

import aiohttp

from fetcher import fill_queue, parse_urls, start_async_parsing, create_parser


async def mock_fill_queue(urls, url_queue):
    for url in urls:
        await url_queue.put(url.strip())


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_fill_queue(self):
        with open("urls.txt", "r", encoding="utf-8") as file:
            expected_urls = map(lambda x: x.strip(), file.readlines())

        url_queue = asyncio.Queue(maxsize=4)
        task = asyncio.create_task(fill_queue(url_queue, "urls.txt"))

        for url in expected_urls:
            self.assertEqual(await url_queue.get(), url)
            url_queue.task_done()
        task.cancel()

    @patch("builtins.print")
    async def test_parse_urls(self, mock_print):
        urls = [
            "https://ru.wikipedia.org",
            "https://en.wikipedia.org",
            "https://pl.wikipedia.org",
            "https://bmstu.ru",
            "https://google.ru",
            "https://www.state.gov",
            "https://instagram.com",
            "https://rkn-zablochil.ru",
        ]
        url_queue = asyncio.Queue(maxsize=len(urls) * 2)
        queue_task = asyncio.create_task(mock_fill_queue(urls, url_queue))

        async with aiohttp.ClientSession() as session:
            await parse_urls(session, url_queue, queue_task)
        res = str(mock_print.call_args_list)
        self.assertEqual(len(mock_print.call_args_list), len(urls))  # Ровно len вызовов
        self.assertTrue(any(url in res for url in urls))  # Что-то удалось распарсить
        self.assertFalse(res.count("Ошибка") >= len(urls))  # Ошибок меньше 100%

    @patch("builtins.print")
    async def test_start_async_parsing(self, mock_print):
        await start_async_parsing("some_urls.txt", 5, 10)
        res = str(mock_print.call_args_list)
        with open("some_urls.txt", "r", encoding="utf-8") as file:
            urls = file.readlines()
            file_len = len(urls)
            self.assertEqual(
                len(mock_print.call_args_list), file_len
            )  # Ровно len вызовов
            self.assertTrue(
                any(url in res for url in urls)
            )  # Что-то удалось распарсить
            self.assertFalse(res.count("Ошибка") >= file_len)  # Ошибок меньше 100%

    def test_arg_parser(self):
        arg_conf = create_parser()
        self.assertTrue(isinstance(arg_conf, argparse.ArgumentParser))
        self.assertEqual(arg_conf.get_default("async_reqs"), "5")
        self.assertEqual(arg_conf.get_default("file"), "some_urls.txt")


if __name__ == "__main__":
    unittest.main()

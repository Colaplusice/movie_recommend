import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup


class AsnycGrab(object):

    def __init__(self, url_list, max_threads):

        self.urls = url_list
        self.results = {}
        self.max_threads = max_threads

    def __parse_results(self, url, html):

        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title').get_text()
            print('title', title)
        except Exception as e:
            raise e

        if title:
            self.results[url] = title

    async def get_body(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                print(response.status)
                assert response.status == 200
                html = await response.read()
                return response.url, html

    async def get_results(self, url):
        url, html = await self.get_body(url)
        self.__parse_results(url, html)
        return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()
            try:
                task_status = await self.get_results(current_url)
            except Exception as e:
                logging.exception('Error for {}'.format(current_url), exc_info=True)

    def eventloop(self):
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.urls]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(task_id, q, ) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__ == '__main__':
    async_example = AsnycGrab(['http://edmundmartin.com',
                               # 'https://www.udemy.com',
                               'https://github.com/',
                               'https://zhangslob.github.io/',
                               'https://www.zhihu.com/'], 5)
    async_example.eventloop()
    print(async_example.results)

# точностью до 5 знаков).
# BMC for task 3
from fileinput import filename
from re import U
import aiohttp
import asyncio
import json
import argparse
import aiofiles
import logging
import os
import re
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Image loader")

arguments_parser = argparse.ArgumentParser(prog="python task2.py", description="Send images to server")
arguments_parser.add_argument('-i', '--image_folder', default='images/cats_and_dogs_filtered/train/cats')
arguments_parser.add_argument('-s', '--server_name', default='localhost')
arguments_parser.add_argument('-w', '--workers', default=4)


# upload image to server
async def upload(file_name: str, url: str, session: aiohttp.ClientSession):
    try:
        async with aiofiles.open(file_name, mode='rb') as f:
            content = await f.read()

        form = aiohttp.FormData()
        form.add_field(file_name, content,
                       content_type='image/jpeg',
                       filename=file_name)

        async with session.post(url, data=form) as resp:
            if resp.status == 201:
                logger.info(f'{file_name} loaded')
                print(await resp.text())
    except Exception as e:
        logger.error(e)


async def worker(url: str, queue: asyncio.Queue):
    # TODO Possible loop not found exception
    async with aiohttp.ClientSession() as session:
        while True:
            image_path = await queue.get()
            await upload(file_name=image_path, url=url, session=session)
            queue.task_done()


async def main():
    arguments = arguments_parser.parse_args()

    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    image_paths = os.listdir(arguments.image_folder)

    # Filter acceptable image formats
    _filter = re.compile("(.*)\\.(jpeg|jpg|gif)$")
    _filtered_paths = [os.path.join(arguments.image_folder, _p) for _p in image_paths if _filter.match(_p)]
    for _file_name in _filtered_paths:
        # TODO check file name with regex expression if it is an known image format
        queue.put_nowait(_file_name)

    # Create three worker tasks to process the queue concurrently.
    url = 'http://localhost:8001/images'

    tasks = []
    for i in range(int(arguments.workers)):
        task = asyncio.create_task(worker(url, queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel tasks when queue is empty
    for task in tasks:
        task.cancel()

    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())

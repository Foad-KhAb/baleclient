import asyncio
from aiobale import Client, Dispatcher
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp)


@dp.message(lambda m: m.content.document)
async def handler(msg: Message):
    doc = msg.content.document
    await client.download_file(doc.file_id, doc.access_hash, destination=doc.name)

    await msg.answer("File saved!")


async def main():
    await client.start()


asyncio.run(main())

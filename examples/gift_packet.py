import asyncio
from aiobale import Client, Dispatcher
from aiobale.enums import ChatType
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp)


@dp.message(lambda m: m.content.gift and m.chat.type == ChatType.PRIVATE)
async def handler(msg: Message):
    await client.open_packet(msg)

    await asyncio.sleep(2)
    await msg.answer("Thanks! That was kind — but let me give it back to you.")
    
    packet = msg.content.gift
    await client.send_giftpacket(
        msg.chat.id,
        msg.chat.type,
        packet.total_amount,
        "Thanks... I really appreciate it though.",
    )


async def main():
    await client.start()


asyncio.run(main())

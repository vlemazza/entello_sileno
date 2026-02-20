import json
import random
import aiofiles

async def load_messages(path="waiting_messages.json"):
    async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
        content = await f.read()
        return json.loads(content)

async def get_waiting_messages():
    messages = await load_messages()

    rand_values = {
        "rand1": random.randint(0, 10),
        "rand2": random.randint(0, 999),
        "rand3": f"{random.randint(0, 59):02d}",
        "rand4": f"{random.randint(0, 59):02d}",
    }

    return [msg.format(**rand_values) for msg in messages]

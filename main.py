from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star
from astrbot.core.message.components import Plain
from httpx import AsyncClient


class StarLighter(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):
        messages = event.get_messages()
        for message in messages:
            if isinstance(message, Plain) and message.text.startswith("/x"):
                async for result in self.x(event):
                    yield result
                return

    async def x(self, event: AstrMessageEvent):
        base_url = self.config["x"]["base_url"]
        timeout = self.config["x"]["timeout"]

        messages = event.get_messages()
        texts = [message.text for message in messages if isinstance(message, Plain)]
        msg = " ".join(texts).removeprefix("/x").lstrip()

        async with AsyncClient(base_url=base_url, timeout=timeout) as client:
            response = await client.post("/", json={"msg": msg})

        yield event.plain_result(response.text)

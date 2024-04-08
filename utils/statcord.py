import asyncio
import contextlib
import aiohttp
import psutil

from disnake import Client as DiscordClient
from typing import Any, Optional, Union, List, Dict, Iterable, Callable, Awaitable
from disnake.ext.commands import Context

class StatcordException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

class RequestFailure(StatcordException):
    def __init__(self, status: int, response: str):
        self.status = status
        self.response = response
        super().__init__("{}: {}".format(status, response))

class TooManyRequests(RequestFailure):
    def __init__(self, status: int, response: str, wait: int):
        self.wait = wait
        super().__init__(status, response)

class Client:
    """Client for using the statcord API"""

    def __init__(self, bot, token, **kwargs):

        if not isinstance(bot, DiscordClient):
            raise TypeError(f"Expected class deriving from disnake.Client for arg bot not {bot.__class__.__qualname__}")
        if not isinstance(token, str):
            raise TypeError(f"Expected str for arg token not {token.__class__.__qualname__}")

        self.bot: DiscordClient = bot
        self.key: str = token
        self.base: str = "https://api.statcord.com/v3/"
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=bot.loop)

        self.custom1: Optional[Callable[[], Awaitable[str]]] = kwargs.get("custom1") or None
        self.custom2: Optional[Callable[[], Awaitable[str]]] = kwargs.get("custom2") or None
        self.active: List[int] = []
        self.commands: int = 0
        self.popular: List[Dict[str, Union[str, int]]] = []
        self.previous_bandwidth: int = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv


    @staticmethod
    def __headers() -> Dict[str, str]:
        return {'Content-Type': 'application/json'}

    def _trace(self) -> Dict[str,Any]:
        return {}

    # noinspection SpellCheckingInspection
    async def __handle_response(self, res: aiohttp.ClientResponse) -> dict:
        try:
            msg = await res.json() or {}
        except aiohttp.ContentTypeError:
            msg = await res.text()
        status = res.status
        if status == 200:
            return msg
        elif status == 429:
            raise TooManyRequests(status, msg, int(msg.get("timeleft") or '600'))
        else:
            raise RequestFailure(status=status, response=msg)

    @property
    def servers(self) -> str:
        return str(len(self.bot.guilds))

    @property
    def _user_counter(self) -> Iterable[int]:
        for g in self.bot.guilds:
            with contextlib.suppress(AttributeError):
                yield g.member_count

    @property
    def users(self) -> str:
        return str(sum(self._user_counter))

    async def post_data(self) -> None:
        bot_id = str(self.bot.user.id)
        commands = str(self.commands)

        mem = psutil.virtual_memory()
        mem_used = str(mem.used)
        mem_load = str(mem.percent)

        cpu_load = str(psutil.cpu_percent())

        current_bandwidth = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        bandwidth = str(current_bandwidth - self.previous_bandwidth)
        self.previous_bandwidth = current_bandwidth

        if self.custom1:
            # who knows why PyCharm gets annoyed there /shrug
            # noinspection PyCallingNonCallable
            custom1 = str(await self.custom1())
        else:
            custom1 = "0"

        if self.custom2:
            # who knows why PyCharm gets annoyed there /shrug
            # noinspection PyCallingNonCallable
            custom2 = str(await self.custom2())
        else:
            custom2 = "0"

        # noinspection SpellCheckingInspection
        data = {
            "id": bot_id,
            "key": self.key,
            "servers": self.servers,
            "users": self.users,
            "commands": commands,
            "active": self.active,
            "popular": self.popular,
            "memactive": mem_used,
            "memload": mem_load,
            "cpuload": cpu_load,
            "bandwidth": bandwidth,
            "custom1": custom1,
            "custom2": custom2,
        }

        data.update(self._trace())

        self.active = []
        self.commands = 0
        self.popular = []

        async with self.session.post(url=self.base + "stats", json=data, headers=self.__headers()) as resp:
            await self.__handle_response(resp)

    def start_loop(self) -> None:
        self.bot.loop.create_task(self.__loop())

    def command_run(self, ctx: Context) -> None:
        self.commands += 1
        if ctx.author.id not in self.active:
            self.active.append(ctx.author.id)

        command = ctx.command.name
        for cmd in filter(lambda x: x["name"] == command, self.popular):
            cmd["count"] = str(int(cmd["count"]) + 1)
            break
        else:
            self.popular.append({"name": command, "count": "1"})

    async def __loop(self) -> None:
        """
        The internal loop used for automatically posting server/guild count stats
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                await self.post_data()
            except Exception as e:
                if isinstance(e,TooManyRequests):
                    await asyncio.sleep(e.wait)
                    continue
                if isinstance(e,RequestFailure):
                    await asyncio.sleep(600)
                    continue
                print(e)
            else:
              await asyncio.sleep(60)
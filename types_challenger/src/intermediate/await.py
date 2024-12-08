"""
TODO:

`run_async` takes an awaitable integer.
"""


from collections.abc import Awaitable


def run_async(func: Awaitable[int]):
    ...


from asyncio import Queue

q: Queue[int] = Queue()
q2: Queue[str] = Queue()


async def afunction() -> int:
    return await q.get()


async def afunction2() -> str:
    return await q2.get()


run_async(afunction())
run_async(1)  # expect-type-error
run_async(afunction2())  # expect-type-error
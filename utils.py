from asyncio import get_event_loop

from bcrypt import hashpw, gensalt


async def hashing(data: str) -> bytes:
    return await get_event_loop().run_in_executor(None, hashpw, data.encode(), gensalt())


async def git_token(githubCode: str):
    return "dada"

import asyncio
import uuid
from asyncio import get_event_loop
from email.message import EmailMessage
from uuid import UUID

import aiosmtplib
from aiosmtplib import send, SMTP
from bcrypt import hashpw, gensalt
from web3 import Web3


async def hashing(data: str) -> str:
    return Web3.solidityKeccak(['bytes32'], [
        '0x' + (await get_event_loop().run_in_executor(None, hashpw, data.encode(), gensalt())).hex()]).hex()


async def git_token(githubCode: str):
    return '1'


async def send_email(email, hash_email, github_token, email_token: UUID, e_from, e_pass):
    message = EmailMessage()
    message["From"] = e_from
    message["To"] = email
    message["Subject"] = "Verification!"
    message.set_content(
        f"To pass verification, follow the link:\nhttp://localhost:3000/email-success?code={github_token}&email_token={email_token.hex}&email={hash_email}")

    async with SMTP(hostname="smtp.gmail.com", port=465, use_tls=True, username=e_from, password=e_pass) as smtp:
        await smtp.send_message(message)


# asyncio.get_event_loop().run_until_complete(
#     send_email('agibalov129@gmail.com', 'hash_email111', 'github_token111', uuid.uuid4()))

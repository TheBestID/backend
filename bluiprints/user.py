from sanic import Blueprint
from sanic.response import Request, text

from table import Users

user = Blueprint("user", url_prefix="/user")


@user.post("/address")
async def create_company(request: Request):
    Users.
    return text("Done.")

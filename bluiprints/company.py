from sanic import Blueprint
from sanic.response import Request, text

company = Blueprint("company", url_prefix="/company")


@company.post("/create")
async def create_company(request: Request):
    return text("Done.")


@company.get("/")
async def get_company(request: Request):
    return text("Company #1.")

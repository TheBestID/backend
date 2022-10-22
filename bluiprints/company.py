from sanic.response import json, Request, text
from sanic import Blueprint

company = Blueprint("company", url_prefix="/company")


@company.post("/create")
async def create_company(request: Request):
    return text("Done.")


@company.get("/")
async def get_company(request: Request):
    return text("Company #1.")

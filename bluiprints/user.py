from sanic.response import json, Request, text
from sanic import Blueprint

user = Blueprint("user", url_prefix="/user")

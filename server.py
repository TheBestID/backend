from sanic import Sanic, text
from bluiprints.company import company
from bluiprints.user import user
from sanic_openapi import openapi3_blueprint

app = Sanic("SoulID")
# app.blueprint(openapi3_blueprint)

app.blueprint(company)
app.blueprint(user)

if __name__ == "__main__":
    app.run(dev=True)  # , fast=True

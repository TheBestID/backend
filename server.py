from databases import Database
from sanic import Sanic

from bluiprints.company import company
from bluiprints.user import user

app = Sanic("SoulID")
app.config.HEALTH = True

app.blueprint(company)
app.blueprint(user)


if __name__ == "__main__":
    app.run(dev=True)  # , fast=True

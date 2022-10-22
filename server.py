from sanic import Sanic
from bluiprints.company import company
from bluiprints.user import user

app = Sanic("SoulID")

app.blueprint(company)
app.blueprint(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, dev=True)  # , fast=True

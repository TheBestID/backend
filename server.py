from asyncpg import create_pool
from sanic import Sanic

# from blueprints.company import company
from blueprints.user import user
from config import host, password, database, username
from table import create

app = Sanic("SoulID")

app.config.HEALTH = False

# app.blueprint(company)
app.blueprint(user)


@app.before_server_start
async def init(app1):
    app1.config['POOL'] = await create_pool(host=host, user=username, password=password, database=database, min_size=2,
                                            max_size=5)
    await create(app1.config['POOL'])


@app.before_server_stop
async def stop(app1):
    app1.config['POOL'].close()


if __name__ == "__main__":
    app.run(dev=True)  # , fast=True

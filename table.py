from sqlalchemy import Table, Column, MetaData, Integer, String

metadata = MetaData()

Users = Table("users", metadata,
              Column('id', Integer, primary_key=True),
              Column('address', String),
              Column('github', String),
              Column('email', String),
              Column('sbt', String))

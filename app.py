from flask import Flask
from peewee import SqliteDatabase

app = Flask(__name__)
app.config.from_object('config')

db = SqliteDatabase('games.db',
                    pragmas={('foreign_keys', 1), ('ignore_check_constraints', 0)})
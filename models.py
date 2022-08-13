from peewee import AutoField, CharField, IntegerField, ForeignKeyField, Model, DateField, DecimalField
from app import db

class Genre(Model):
    GenreId = AutoField()
    GenreName = CharField(unique=True)

    class Meta:
        database = db

class Temp_Genre(Model):
    GenreId = AutoField()
    GenreName = CharField()

    class Meta:
        database = db


class Game(Model):
    GameId = AutoField()
    GameTitle = CharField(unique=True)
    ReleaseDate = DateField()
    GenreId = ForeignKeyField(Genre)

    class Meta:
        database = db

class Temp_Game(Model):
    GameId = AutoField()
    GameTitle = CharField()
    ReleaseDate = DateField()
    GenreId = ForeignKeyField(Genre)

    class Meta:
        database = db


class WishList(Model):
    WishListId = AutoField()
    GameId = ForeignKeyField(Game, on_delete='CASCADE', unique=True)

    class Meta:
        database = db


class PlayList(Model):
    PlaylistId = AutoField()
    PlayingTime = DecimalField(max_digits=3, decimal_places=2, auto_round=True, rounding='ROUND_DOWN')
    PurchaseDate = DateField()
    PurchasePrice = DecimalField(max_digits=3, decimal_places=2, auto_round=True, rounding='ROUND_DOWN')
    Rating = IntegerField()
    GameId = ForeignKeyField(Game, on_delete='CASCADE', unique=True)

    class Meta:
        database = db

# Create tables
def create_tables():
    with db.connection_context():
        db.create_tables([Genre, Game, WishList, PlayList])

create_tables()
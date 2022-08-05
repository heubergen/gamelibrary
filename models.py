from peewee import AutoField, CharField, IntegerField, ForeignKeyField, Model, DateField
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
    PlayingTime = IntegerField()
    PurchaseDate = DateField()
    Rating = IntegerField()
    GameId = ForeignKeyField(Game, on_delete='CASCADE', unique=True)

    class Meta:
        database = db
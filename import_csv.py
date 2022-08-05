from sqlite3 import connect
from flask import flash
from pandas import read_csv

from app import db
from error_msg import error_bad_case, error_transfer_temp_to_final
from models import Game, Genre, Temp_Game, Temp_Genre

def import_csv(import_csv_type):
    try:
        match import_csv_type:
            case "ch_genre":
                db.create_tables([Temp_Genre])

                conn = connect('games.db')
                csvfile = read_csv("genres.csv")
                csvfile.to_sql(name='temp_genre', con=conn, if_exists='append', index=False)
                conn.close()

                Genre.insert_from(Temp_Genre.select(Temp_Genre.GenreName),
                                fields=[Genre.GenreName
                                        ]).on_conflict(action='IGNORE').execute()
                db.drop_tables(Temp_Genre)
            case "ch_game":
                db.create_tables([Temp_Game])
                conn = connect('games.db')
                csvfile = read_csv("games.csv")
                csvfile.to_sql(name='temp_game', con=conn, if_exists='append', index=False)
                conn.close()
                Game.insert_from(Temp_Game.select(Temp_Game.GameTitle, Temp_Game.ReleaseDate, Temp_Game.GenreId),
                                fields=[Game.GameTitle, Game.ReleaseDate, Temp_Game.GenreId
                                        ]).on_conflict(action='IGNORE').execute()
                db.drop_tables(Temp_Game)       
            case _:
                flash(error_bad_case)
    except:
        flash(error_transfer_temp_to_final)
        db.drop_tables([Temp_Genre], safe=True)
        db.drop_tables([Temp_Game], safe=True)
import warnings
from flask import flash
from pandas import read_csv


from app import db
from error_msg import error_bad_case, error_transfer_temp_to_final
from models import Game, Genre, Temp_Game, Temp_Genre

def import_csv(import_csv_type, upload_file):
    try:
        match import_csv_type:
            case "ch_genre":
                db.create_tables([Temp_Genre])

                # We use peewee instead of SQLAlchemy to import the csv
                warnings.filterwarnings("ignore", message="pandas only support SQLAlchemy", category=UserWarning)
                csvfile = read_csv(upload_file)
                csvfile.to_sql(name='temp_genre', con=db, if_exists='append', index=False)

                Genre.insert_from(Temp_Genre.select(Temp_Genre.GenreName),
                                fields=[Genre.GenreName
                                        ]).on_conflict(action='IGNORE').execute()
                db.drop_tables(Temp_Genre)
            case "ch_game":
                db.create_tables([Temp_Game])

                # We use peewee instead of SQLAlchemy to import the csv
                warnings.filterwarnings("ignore", message="pandas only support SQLAlchemy", category=UserWarning)
                csvfile = read_csv(upload_file)
                csvfile.to_sql(name='temp_game', con=db, if_exists='append', index=False)

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
from flask import flash, render_template, request, redirect, url_for
from app import app, db
from models import *
from forms import *
from error_msg import *
from import_csv import import_csv

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

#TODO Expand playlist table

def create_tables():
    with db.connection_context():
        db.create_tables([Genre, Game, WishList, PlayList])


create_tables()

data_gameslist_query = (
    "SELECT GameId, GameTitle, ReleaseDate, GenreName FROM game INNER JOIN Genre ON game.GenreId_id = Genre.GenreId;"
)
data_genrelist_query = ("SELECT * FROM Genre")
data_wishlist_query = (
    "SELECT GameId, GameTitle FROM wishlist INNER JOIN game ON wishlist.GameId_id = game.GameId;"
)
data_games_to_wishlist_query = (
    "SELECT GameId, GameTitle FROM game WHERE GameId NOT IN (SELECT GameId_id FROM wishlist);"
)
data_playlist_query = (
    "SELECT PlaylistId,PlayingTime,PurchaseDate,Rating,GameId_id FROM playlist INNER JOIN game ON playlist.GameId_id = game.GameId;"
)
data_games_to_playlist_query = (
    "SELECT GameId, GameTitle FROM game WHERE GameId NOT IN (SELECT GameId_id FROM playlist);"
)

# TODO Loop this!
def update_gamelist():
    global data_gameslist
    cursor = db.execute_sql(data_gameslist_query)
    data_gameslist = cursor.fetchall()


def update_genrelist():
    global data_genrelist
    cursor = db.execute_sql(data_genrelist_query)
    data_genrelist = cursor.fetchall()


def update_wishlist():
    global data_wishlist
    cursor = db.execute_sql(data_wishlist_query)
    data_wishlist = cursor.fetchall()


def update_games_wishlist():
    global data_games_to_wishlist
    cursor = db.execute_sql(data_games_to_wishlist_query)
    data_games_to_wishlist = cursor.fetchall()


def update_games_playlist():
    global data_games_to_playlist
    cursor = db.execute_sql(data_games_to_playlist_query)
    data_games_to_playlist = cursor.fetchall()


def update_playlist():
    global data_playlist
    cursor = db.execute_sql(data_playlist_query)
    data_playlist = cursor.fetchall()


root_game = "/game"
root_genre = "/genre"
root_wishlist = "/wishlist"
root_playlist = "/playlist"
root_import = "/import"
#TODO use them in the template too


@app.route('/', methods=['GET'])
def index():
    return redirect(root_game)


@app.route(root_game, methods=['GET', 'POST'])
def add_game():
    update_genrelist()
    update_gamelist()
    pagetitle = "Game List"

    form = AddGamesForm()
    form.genrechoice.choices = [("0", "")] + [(g[0], g[1])
                                              for g in data_genrelist]
    form2 = RemoveGameButton()
    if form.validate_on_submit():
        with db.atomic():
            Game.create(GameTitle=form.gametitle.data,
                        ReleaseDate=form.date.data,
                        GenreId_id=form.genrechoice.data)
        update_gamelist()
        return redirect(url_for('add_game'))
    return render_template('games.html',
                           form=form,
                           form2=form2,
                           gamelist=data_gameslist,
                           pagetitle=pagetitle,
                           error_add_game=error_add_game,
                           error_add_wishlist=error_add_to_wishlist,
                           error_delete_game=error_delete_game,
                           root_game=root_game)


@app.route('/game/delete/<int:GameId>', methods=['POST'])
def delete_game(GameId):
    form2 = RemoveGameButton()
    if form2.validate_on_submit():
        try:
            game = Game.get(Game.GameId == GameId)
            game.delete_instance()
            update_gamelist()
        except:
            flash(error_delete_game)
    return redirect(request.referrer)


@app.route(root_genre, methods=['GET', 'POST'])
def add_genre():
    update_genrelist()
    pagetitle = "Genre List"
    form = AddGenreForm()
    form2 = RemoveGenreButton()
    if form.validate_on_submit():
        try:
            with db.atomic():
                Genre.create(GenreName=request.form['genretitle'])
            update_genrelist()
            return redirect(url_for('add_genre'))
        except:
            flash(error_add_genre)
    return render_template('genre.html',
                           form=form,
                           form2=form2,
                           genrelist=data_genrelist,
                           pagetitle=pagetitle,
                           error_delete_genre=error_delete_genre,
                           error_add_genre=error_add_genre,
                           root_genre=root_genre)


@app.route('/genre/delete/<int:GenreId>', methods=['POST'])
def delete_genre(GenreId):
    update_genrelist()
    form2 = RemoveGenreButton()
    if form2.validate_on_submit():
        try:
            genre = Genre.get(Genre.GenreId == GenreId)
            genre.delete_instance()
            update_genrelist()
        except:
            flash(error_delete_genre)
    return redirect(request.referrer)


@app.route(root_wishlist, methods=['GET', 'POST'])
def add_wishlist():
    update_wishlist()
    update_games_wishlist()
    pagetitle = "Genre List"
    form = AddGameToWishlistForm()
    form.gametitle.choices = [("0", "")] + [(gw[0], gw[1])
                                            for gw in data_games_to_wishlist]
    form2 = RemoveWishListButton()
    if form.validate_on_submit():
        try:
            with db.atomic():
                WishList.create(GameId=request.form['gametitle'])
            update_wishlist()
            return redirect(url_for('add_wishlist'))
        except:
            flash(error_add_to_wishlist)
    return render_template(
        'wishlist.html',
        form=form,
        form2=form2,
        wishlist=data_wishlist,
        pagetitle=pagetitle,
        error_delete_from_wishlist=error_delete_from_wishlist,
        error_add_to_wishlist=error_add_to_wishlist,
        root_wishlist=root_wishlist)


@app.route('/wishlist/remove/<int:GameId>', methods=['POST'])
def remove_wishlist(GameId):
    form2 = RemoveWishListButton()
    if form2.validate_on_submit():
        try:
            genre = WishList.get(WishList.GameId == GameId)
            genre.delete_instance()
            update_games_wishlist()
        except:
            flash(error_delete_genre)
    return redirect(request.referrer)


@app.route(root_playlist, methods=['GET', 'POST'])
def add_playlist():
    update_playlist()
    update_games_playlist()
    pagetitle = "Play List"
    form = AddGameToPlayListForm()
    form.gametitle.choices = [("0", "")] + [(gp[0], gp[1])
                                            for gp in data_games_to_playlist]
    form2 = RemovePlayListButton()
    if form.validate_on_submit():
        try:
            with db.atomic():
                PlayList.create(GameId=form.gametitle.data,
                                PlayingTime=form.playtime.data,
                                PurchaseDate=form.date.data,
                                Rating=form.rating.data)
            update_playlist()
            update_games_playlist()
            return redirect(url_for('add_playlist'))
        except:
            flash(error_add_to_playlist)
    return render_template(
        'playlist.html',
        form=form,
        form2=form2,
        playlist=data_playlist,
        pagetitle=pagetitle,
        error_add_to_playlist=error_add_to_playlist,
        error_delete_from_playlist=error_delete_from_playlist,
        root_playlist=root_playlist)


@app.route('/playlist/remove/<int:PlaylistId>', methods=['POST'])
def remove_playlist(PlaylistId):
    form2 = RemovePlayListButton()
    if form2.validate_on_submit():
        try:
            genre = PlayList.get(PlayList.PlaylistId == PlaylistId)
            genre.delete_instance()
            update_playlist()
            update_games_playlist()
        except:
            flash(error_delete_from_playlist)
    return redirect(request.referrer)


@app.route(root_import, methods=['GET', 'POST'])
def process_import():
    pagetitle = "Import"
    form = ImportDataForm()
    if form.validate_on_submit():
        upload_file = form.csv_file.data
        import_csv_type = form.type.data
        import_csv(import_csv_type, upload_file)
        return redirect(url_for('process_import'))
    return render_template(
        'import.html',
        pagetitle=pagetitle,
        form=form,
        error_transfer_temp_to_final=error_transfer_temp_to_final,
        error_bad_case=error_bad_case,
        root_import=root_import)

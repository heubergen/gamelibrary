from flask import flash, render_template, request, redirect, url_for
from app import app, db
from models import *
from forms import *
from error_msg import *
from import_csv import import_csv

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

#TODO Custom error messages for everything
#TODO Try to use function for create and remove db entries
#TODO Add visualization
#TODO Try to add settings page
#TODO Try out SASS


data_gameslist_query = (
    "SELECT GameId, GameTitle, ReleaseDate, GenreName FROM game INNER JOIN Genre ON game.GenreId_id = Genre.GenreId;"
)
data_genrelist_query = ("SELECT * FROM Genre")

data_wishlist_query = (
    "SELECT GameId, GameTitle, GenreName FROM wishlist INNER JOIN game ON wishlist.GameId_id = game.GameId INNER JOIN genre on game.GenreId_id = genre.GenreId;"
)
data_games_to_wishlist_query = (
    "SELECT GameId, GameTitle FROM game WHERE GameId NOT IN (SELECT GameId_id FROM wishlist);"
)
data_playlist_query = (
    "SELECT PlaylistId,GameTitle,PlayingTime,PurchaseDate,PurchasePrice,Rating, ROUND((PurchasePrice/PlayingTime), 2), ROUND(((PurchasePrice/PlayingTime)/(Rating*2)/10), 2) FROM playlist INNER JOIN game ON playlist.GameId_id = game.GameId;"
)
data_games_to_playlist_query = (
    "SELECT GameId, GameTitle FROM game WHERE GameId NOT IN (SELECT GameId_id FROM playlist);"
)

def update_lists(tmp_sql_query):
    with db.connection_context():
        cursor = db.execute_sql(tmp_sql_query)
        data_gameslist = cursor.fetchall()
        return data_gameslist


root_game = "/game"
root_genre = "/genre"
root_wishlist = "/wishlist"
root_playlist = "/playlist"
root_import = "/import"


@app.route('/', methods=['GET'])
def index():
    return redirect(root_game)


@app.route(root_game, methods=['GET', 'POST'])
def add_game():
    data_genrelist = update_lists(data_genrelist_query)
    data_gameslist = update_lists(data_gameslist_query)
    pagetitle = "Game List"

    form = AddGamesForm()
    form.genrechoice.choices = [("0", "")] + [(g[0], g[1])
                                              for g in data_genrelist]
    form2 = RemoveGameButton()
    if form.validate_on_submit():
        try:
            with db.connection_context():
                with db.atomic():
                    Game.create(GameTitle=form.gametitle.data,
                                ReleaseDate=form.date.data,
                                GenreId_id=form.genrechoice.data)
                update_lists(data_gameslist_query)
        except:
            if app.debug:
                raise
            else:
                flash(error_add_game)
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
            with db.connection_context():
                game = Game.get(Game.GameId == GameId)
                game.delete_instance()
                update_lists(data_gameslist_query)
        except:
            if app.debug:
                raise
            else:
                flash(error_delete_game)
    return redirect(request.referrer)


@app.route(root_genre, methods=['GET', 'POST'])
def add_genre():
    data_genrelist = update_lists(data_genrelist_query)
    pagetitle = "Genre List"
    form = AddGenreForm()
    form2 = RemoveGenreButton()
    if form.validate_on_submit():
        try:
            with db.connection_context():
                with db.atomic():
                    Genre.create(GenreName=request.form['genretitle'])
                update_lists(data_genrelist_query)
                return redirect(url_for('add_genre'))
        except:
            if app.debug:
                raise
            else:
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
    update_lists(data_genrelist_query)
    form2 = RemoveGenreButton()
    if form2.validate_on_submit():
        try:
            with db.connection_context():
                genre = Genre.get(Genre.GenreId == GenreId)
                genre.delete_instance()
                update_lists(data_genrelist_query)
        except:
            if app.debug:
                raise
            else:
                flash(error_delete_genre)
    return redirect(request.referrer)


@app.route(root_wishlist, methods=['GET', 'POST'])
def add_wishlist():
    data_wishlist = update_lists(data_wishlist_query)
    data_games_to_wishlist = update_lists(data_games_to_wishlist_query)
    pagetitle = "Genre List"
    form = AddGameToWishlistForm()
    form.gametitle.choices = [("0", "")] + [(gw[0], gw[1])
                                            for gw in data_games_to_wishlist]
    form2 = RemoveWishListButton()
    if form.validate_on_submit():
        try:
            with db.connection_context():
                with db.atomic():
                    WishList.create(GameId=request.form['gametitle'])
                update_lists(data_wishlist_query)
                return redirect(url_for('add_wishlist'))
        except:
            if app.debug:
                raise
            else:
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
            with db.connection_context():
                genre = WishList.get(WishList.GameId == GameId)
                genre.delete_instance()
                update_lists(data_games_to_wishlist_query)
        except:
            if app.debug:
                raise
            else:
                flash(error_delete_genre)
    return redirect(request.referrer)


@app.route(root_playlist, methods=['GET', 'POST'])
def add_playlist():
    data_playlist = update_lists(data_playlist_query)
    data_games_to_playlist = update_lists(data_games_to_playlist_query)
    pagetitle = "Play List"
    form = AddGameToPlayListForm()
    form.gametitle.choices = [("0", "")] + [(gp[0], gp[1])
                                            for gp in data_games_to_playlist]
    form2 = RemovePlayListButton()
    if form.validate_on_submit():
        try:
            with db.connection_context():
                with db.atomic():
                    PlayList.create(GameId=form.gametitle.data,
                                    PlayingTime=form.playtime.data,
                                    PurchaseDate=form.date.data,
                                    PurchasePrice=form.price.data,
                                    Rating=form.rating.data)
            update_lists(data_playlist_query)
            update_lists(data_games_to_playlist_query)
            return redirect(url_for('add_playlist'))
        except:
            if app.debug:
                raise
            else:
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
            with db.connection_context():
                genre = PlayList.get(PlayList.PlaylistId == PlaylistId)
                genre.delete_instance()
                update_lists(data_playlist_query)
                update_lists(data_games_to_playlist_query)
        except:
            if app.debug:
                raise
            else:
                flash(error_delete_from_playlist)
    return redirect(request.referrer)


@app.route(root_import, methods=['GET', 'POST'])
def process_import():
    pagetitle = "Import"
    form = ImportDataForm()
    if form.validate_on_submit():
        try:
            upload_file = form.csv_file.data
            import_csv_type = form.type.data
            import_csv(import_csv_type, upload_file)
            return redirect(url_for('process_import'))
        except:
            if app.debug:
                raise
            else:
                flash(error_csv_import)
    return render_template(
        'import.html',
        pagetitle=pagetitle,
        form=form,
        error_transfer_temp_to_final=error_transfer_temp_to_final,
        error_bad_case=error_bad_case,
        root_import=root_import)
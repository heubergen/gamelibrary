from app import db

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
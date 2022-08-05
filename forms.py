from random import random
from wtforms import Form, StringField, validators, SelectField, DateField, SubmitField, DecimalField, FileField

class AddGamesForm(Form):
    gametitle = StringField('Title', [validators.Length(min=1, max=200)])
    date = DateField('Release Date')
    genrechoice = SelectField('Genre', [validators.DataRequired()], coerce=int)
    submit = SubmitField('Add Game')


class RemoveGameButton(Form):
    submit = SubmitField('Delete', id="delete_button")


class AddGenreForm(Form):
    genretitle = StringField('Title', [validators.Length(min=1, max=200)])
    submit = SubmitField('Add Genre')


class RemoveGenreButton(Form):
    submit = SubmitField('Delete', id="delete_button")


class RemoveWishListButton(Form):
    submit = SubmitField('Remove', id="remove_button")


class AddGameToWishlistForm(Form):
    gametitle = SelectField('Game', [validators.DataRequired()], coerce=int)
    submit = SubmitField('Add Game to Wishlist')


class AddGameToPlayListForm(Form):
    gametitle = SelectField('Game', [validators.DataRequired()], coerce=int)
    playtime = DecimalField('Playing Time')
    date = DateField('Purchase Date')
    rating = DecimalField('Rating (1-10)')
    submit = SubmitField('Add Game to Playlist')

class RemovePlayListButton(Form):
    submit = SubmitField('Remove', id="delete_button")

class ImportGenreForm(Form):
    type = SelectField('Type Of Import', choices=[('0', ''), ('ch_genre', 'Genres'), ('ch_game', 'Game')])
    submit = SubmitField('Import')
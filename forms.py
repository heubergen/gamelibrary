from wtforms import Form, StringField, validators, SelectField, DateField, SubmitField, DecimalField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class AddGamesForm(FlaskForm):
    gametitle = StringField('Title', [validators.Length(min=1, max=200)])
    date = DateField('Release Date')
    genrechoice = SelectField('Genre', [validators.DataRequired()], coerce=int)
    submit = SubmitField('Add Game')


class RemoveGameButton(FlaskForm):
    submit = SubmitField('Delete', id="delete_button")


class AddGenreForm(FlaskForm):
    genretitle = StringField('Title', [validators.Length(min=1, max=200)])
    submit = SubmitField('Add Genre')


class RemoveGenreButton(FlaskForm):
    submit = SubmitField('Delete', id="delete_button")


class RemoveWishListButton(FlaskForm):
    submit = SubmitField('Remove', id="delete_button")


class AddGameToWishlistForm(FlaskForm):
    gametitle = SelectField('Game', [validators.DataRequired()], coerce=int)
    submit = SubmitField('Add Game to Wishlist')


class AddGameToPlayListForm(FlaskForm):
    gametitle = SelectField('Game', [validators.DataRequired()], coerce=int)
    playtime = DecimalField('Playing Time')
    date = DateField('Purchase Date')
    price = DecimalField('Purchase Price')
    rating = DecimalField('Rating (1-10)')
    submit = SubmitField('Add Game to Playlist')

class RemovePlayListButton(FlaskForm):
    submit = SubmitField('Remove', id="delete_button")

class ImportDataForm(FlaskForm):
    type = SelectField('Type Of Import', choices=[('0', ''), ('ch_genre', 'Genres'), ('ch_game', 'Game')])
    csv_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'CSV only!')])
    submit = SubmitField('Import')
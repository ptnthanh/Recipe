from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    ingre = StringField('Ingredient to add', validators=[DataRequired()])
    submit = SubmitField('Add')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    ingre = None
    form = NameForm()
    if form.validate_on_submit():
        ingre = form.ingre.data
        form.ingre.data = ''
    return render_template('index.html', form=form, ingre=ingre)

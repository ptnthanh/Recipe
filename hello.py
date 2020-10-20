from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime

app = Flask(__name__)
application = app

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'

bootstrap = Bootstrap(app)
moment = Moment(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#Create database model
class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #Function to return string when we add sth
    def __repr__(self):
        return '<Name %r>' % self.id


class IngredientForm(FlaskForm):
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
    form = IngredientForm()
    if form.validate_on_submit():
        ingre = form.ingre.data
        new_ingre = Ingredients(name=ingre)
        form.ingre.data = ''

        #Push to database
        try:
            db.session.add(new_ingre)
            db.session.commit()
            return redirect('/assignment09')
        except:
            return "There was an error adding new ingredient"
    else:
        ingredients = Ingredients.query.order_by(Ingredients.date_created)
        return render_template('index.html', form=form, ingredients=ingredients)

if __name__ == '__main__':
    manager.run()

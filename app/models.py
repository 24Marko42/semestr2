from . import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import current_app

recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

saves = db.Table('saves',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    liked = db.relationship('Recipe', secondary=likes, backref='liked_by', lazy='dynamic')
    saved = db.relationship('Recipe', secondary=saves, backref='saved_by', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    steps = db.Column(db.Text)
    image = db.Column(db.String(200))
    image_url = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship('Tag', secondary=recipe_tags, backref='recipes')

    def to_dict(self):
        d = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': self.ingredients,
            'steps': self.steps,
            'image': self.image,
            'image_url': self.image_url,
            'author': self.author.username if self.author else None,
            'tags': [t.name for t in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        try:
            likes = self.liked_by.count()
        except Exception:
            likes = len(self.liked_by)
        d['likes'] = likes
        return d

    def image_file_exists(self):
        if not self.image:
            return False
        up = current_app.config.get('UPLOAD_FOLDER')
        if not up:
            return False
        path = os.path.join(up, self.image)
        return os.path.exists(path)

    def __repr__(self):
        return f'<Recipe {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'


@login.user_loader
def load_user(id):
    return db.session.get(User, id)

import os
from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash
from .models import Recipe, Tag
from .forms import RecipeForm
from . import db
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

bp = Blueprint('web', __name__, template_folder='templates')


@bp.route('/')
def index():
    q = request.args.get('q')
    if q:
        recipes = Recipe.query.filter(Recipe.title.ilike(f'%{q}%')).all()
    else:
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes)


@bp.route('/recipe/<int:id>')
def recipe(id):
    r = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=r)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = RecipeForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            up = current_app.config.get('UPLOAD_FOLDER')
            os.makedirs(up, exist_ok=True)
            f = form.image.data
            filename = secure_filename(f.filename)
            path = os.path.join(up, filename)
            f.save(path)
        recipe = Recipe(title=form.title.data,
                        ingredients=form.ingredients.data,
                        steps=form.steps.data,
                        image=filename,
                        author=current_user)
        tag_names = [t.strip() for t in (form.tags.data or '').split(',') if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            recipe.tags.append(tag)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added')
        return redirect(url_for('web.index'))
    return render_template('add_recipe.html', form=form)


@bp.route('/profile')
@login_required
def profile():
    user = current_user
    saved = user.saved.all()
    return render_template('profile.html', user=user, saved=saved)

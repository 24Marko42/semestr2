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
    q = request.args.get('q', '').strip()
    tag = request.args.get('tag', '').strip()
    query = Recipe.query
    if tag:
        # join on tags and filter by exact tag name
        query = query.join(Recipe.tags).filter(Tag.name == tag)
    if q:
        query = query.filter(Recipe.title.ilike(f'%{q}%'))
    recipes = query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes, active_tag=tag, q=q)


@bp.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    r = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=r)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = RecipeForm()
    if form.validate_on_submit():
        filename = None
        image_url = form.image_url.data if hasattr(form, 'image_url') else None
        if form.image.data:
            up = current_app.config.get('UPLOAD_FOLDER')
            os.makedirs(up, exist_ok=True)
            f = form.image.data
            filename = secure_filename(f.filename)
            path = os.path.join(up, filename)
            f.save(path)
        recipe = Recipe(title=form.title.data,
                        description=getattr(form, 'description', None) and form.description.data,
                        ingredients=form.ingredients.data,
                        steps=form.steps.data,
                        image=filename,
                        image_url=image_url if not filename else None,
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
    liked = user.liked.all()
    return render_template('profile.html', user=user, saved=saved, liked=liked)

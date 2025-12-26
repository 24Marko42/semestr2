from flask import Blueprint, jsonify, request
from flask_login import current_user
from .models import Recipe, Tag, User
from . import db

bp = Blueprint('api', __name__)


@bp.route('/recipes', methods=['GET'], strict_slashes=False)
def list_recipes():
    """
    List recipes
    ---
    parameters:
      - in: query
        name: tag
        schema:
          type: string
        description: filter by tag name
    responses:
      200:
        description: List of recipes
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    tag = request.args.get('tag')
    if tag:
        recipes = Recipe.query.join(Recipe.tags).filter(Tag.name == tag).all()
    else:
        recipes = Recipe.query.all()
    return jsonify([r.to_dict() for r in recipes])


@bp.route('/recipes', methods=['POST'], strict_slashes=False)
def create_recipe():
    """
    Create a new recipe
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [title]
            properties:
              title:
                type: string
              description:
                type: string
              ingredients:
                type: string
              steps:
                type: string
              image_url:
                type: string
              tags:
                type: array
                items:
                  type: string
    responses:
      201:
        description: Created recipe
    """
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'error': 'title required'}), 400
    recipe = Recipe(title=title,
                    description=data.get('description'),
                    ingredients=data.get('ingredients'),
                    steps=data.get('steps'),
                    image_url=data.get('image_url'))
    tags = data.get('tags') or []
    for t in tags:
        tag = Tag.query.filter_by(name=t).first()
        if not tag:
            tag = Tag(name=t)
        recipe.tags.append(tag)
    db.session.add(recipe)
    db.session.commit()
    return jsonify(recipe.to_dict()), 201


@bp.route('/recipes/<int:id>', methods=['GET'], strict_slashes=False)
def get_recipe(id):
    """
    Get a recipe by id
    ---
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Recipe found
    """
    r = Recipe.query.get_or_404(id)
    return jsonify(r.to_dict())


@bp.route('/recipes/<int:id>', methods=['PUT'], strict_slashes=False)
def update_recipe(id):
    """
    Update a recipe
    ---
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              ingredients:
                type: string
              steps:
                type: string
    responses:
      200:
        description: Updated recipe
    """
    r = Recipe.query.get_or_404(id)
    data = request.get_json() or {}
    r.title = data.get('title', r.title)
    r.ingredients = data.get('ingredients', r.ingredients)
    r.steps = data.get('steps', r.steps)
    db.session.commit()
    return jsonify(r.to_dict())


@bp.route('/recipes/<int:id>', methods=['DELETE'], strict_slashes=False)
def delete_recipe(id):
    r = Recipe.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'result': 'deleted'})


@bp.route('/recipes/<int:id>/like', methods=['POST'], strict_slashes=False)
def like_recipe(id):
    """
    Toggle like for a recipe by user_id
    ---
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            required: [user_id]
            properties:
              user_id:
                type: integer
    responses:
      200:
        description: Returns current likes count
    """
    r = Recipe.query.get_or_404(id)
    # Accept user_id via JSON/form or fall back to logged-in user
    user_id = None
    if request.is_json and request.json is not None:
        user_id = request.json.get('user_id')
    else:
        user_id = request.form.get('user_id')
    if not user_id and current_user.is_authenticated:
        user_id = current_user.id
    if not user_id:
        return jsonify({'error': 'authentication required'}), 401
    user = db.session.get(User, id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    if r in user.liked:
        user.liked.remove(r)
    else:
        user.liked.append(r)
    db.session.commit()
    try:
        likes = r.liked_by.count()
    except TypeError:
        likes = len(r.liked_by)
    return jsonify({'likes': likes})


@bp.route('/recipes/<int:id>/save', methods=['POST'], strict_slashes=False)
def save_recipe(id):
    """
    Toggle save for a recipe by user_id (save/unsave)
    ---
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            required: [user_id]
            properties:
              user_id:
                type: integer
    responses:
      200:
        description: Returns number of saved recipes for user
    """
    r = Recipe.query.get_or_404(id)
    user_id = None
    if request.is_json and request.json is not None:
        user_id = request.json.get('user_id')
    else:
        user_id = request.form.get('user_id')
    if not user_id and current_user.is_authenticated:
        user_id = current_user.id
    if not user_id:
        return jsonify({'error': 'authentication required'}), 401
    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({'error': 'user not found'}), 404
    if r in user.saved:
        user.saved.remove(r)
    else:
        user.saved.append(r)
    db.session.commit()
    # number of saved recipes for the user
    try:
        saved_count = user.saved.count()
    except TypeError:
        saved_count = len(user.saved)
    return jsonify({'saved': saved_count})

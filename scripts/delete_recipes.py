from app import create_app
from app.models import Recipe, likes, saves
from app import db

# IDs to delete
TO_DELETE = [1, 4]

app = create_app()
with app.app_context():
    deleted = []
    for rid in TO_DELETE:
        r = Recipe.query.get(rid)
        if not r:
            print(f'Recipe id={rid} not found, skipping')
            continue
        # delete association rows explicitly
        db.session.execute(likes.delete().where(likes.c.recipe_id == rid))
        db.session.execute(saves.delete().where(saves.c.recipe_id == rid))
        # delete the recipe
        db.session.delete(r)
        deleted.append(r.title)
    db.session.commit()

    if deleted:
        print('Deleted recipes:')
        for t in deleted:
            print('-', t)
    else:
        print('No recipes deleted.')

    # show remaining recipes
    print('\nRemaining recipes:')
    for r in Recipe.query.order_by(Recipe.id):
        print(r.id, '|', r.title, '| image_url=', r.image_url)

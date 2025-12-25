from app import create_app, db
from app.models import Recipe, Tag

app = create_app()
with app.app_context():
    if Recipe.query.filter_by(title='Classic Espresso').first():
        print('Classic Espresso already exists, skipping create.')
    else:
        r = Recipe(
            title='Classic Espresso',
            description=None,
            ingredients='Espresso, steamed milk, milk foam',
            steps='1. Pull espresso\n2. Steam milk to velvety texture\n3. Pour and serve'
        )
        tag = Tag.query.filter_by(name='espresso').first()
        if not tag:
            tag = Tag(name='espresso')
            db.session.add(tag)
            db.session.flush()
        r.tags.append(tag)
        db.session.add(r)
        db.session.commit()
        print('Added Classic Espresso with id', r.id)

    # print recipes
    from app.models import Recipe as R
    print('\nCurrent recipes:')
    for rec in R.query.order_by(R.id):
        print(rec.id, '|', rec.title, '| image_url=', rec.image_url)

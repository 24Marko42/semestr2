"""Seed database with example recipes (images from free sources).
Run with: python scripts/seed_recipes.py
"""
from app import create_app, db
from app.models import Recipe, Tag

RECIPES = [
    {
        'title': 'Classic Espresso',
        'description': 'A strong, concentrated coffee brewed by forcing hot water through finely-ground coffee.',
        'ingredients': 'Finely ground espresso coffee, water',
        'steps': '1. Tamp ground coffee\n2. Pull a 25-30s shot\n3. Serve immediately',
        'image_url': 'https://images.unsplash.com/photo-1510627498534-cf7e9002facc?auto=format&fit=crop&w=800&q=60',
        'tags': ['espresso', 'classic']
    },
    {
        'title': 'Cappuccino',
        'description': 'A balanced mix of espresso, steamed milk and velvety milk foam.',
        'ingredients': 'Espresso, steamed milk, milk foam',
        'steps': '1. Pull espresso\n2. Steam milk to velvety texture\n3. Pour and serve',
        'image_url': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=60',
        'tags': ['milk', 'espresso']
    },
    {
        'title': 'Latte',
        'description': 'Smooth espresso with plenty of steamed milk and a light foam layer.',
        'ingredients': 'Espresso, lots of steamed milk, light foam',
        'steps': '1. Pull espresso\n2. Add steamed milk\n3. Top with foam',
        'image_url': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=800&q=60',
        'tags': ['milk', 'mild']
    },
    {
        'title': 'French Press',
        'description': 'Coarse ground coffee steeped in hot water then pressed to separate grounds.',
        'ingredients': 'Coarsely ground coffee, hot water',
        'steps': '1. Add coffee\n2. Pour hot water\n3. Steep 4 minutes\n4. Press and serve',
        'image_url': 'https://images.unsplash.com/photo-1506368249639-73a05d6f6488?auto=format&fit=crop&w=800&q=60',
        'tags': ['filter', 'handbrew']
    },
    {
        'title': 'Cold Brew',
        'description': 'Slow-steeped coffee for a smooth, low-acidity cold coffee concentrate.',
        'ingredients': 'Coarse ground coffee, cold water',
        'steps': '1. Combine grounds and water\n2. Steep 12-24 hours\n3. Filter and serve over ice',
        'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=800&q=60',
        'tags': ['cold', 'refreshing']
    },
    {
        'title': 'Turkish Coffee',
        'description': 'Finely ground coffee simmered in a cezve until foamy; served unfiltered.',
        'ingredients': 'Extra-finely ground coffee, water, sugar (optional)',
        'steps': '1. Mix coffee and water\n2. Heat slowly until foam forms\n3. Serve with grounds',
        'image_url': 'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=800&q=60',
        'tags': ['traditional']
    }
]


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        for r in RECIPES:
            if Recipe.query.filter_by(title=r['title']).first():
                continue
            recipe = Recipe(title=r['title'], description=r['description'], ingredients=r['ingredients'], steps=r['steps'], image_url=r['image_url'])
            for tname in r.get('tags', []):
                tag = Tag.query.filter_by(name=tname).first()
                if not tag:
                    tag = Tag(name=tname)
                recipe.tags.append(tag)
            db.session.add(recipe)
        db.session.commit()
        print('Seeded recipes')


if __name__ == '__main__':
    seed()
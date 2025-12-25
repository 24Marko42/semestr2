from app import create_app
from app.models import Recipe

app = create_app()
with app.app_context():
    print('recipes:', Recipe.query.count())

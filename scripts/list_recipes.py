from app import create_app
from app.models import Recipe
app = create_app()
with app.app_context():
    for r in Recipe.query.order_by(Recipe.id):
        print(r.id, "|", r.title, "| image=", repr(r.image), "| image_url=", r.image_url)

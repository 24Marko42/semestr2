import io
import uuid
import pytest
from app import create_app, db
from app.models import User, Recipe


@pytest.fixture
def client(tmp_path):
    app = create_app(config_overrides={
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'UPLOAD_FOLDER': tmp_path.as_posix()
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_index_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Recipes' in rv.data


def test_add_requires_login(client):
    rv = client.get('/add', follow_redirects=True)
    assert b'Login' in rv.data or b'Please log in' in rv.data


def test_add_post_logged_in(client):
    unique = uuid.uuid4().hex[:6]
    username = f'user_{unique}'
    email = f'user_{unique}@example.com'
    with client.application.app_context():
        user = User(username=username, email=email)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    # login
    rv = client.post('/login', data={'identifier': username, 'password': 'password'}, follow_redirects=True)
    assert b'Recipes' in rv.data

    # post new recipe with image
    data = {
        'title': 'UI Test',
        'description': 'A test description for UI',
        'ingredients': 'coffee',
        'steps': 'brew',
        'tags': 'test',
        'image': (io.BytesIO(b'fakeimagecontent'), 'test.jpg')
    }
    rv2 = client.post('/add', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Recipe added' in rv2.data

    # check file saved
    import os
    files = os.listdir(client.application.config['UPLOAD_FOLDER'])
    assert any('test.jpg' in f for f in files)

    # index contains new recipe and description snippet
    rv3 = client.get('/')
    assert b'UI Test' in rv3.data
    assert b'A test description' in rv3.data


def test_recipe_page_shows(client):
    with client.application.app_context():
        r = Recipe(title='ShowMe', ingredients='a', steps='b')
        db.session.add(r)
        db.session.commit()
        rid = r.id
    rv = client.get(f'/recipe/{rid}')
    assert b'ShowMe' in rv.data


def test_liked_recipes_appear_in_profile(client):
    import uuid
    from app.models import User
    app = client.application
    with app.app_context():
        unique = uuid.uuid4().hex[:6]
        username = f'user_{unique}'
        email = f'user_{unique}@example.com'
        user = User(username=username, email=email)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        # create a recipe
        r = Recipe(title='LikeMe', ingredients='x', steps='y')
        db.session.add(r)
        db.session.commit()
        rid = r.id
    # login
    rv = client.post('/login', data={'identifier': username, 'password': 'password'}, follow_redirects=True)
    assert rv.status_code == 200
    # like via API (no user_id, uses current_user)
    rv_like = client.post(f'/api/recipes/{rid}/like')
    assert rv_like.status_code == 200
    # profile should show the liked recipe
    rv_profile = client.get('/profile')
    assert b'LikeMe' in rv_profile.data
    # now remove like via API (simulate pressing Remove like)
    rv_remove = client.post(f'/api/recipes/{rid}/like')
    assert rv_remove.status_code == 200
    # profile should no longer contain the liked recipe
    rv_profile2 = client.get('/profile')
    assert b'LikeMe' not in rv_profile2.data


def test_tag_search(client):
    from app.models import Tag
    with client.application.app_context():
        r1 = Recipe(title='Espresso Shot', ingredients='a', steps='b')
        r2 = Recipe(title='Foamy Latte', ingredients='c', steps='d')
        t1 = Tag(name='espresso')
        t2 = Tag(name='latte')
        r1.tags.append(t1)
        r2.tags.append(t2)
        db.session.add_all([r1, r2, t1, t2])
        db.session.commit()
    rv = client.get('/?tag=espresso')
    assert b'Espresso Shot' in rv.data
    assert b'Foamy Latte' not in rv.data
    rv2 = client.get('/?tag=espresso&q=Espresso')
    assert b'Espresso Shot' in rv2.data

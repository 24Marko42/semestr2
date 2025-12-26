import pytest
from app import create_app, db
from app.models import Recipe


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


def test_create_and_get_recipe(client):
    data = {
        'title': 'Test',
        'description': 'Small test recipe',
        'ingredients': 'coffee',
        'steps': 'brew',
        'image_url': 'https://images.unsplash.com/photo-1510627498534-cf7e9002facc?auto=format&fit=crop&w=800&q=60',
        'tags': ['espresso']
    }
    rv = client.post('/api/recipes', json=data)
    assert rv.status_code == 201
    j = rv.get_json()
    assert j['title'] == 'Test'
    assert j['description'] == 'Small test recipe'

    rid = j['id']
    rv2 = client.get(f'/api/recipes/{rid}')
    assert rv2.status_code == 200
    j2 = rv2.get_json()
    assert j2['title'] == 'Test'
    assert j2['image_url'] == data['image_url']


def test_like_and_save_recipe(client):
    # create user and recipe
    from app import db
    from app.models import User
    import uuid
    app = client.application
    with app.app_context():
        unique = uuid.uuid4().hex[:6]
        unique_email = f"tester+{unique}@example.com"
        unique_username = f"tester_{unique}"
        user = User(username=unique_username, email=unique_email)
        user.set_password('pw')
        db.session.add(user)
        db.session.commit()
        uid = user.id

    data = {'title': 'ToLike', 'ingredients': 'coffee', 'steps': 'brew'}
    rv = client.post('/api/recipes', json=data)
    assert rv.status_code == 201
    rid = rv.get_json()['id']

    # like
    rv_like = client.post(f'/api/recipes/{rid}/like', json={'user_id': uid})
    assert rv_like.status_code == 200
    assert rv_like.get_json()['likes'] == 1

    # unlike
    rv_like2 = client.post(f'/api/recipes/{rid}/like', json={'user_id': uid})
    assert rv_like2.status_code == 200
    assert rv_like2.get_json()['likes'] == 0

    # save
    rv_save = client.post(f'/api/recipes/{rid}/save', json={'user_id': uid})
    assert rv_save.status_code == 200
    assert rv_save.get_json()['saved'] == 1

    # unsave
    rv_save2 = client.post(f'/api/recipes/{rid}/save', json={'user_id': uid})
    assert rv_save2.status_code == 200
    assert rv_save2.get_json()['saved'] == 0


def test_like_with_authenticated_user(client):
    # create user and recipe
    import uuid
    from app.models import User
    app = client.application
    with app.app_context():
        unique = uuid.uuid4().hex[:6]
        email = f"tester+{unique}@example.com"
        username = f"tester_{unique}"
        user = User(username=username, email=email)
        user.set_password('pw')
        db.session.add(user)
        db.session.commit()
        uid = user.id
        # create recipe
        r = Recipe(title='AuthLike', ingredients='x', steps='y')
        db.session.add(r)
        db.session.commit()
        rid = r.id
    # login via form
    rv = client.post('/login', data={'identifier': username, 'password': 'pw'}, follow_redirects=True)
    assert rv.status_code == 200
    # like without user_id in body
    rv_like = client.post(f'/api/recipes/{rid}/like')
    assert rv_like.status_code == 200
    assert rv_like.get_json()['likes'] == 1
    # unlike
    rv_like2 = client.post(f'/api/recipes/{rid}/like')
    assert rv_like2.status_code == 200
    assert rv_like2.get_json()['likes'] == 0

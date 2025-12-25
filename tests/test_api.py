import json
import pytest
from app import create_app, db
from app.models import Recipe, User


@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # use temporary upload folder
    app.config['UPLOAD_FOLDER'] = tmp_path.as_posix()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_create_and_get_recipe(client):
    data = {'title': 'Test', 'ingredients': 'coffee', 'steps': 'brew', 'tags': ['espresso']}
    rv = client.post('/api/recipes', json=data)
    assert rv.status_code == 201
    j = rv.get_json()
    assert j['title'] == 'Test'

    rid = j['id']
    rv2 = client.get(f'/api/recipes/{rid}')
    assert rv2.status_code == 200
    j2 = rv2.get_json()
    assert j2['title'] == 'Test'


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

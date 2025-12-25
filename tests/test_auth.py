import pytest
from app import create_app, db


@pytest.fixture
def client(tmp_path):
    app = create_app(config_overrides={
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_register_and_login(client):
    import uuid
    unique = uuid.uuid4().hex[:6]
    username = f'user_{unique}'
    email = f'user_{unique}@example.com'

    rv = client.post('/register', data={'username': username, 'email': email, 'password': 'password', 'password2': 'password'}, follow_redirects=True)
    # registration should succeed and we expect the message or redirect to login
    assert b'Registration successful' in rv.data or b'Please log in' in rv.data or b'Login' in rv.data

    # login by username
    rv2 = client.post('/login', data={'identifier': username, 'password': 'password'}, follow_redirects=True)
    assert b'Recipes' in rv2.data

    # logout
    client.get('/logout', follow_redirects=True)

    # login by email
    rv3 = client.post('/login', data={'identifier': email, 'password': 'password'}, follow_redirects=True)
    assert b'Recipes' in rv3.data


def test_register_duplicate(client):
    import uuid
    unique = uuid.uuid4().hex[:6]
    username = f'user_{unique}'
    email = f'user_{unique}@example.com'

    rv = client.post('/register', data={'username': username, 'email': email, 'password': 'password', 'password2': 'password'}, follow_redirects=True)
    assert b'Registration successful' in rv.data or b'Please log in' in rv.data

    # duplicate username
    rv2 = client.post('/register', data={'username': username, 'email': f'other_{unique}@example.com', 'password': 'password', 'password2': 'password'}, follow_redirects=True)
    assert b'Username already taken' in rv2.data or b'Validation errors' in rv2.data

    # duplicate email
    rv3 = client.post('/register', data={'username': f'other_{unique}', 'email': email, 'password': 'password', 'password2': 'password'}, follow_redirects=True)
    assert b'Email already registered' in rv3.data or b'Validation errors' in rv3.data

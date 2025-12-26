from app import create_app, db
from app.models import User

app = create_app(config_overrides={'TESTING': True, 'WTF_CSRF_ENABLED': False, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
with app.app_context():
    db.create_all()
    u1 = User(username='u1', email='u1@example.com')
    u1.set_password('pw')
    u2 = User(username='u2', email='u2@example.com')
    u2.set_password('pw')
    db.session.add_all([u1, u2])
    db.session.commit()

    client = app.test_client()
    # login
    rv = client.post('/login', data={'identifier': 'u1', 'password': 'pw'}, follow_redirects=True)
    print('login status', rv.status_code)
    # GET edit
    rv_get = client.get('/profile/edit')
    print('GET edit len', len(rv_get.data), 'contains Edit Profile?', b'Edit Profile' in rv_get.data)
    # POST duplicate username
    rv_post = client.post('/profile/edit', data={'username': 'u2', 'email': 'u1@example.com', 'new_password': ''}, follow_redirects=True)
    print('POST status', rv_post.status_code)
    s = rv_post.data.decode()
    print('Has error text substring:', 'Username already taken' in s)
    print('----SNIPPET----')
    print('\n'.join(s.splitlines()[:80]))

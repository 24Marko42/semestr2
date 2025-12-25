from app import create_app
app = create_app()
print('App name:', app.name)
print('Debug:', app.debug)
print('URL map routes:')
for r in app.url_map.iter_rules():
    print(r)

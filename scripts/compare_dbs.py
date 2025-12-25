import sqlite3
from pathlib import Path

def recipes_from(db_path):
    if not Path(db_path).exists():
        return []
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    try:
        cur.execute('SELECT id, title, image, image_url FROM recipe')
    except Exception as e:
        return []
    rows = cur.fetchall()
    con.close()
    return rows

curr = recipes_from('app.db')
bak = recipes_from('app.db.bak')

print('Current DB recipes:')
for r in curr:
    print(r)
print('\nBackup DB recipes:')
for r in bak:
    print(r)

# find in bak not in curr by title
curr_titles = {r[1] for r in curr}
only_in_bak = [r for r in bak if r[1] not in curr_titles]
print('\nIn backup but not current:')
for r in only_in_bak:
    print(r)

# find by exact id missing
curr_ids = {r[0] for r in curr}
missing_ids = [r for r in bak if r[0] not in curr_ids]
print('\nIn backup with IDs not in current:')
for r in missing_ids:
    print(r)

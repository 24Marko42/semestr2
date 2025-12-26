import os
from dotenv import load_dotenv
from app import create_app

# Load .env if present
load_dotenv()

app = create_app()


def main():
    """Run the Flask development server and perform helpful startup steps."""
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', os.getenv('PORT', '5000')))
    debug = os.getenv('FLASK_DEBUG', '0') in ('1', 'true', 'True')

    try:
        from app import db
        db_url = os.getenv('DATABASE_URL') or app.config.get('SQLALCHEMY_DATABASE_URI')
        if db_url and db_url.startswith('sqlite:///'):
            sqlite_path = db_url.replace('sqlite:///', '')
            if not os.path.exists(sqlite_path):
                print('Database file not found, creating database and tables...')
                with app.app_context():
                    db.create_all()
                print('Database created.')
    except Exception as e:
        # non-fatal - continue
        print('Warning: could not auto-create DB:', e)

    print(f"Starting Coffee Recipes app on http://{host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()

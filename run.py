from web_school import create_app, db
import os

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(host='localhost', port=1115, debug=True)

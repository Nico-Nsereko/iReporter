from application.routes import Views

from flask import Flask

def server():
    app=Flask(__name__)
    Views.get_views(app)
    return app

App= server()


if __name__ == '__main__':
    App.run(debug=True)
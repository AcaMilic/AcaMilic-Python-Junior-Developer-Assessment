from __init__ import app

from app.routes import web


app.register_blueprint(web)
app.static_folder = "app/static"



if __name__ == '__main__':
    app.run(debug=True, port='5001')
from flask.ext.script import Manager, Server
from app.flask_min import app

manager = Manager(app)
manager.add_command("runserver", 
        Server(host="0.0.0.0", port=8000, debug=True))

if __name__ == '__main__':
    manager.run()
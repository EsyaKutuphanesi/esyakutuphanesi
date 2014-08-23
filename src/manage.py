from flask.ext.script import Server, Manager
from database import manager as database_manager

from esyakutuphanesi import app

manager = Manager(app, with_default_commands=False)

server = Server(host="0.0.0.0", port=5000)

manager.add_command("runserver", server)
manager.add_command("database", database_manager)


if __name__ == "__main__":
    manager.run()

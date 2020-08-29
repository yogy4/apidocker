import unittest
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
# from app import apl, db
# from conf.base import base

from app import backserv, db

migrate = Migrate(backserv, db)
# manager = Manager(apl)
manager = Manager(backserv)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
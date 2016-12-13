from pygres import Pygres
import os

config = dict(
    SQL_HOST=os.environ['LDB_HOST'],
    SQL_DB=os.environ['LDB_DATABASE'],
    SQL_USER=os.environ['LDB_USER'],
    SQL_PASSWORD=os.environ['LDB_PASSWORD'],
    SQL_PORT=os.environ['LDB_PORT'],
)
db = Pygres(config)

from pygres import Pygres

config = dict(
    SQL_HOST='127.0.0.1',
    SQL_DB='bypricet',
    SQL_USER='scrape',
    SQL_PASSWORD='pass',
    SQL_PORT="5433",
)
db = Pygres(config)

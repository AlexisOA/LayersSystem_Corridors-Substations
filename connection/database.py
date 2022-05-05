from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from connection.config import config


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        print("Database not exists")

    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_engine_from_settings():
    params_database = config()
    keys = ['user', 'password', 'host', 'port', 'database']
    if not all(key in keys for key in params_database.keys()):
        raise Exception('Bad config file')

    return get_engine(params_database['user'],
                      params_database['password'],
                      params_database['host'],
                      params_database['port'],
                      params_database['database'])


def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    print(engine.url)
    return session




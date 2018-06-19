import psycopg2
import sys
sys.path.append('../')

from config import config


def init_db(name, user, pasw, host, schema_path):
    with psycopg2.connect(dbname=name, user=user, password=pasw, host=host) as db:
        with open(schema_path, "r") as f:
            db.cursor().execute(f.read())
        db.commit()

# Настройка базы данных
try:
    init_db(
        name=config["DEFAULT"]["DB_NAME"],
        user=config["DEFAULT"]["DB_USER"],
        pasw=config["DEFAULT"]["DB_PASSWORD"],
        host=config["DEFAULT"]["DB_HOST"],
        schema_path=current_path + "/" + "schema.sql")
except BaseException as e:
    print(str(e))

import uuid
from contextlib import contextmanager

import psycopg2
import typer
from passlib.hash import pbkdf2_sha512
from psycopg2.extras import DictCursor

app = typer.Typer()


@contextmanager
def postgres_conntection(**kwargs):
    conn = psycopg2.connect(**kwargs, cursor_factory=DictCursor)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


@app.command()
def main(
    db_password: str,
    email: str = 'admin@admin.admin', password: str = 'admin',
    first_name: str = 'admin', last_name: str = 'admin',
    host: str = 'db',
    port: int = 5432,
    db: str = 'postgres',
    user: str = 'postgres'
):
    dsl = {
        'dbname': db,
        'user': user,
        'password': db_password,
        'host': host,
        'port': port
    }
    with postgres_conntection(**dsl) as pg_conn:
        cursor = pg_conn.cursor()
        user_id = uuid.uuid4()
        password = pbkdf2_sha512.hash(password)
        cursor.execute("SELECT id, name from role where name = 'admin'")
        res = cursor.fetchone()
        if res:
            role_id = res[0]
        else:
            role_id = uuid.uuid4()
            cursor.execute(
                "INSERT INTO role (id, name)"
                f"values ('{role_id}', 'admin')")
        cursor.execute(
            "INSERT into public.user "
            "(id, email, first_name, last_name, password)"
            f"VALUES ('{user_id}', '{email}', "
            f"'{first_name}', '{last_name}', '{password}')"
        )
        user_role_id = uuid.uuid4()
        cursor.execute(
            "INSERT INTO user_role (id, user_id, role_id)"
            f"VALUES ('{user_role_id}', '{user_id}', '{role_id}')"
        )


if __name__ == "__main__":
    app()

import os

DATABASE_URL = f"mysql+aiomysql://{os.environ['MARIADB_USER']}:{os.environ['MARIADB_PASSWORD']}@{os.environ['MARIADB_HOST']}:{os.environ['MARIADB_PORT']}/{os.environ['MARIADB_DATABASE']}"

TOTAL_USERS = 40_000_000

INSERT_QUERY = "INSERT INTO users(full_name, birth_date) VALUES (:full_name, :birth_date)"

STATUS_OK = {"success": True}

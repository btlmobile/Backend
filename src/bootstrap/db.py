import logging
from sqlalchemy import text


def init_db():
    try:
        from src.config.db_dev import Base, engine, database

        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            check_role = conn.execute(
                text(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=:db AND TABLE_NAME='users' AND COLUMN_NAME='role'"
                ),
                {"db": database},
            ).scalar_one()
            if int(check_role) == 0:
                conn.execute(
                    text(
                        "ALTER TABLE users ADD COLUMN `role` VARCHAR(32) NOT NULL DEFAULT 'user'"
                    )
                )
            check_role_level = conn.execute(
                text(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=:db AND TABLE_NAME='users' AND COLUMN_NAME='role_level'"
                ),
                {"db": database},
            ).scalar_one()
            if int(check_role_level) == 0:
                conn.execute(
                    text(
                        "ALTER TABLE users ADD COLUMN `role_level` INT NOT NULL DEFAULT 0"
                    )
                )
            conn.commit()
    except Exception as e:
        logging.getLogger("bootstrap").error("db init failed: %s", str(e))

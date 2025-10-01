from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.helper.settings_helper import load_settings

settings = load_settings()
mysql_cfg = settings.get("mysql", {})
user = mysql_cfg.get("user", "btl")
password = mysql_cfg.get("password", "secret")
host = mysql_cfg.get("host", "localhost")
port = int(mysql_cfg.get("port", 3306))
database = mysql_cfg.get("database", "btl_mobile")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

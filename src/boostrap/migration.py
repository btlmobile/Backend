from redis_om import Migrator

from src.features.api.store_bottle.stored_bottle_entity import StoredBottleEntity
from src.features.auth.auth_entity import AuthUserEntity
from src.features.chat.chat_entity import ChatEntity
from src.features.report.report_entity import ReportEntity
from src.features.sea.bottle.bottle_entity import BottleEntity


def run_migrations() -> None:
    # Entities must be imported for Migrator to detect them
    migrator = Migrator()
    migrator.run()


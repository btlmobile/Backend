from redis_om import Migrator

# Import all models
from src.features.api.store_bottle.stored_bottle_entity import StoredBottleEntity
from src.features.auth.auth_entity import AuthUserEntity
from src.features.chat.chat_entity import ChatEntity
from src.features.sea.bottle.bottle_entity import BottleEntity
from src.shared.base.redis_model import BaseRedisModel

print("Running manual migration...")
migrator = Migrator()
migrator.run()
print("Migration done.")

print("Checking ChatEntity index...")
try:
    print(ChatEntity.find().all())
    print("ChatEntity find() worked.")
except Exception as e:
    print(f"ChatEntity find() failed: {e}")

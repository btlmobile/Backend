from redis_om import Migrator

def run_migrations() -> None:
    migrator = Migrator()
    migrator.run()


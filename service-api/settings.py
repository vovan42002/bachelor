from envparse import Env

env = Env()

DB_HOST = env.str("DB_HOST", default="localhost")
DB_USERNAME = env.str("DB_USERNAME", default="postgres")
DB_PASSWORD = env.str("DB_PASSWORD", default="postgres")
DB_NAME = env.str("DB_NAME", default="diploma")
DB_PORT = env.str("DB_PORT", default="5432")

DATABASE_URL = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=10)

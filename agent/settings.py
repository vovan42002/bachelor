from envparse import Env

env = Env()

SERVER_API_HOST = env.str(
    "SERVER_API_HOST",
    default=f"localhost",
)
SERVER_API_PORT = env.int(
    "SERVER_API_PORT",
    default=8000,
)

EMAIL = env.str("EMAIL", default="user@example.com")
PASSWORD = env.str("PASSWORD", default="123456")
TIMEOUT = env.int("TIMEOUT", default=30)
RENEW_TOKEN_TIMEOUT = env.int("RENEW_TOKEN_TIMEOUT", default=10)

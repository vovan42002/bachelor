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

ESP_API_HOST = env.str(
    "ESP_API_HOST",
    default=f"localhost",
)
ESP_API_PORT = env.int(
    "ESP_API_PORT",
    default=3000,
)

ESP_URL = f"http://{ESP_API_HOST}:{ESP_API_PORT}"

EMAIL = env.str("EMAIL", default="user@example.com")
PASSWORD = env.str("PASSWORD", default="123456")
TIMEOUT = env.int("TIMEOUT", default=30)
RENEW_TOKEN_TIMEOUT = env.int("RENEW_TOKEN_TIMEOUT", default=10)

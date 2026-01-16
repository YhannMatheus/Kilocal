from src.core.config import settings
from urllib.parse import urlparse, parse_qs, urlunparse
import ssl

def get_tortoise_url(url: str):
    url = url.replace("postgresql://", "postgres://")
    
    parsed = urlparse(url)
    
    return urlunparse(parsed._replace(query=""))

database_url = get_tortoise_url(settings.DATABASE_URL)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": urlparse(database_url).path[1:],
                "host": urlparse(database_url).hostname,
                "password": urlparse(database_url).password,
                "user": urlparse(database_url).username,
                "port": urlparse(database_url).port or 5432,
                "ssl": ssl_context,
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                "src.types.models.user", 
                "src.types.models.workout", 
                "src.types.models.exercise", 
                "src.types.models.sets", 
                "src.types.models.body_assessments",
                "src.types.models.caloric_intakes",
                "src.types.models.session",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}